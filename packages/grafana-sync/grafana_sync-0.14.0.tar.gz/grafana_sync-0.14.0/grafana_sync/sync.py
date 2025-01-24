import logging
from collections.abc import Mapping
from typing import TYPE_CHECKING

from grafana_sync.api.client import FOLDER_GENERAL, FOLDER_SHAREDWITHME
from grafana_sync.api.models import DatasourceDefinition
from grafana_sync.dashboards.models import DataSource, DSRef
from grafana_sync.datasource_mapper import map_datasources
from grafana_sync.exceptions import (
    DashboardNotFoundError,
    DestinationParentNotFoundError,
)

if TYPE_CHECKING:
    from rich.table import Table

    from grafana_sync.api.client import GrafanaClient
    from grafana_sync.api.models import DashboardData

logger = logging.getLogger(__name__)


class GrafanaSync:
    """Handles synchronization of folders and dashboards between Grafana instances."""

    ds_map: Mapping[str, DSRef] | None
    src_datasources: list[DatasourceDefinition] | None
    dst_datasources: list[DatasourceDefinition] | None
    src_ds_config: Mapping[str, DataSource] | None

    def __init__(
        self,
        src_grafana: "GrafanaClient",
        dst_grafana: "GrafanaClient",
        *,
        dst_parent_uid: str | None = None,
        migrate_datasources: bool = False,
    ) -> None:
        self.src_grafana = src_grafana
        self.dst_grafana = dst_grafana
        self.folder_relocation_queue: dict[str, str] = {}
        self.dst_parent_uid = dst_parent_uid
        self.migrate_datasources = migrate_datasources
        self.ds_map = None
        self.src_datasources = None
        self.dst_datasources = None
        self.src_ds_config = None

    async def sync_folder(
        self,
        folder_uid: str,
        can_move: bool,
        dry_run: bool,
    ) -> None:
        """Sync a single folder from source to destination Grafana instance."""
        src_folder = await self.src_grafana.get_folder(folder_uid)
        title = src_folder.title
        parent_uid = src_folder.parent_uid or self.dst_parent_uid or FOLDER_GENERAL

        # Check if folder already exists
        try:
            existing_dst_folder = await self.dst_grafana.get_folder(folder_uid)
        except Exception:
            # Folder doesn't exist
            logger.info(
                "%s folder '%s' in destination",
                "Would create" if dry_run else "Creating",
                title,
            )
            if dry_run:
                return
            try:
                # Handle dst_parent_uid for top-level folders
                if parent_uid == FOLDER_GENERAL:
                    if self.dst_parent_uid == FOLDER_GENERAL:
                        dst_parent_uid = None  # Explicitly place at root
                    elif self.dst_parent_uid is not None:
                        dst_parent_uid = self.dst_parent_uid
                    else:
                        dst_parent_uid = None
                else:
                    # Check if parent_uid is available in dst
                    try:
                        await self.dst_grafana.get_folder(parent_uid)
                    except Exception:
                        dst_parent_uid = None
                    else:
                        dst_parent_uid = parent_uid

                await self.dst_grafana.create_folder(
                    title=title, uid=folder_uid, parent_uid=dst_parent_uid
                )
                logger.info("Created folder '%s' (uid: %s)", title, folder_uid)
            except Exception:
                logger.exception("Failed to create folder '%s'", title)
        else:
            if existing_dst_folder.title != title:
                logger.info(
                    "%s folder title '%s' in destination",
                    "Would update" if dry_run else "Updating",
                    title,
                )
                if not dry_run:
                    try:
                        await self.dst_grafana.update_folder(
                            uid=folder_uid,
                            title=title,
                            overwrite=True,
                        )
                    except Exception:
                        logger.exception("Failed to update folder '%s'", title)

            # check if the folder needs to be moved
            if (
                can_move
                and (existing_dst_folder.parent_uid or FOLDER_GENERAL) != parent_uid
            ):
                # since a parent might not exist yet, we enqueue the relocations
                self.folder_relocation_queue[folder_uid] = parent_uid

    async def move_folders_to_new_parents(self, dry_run: bool = False) -> None:
        for folder_uid, parent_uid in self.folder_relocation_queue.items():
            if folder_uid in [FOLDER_GENERAL, FOLDER_SHAREDWITHME]:
                continue  # skip system folders

            target_parent = parent_uid if parent_uid != FOLDER_GENERAL else None
            logger.info(
                "%s folder '%s' to new parent '%s'",
                "Would move" if dry_run else "Moving",
                folder_uid,
                parent_uid,
            )

            if not dry_run:
                try:
                    await self.dst_grafana.move_folder(folder_uid, target_parent)
                except Exception:
                    logger.exception(
                        "Failed to move folder '%s' to new parent '%s'",
                        folder_uid,
                        parent_uid,
                    )
                else:
                    logger.info(
                        "Moved folder '%s' to new parent '%s'", folder_uid, parent_uid
                    )

        self.folder_relocation_queue.clear()

    async def get_folder_dashboards(
        self,
        grafana: "GrafanaClient",
        folder_uid: str,
        recursive: bool,
    ) -> set[str]:
        """Get all dashboard UIDs in a folder (and optionally its subfolders)."""
        dashboard_uids = set()

        try:
            async for _, _, dashboards in grafana.walk(
                folder_uid, recursive, include_dashboards=True
            ):
                for dashboard in dashboards.root:
                    dashboard_uids.add(dashboard.uid)
        except Exception as e:
            logger.warning("Failed to get dashboards for folder %s: %s", folder_uid, e)

        return dashboard_uids

    async def delete_dashboard(self, dashboard_uid: str) -> bool:
        """Delete a dashboard from destination Grafana instance."""
        try:
            await self.dst_grafana.delete_dashboard(dashboard_uid)
        except Exception:
            logger.exception("Failed to delete dashboard %s", dashboard_uid)
            return False
        else:
            logger.info("Deleted dashboard with uid: %s", dashboard_uid)
            return True

    def _clean_dashboard_for_comparison(self, dashboard_data: "DashboardData") -> dict:
        """Remove dynamic fields from dashboard data for comparison."""
        return dashboard_data.model_dump(exclude={"id", "version"}, by_alias=True)

    async def get_src_datasources(self):
        if self.src_datasources is not None:
            return self.src_datasources

        self.src_datasources = (await self.src_grafana.get_datasources()).root
        return self.src_datasources

    async def get_dst_datasources(self):
        if self.dst_datasources is not None:
            return self.dst_datasources

        self.dst_datasources = (await self.dst_grafana.get_datasources()).root
        return self.dst_datasources

    async def get_ds_map(self) -> Mapping[str, DSRef]:
        if self.ds_map is not None:
            return self.ds_map

        self.ds_map = map_datasources(
            await self.get_src_datasources(),
            await self.get_dst_datasources(),
        )

        logger.debug("Mapped datasources: %s", self.ds_map)

        return self.ds_map

    async def get_datasource_mapping_cli_table(self) -> "Table":
        from rich.table import Table

        table = Table(title="Data Source Mapping")

        table.add_column("SRC Name")
        table.add_column("SRC UID")
        table.add_column("SRC Type")
        table.add_column("DST Name")
        table.add_column("DST UID")
        table.add_column("DST Type")

        ds_map = await self.get_ds_map()
        src_datasources = await self.get_src_datasources()
        dst_datasources = await self.get_dst_datasources()

        for src_uid, dst_ds_ref in ds_map.items():
            src_ds = next(ds for ds in src_datasources if ds.uid == src_uid)
            dst_ds = next(ds for ds in dst_datasources if ds.uid == dst_ds_ref.uid)
            table.add_row(
                src_ds.name,
                src_ds.uid,
                src_ds.type_,
                dst_ds.name,
                dst_ds.uid,
                dst_ds.type_,
            )

        return table

    async def get_src_ds_config(self) -> Mapping[str, DataSource]:
        if self.src_ds_config is not None:
            return self.src_ds_config

        self.src_ds_config = {
            ds.name: DataSource(
                type=ds.type_,
                uid=ds.uid,
            )
            for ds in (await self.get_src_datasources())
        }

        return self.src_ds_config

    async def sync_dashboard(
        self,
        dashboard_uid: str,
        folder_uid: str | None = None,
        relocate=True,
        dry_run: bool = False,
    ) -> None:
        """Sync a single dashboard from source to destination Grafana instance."""
        # Get dashboard from source
        src_dashboard = await self.src_grafana.get_dashboard(dashboard_uid)
        if not src_dashboard:
            logger.error("Dashboard %s not found in source", dashboard_uid)
            raise DashboardNotFoundError(dashboard_uid)

        src_data = src_dashboard.dashboard

        if self.migrate_datasources:
            ds_map = await self.get_ds_map()
            src_ds_config = await self.get_src_ds_config()
            src_data.upgrade_datasources(src_ds_config)
            src_data.update_datasources(ds_map)

        if folder_uid == FOLDER_GENERAL:
            target_folder = (
                self.dst_parent_uid if self.dst_parent_uid != FOLDER_GENERAL else None
            )
        else:
            target_folder = folder_uid

        # Check if dashboard exists in destination
        try:
            dst_dashboard = await self.dst_grafana.get_dashboard(dashboard_uid)
        except Exception:
            # Dashboard doesn't exist in destination
            dst_dashboard = None
        else:
            # Compare dashboards after cleaning
            if self._clean_dashboard_for_comparison(
                src_data
            ) == self._clean_dashboard_for_comparison(dst_dashboard.dashboard) and (
                target_folder == dst_dashboard.meta.folder_uid or not relocate
            ):
                logger.info(
                    "Dashboard '%s' (uid: %s) is identical, skipping update",
                    src_data.title,
                    dashboard_uid,
                )
                return

        if dst_dashboard is not None and not relocate:
            target_folder = dst_dashboard.meta.folder_uid

        if dry_run:
            logger.info(
                "Would %s dashboard '%s' (uid: %s) to folder '%s'",
                "update" if dst_dashboard else "create",
                src_data.title,
                dashboard_uid,
                target_folder or "General",
            )
        else:
            await self.dst_grafana.update_dashboard(
                src_data,
                folder_uid=target_folder,
            )
            logger.info(
                "%s dashboard '%s' (uid: %s)",
                "Updated" if dst_dashboard else "Created",
                src_data.title,
                dashboard_uid,
            )

    async def ensure_dst_parent_exists(self) -> None:
        """Verify destination parent exists if specified."""
        if self.dst_parent_uid is not None and self.dst_parent_uid != FOLDER_GENERAL:
            try:
                await self.dst_grafana.get_folder(self.dst_parent_uid)
            except Exception as e:
                raise DestinationParentNotFoundError(self.dst_parent_uid) from e

    async def sync(
        self,
        *,
        folder_uid: str = FOLDER_GENERAL,
        recursive: bool = True,
        include_dashboards: bool = True,
        prune: bool = False,
        relocate_folders: bool = True,
        relocate_dashboards: bool = True,
        dry_run: bool = False,
    ):
        await self.ensure_dst_parent_exists()

        # Track source dashboards if pruning is enabled
        src_dashboard_uids = set()
        dst_dashboard_uids = set()

        if include_dashboards and prune:
            # Get all dashboards in destination folders before we start syncing
            dst_dashboard_uids = await self.get_folder_dashboards(
                self.dst_grafana, folder_uid, recursive
            )

        # if a folder was requested sync it first
        if folder_uid != FOLDER_GENERAL:
            await self.sync_folder(folder_uid, can_move=False, dry_run=dry_run)

        # Now walk and sync child folders and optionally dashboards
        async for root_uid, folders, dashboards in self.src_grafana.walk(
            folder_uid, recursive, include_dashboards=include_dashboards
        ):
            for folder in folders.root:
                if folder == FOLDER_SHAREDWITHME:
                    continue  # skip unsyncable folder

                await self.sync_folder(folder.uid, can_move=True, dry_run=dry_run)

            # Sync dashboards if requested
            if include_dashboards:
                for dashboard in dashboards.root:
                    dashboard_uid = dashboard.uid
                    await self.sync_dashboard(
                        dashboard_uid,
                        root_uid,
                        relocate=relocate_dashboards,
                        dry_run=dry_run,
                    )
                    src_dashboard_uids.add(dashboard_uid)

        if relocate_folders:
            logger.info("relocation folders to updated parents if needed")
            await self.move_folders_to_new_parents(dry_run=dry_run)
        else:
            logger.info("skipping folder relocation (disabled)")

        # Prune dashboards that don't exist in source
        if include_dashboards and prune:
            dashboards_to_delete = dst_dashboard_uids - src_dashboard_uids
            for dashboard_uid in dashboards_to_delete:
                logger.info(
                    "%s dashboard with uid '%s' in destination",
                    "Would delete" if dry_run else "Deleting",
                    dashboard_uid,
                )
                if not dry_run:
                    await self.delete_dashboard(dashboard_uid)
