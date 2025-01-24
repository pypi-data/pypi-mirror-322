import logging
from datetime import datetime
from typing import TYPE_CHECKING

import asyncclick as click
from rich import print as rprint
from rich import print_json
from rich.console import Console
from rich.tree import Tree

from grafana_sync.api.client import FOLDER_GENERAL, GrafanaClient
from grafana_sync.backup import GrafanaBackup
from grafana_sync.restore import GrafanaRestore
from grafana_sync.sync import GrafanaSync

if TYPE_CHECKING:
    from collections.abc import Mapping

    from grafana_sync.api.models import (
        GetDashboardResponse,
        GetFolderResponse,
        GetFoldersResponseItem,
        SearchDashboardsResponseItem,
    )

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option(
    "--url",
    envvar="GRAFANA_URL",
    required=True,
    help="Grafana URL",
)
@click.option(
    "--log-level",
    envvar="LOG_LEVEL",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="INFO",
    help="Set logging level",
)
@click.option(
    "--httpx-log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="WARNING",
    help="Set httpx logging level",
)
@click.option(
    "--api-key",
    envvar="GRAFANA_API_KEY",
    help="Grafana API key for token authentication",
)
@click.option(
    "--username",
    envvar="GRAFANA_USERNAME",
    help="Grafana username for basic authentication",
)
@click.option(
    "--password",
    envvar="GRAFANA_PASSWORD",
    help="Grafana password for basic authentication",
)
@click.pass_context
async def cli(
    ctx: click.Context,
    url: str,
    api_key: str | None,
    username: str | None,
    password: str | None,
    log_level: str,
    httpx_log_level: str,
):
    """Sync Grafana dashboards and folders."""
    logging.basicConfig(level=getattr(logging, log_level.upper()))

    # Set httpx logging level
    logging.getLogger("httpx").setLevel(getattr(logging, httpx_log_level.upper()))

    try:
        ctx.obj = await ctx.with_async_resource(
            GrafanaClient(url, api_key, username, password)
        )
    except ValueError as ex:
        raise click.UsageError(ex.args[0]) from ex


@cli.command(name="list")
@click.option(
    "-f",
    "--folder-uid",
    default=FOLDER_GENERAL,
    help="Optional folder UID to list only subfolders of this folder",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    help="List folders recursively",
)
@click.option(
    "-d",
    "--include-dashboards",
    is_flag=True,
    help="Include dashboards in the output",
)
@click.option(
    "-j",
    "--output-json",
    is_flag=True,
    help="Display output in JSON format",
)
@click.option(
    "-e",
    "--extended",
    is_flag=True,
    help="Show extended dashboard details including update information",
)
@click.pass_context
async def list_folders(
    ctx: click.Context,
    folder_uid: str,
    recursive: bool,
    include_dashboards: bool,
    output_json: bool,
    extended: bool,
) -> None:
    """List folders in a Grafana instance."""
    grafana = ctx.ensure_object(GrafanaClient)

    class TreeDashboardItem:
        """Represents a dashboard item in the folder tree structure."""

        def __init__(
            self,
            data: "SearchDashboardsResponseItem",
            extended_data: "GetDashboardResponse | None" = None,
        ) -> None:
            """Initialize dashboard item with API response data."""
            self.data = data
            self.extended_data = extended_data

        @property
        def label(self) -> str:
            """Get the display label for the dashboard."""
            base_label = f"📊 {self.data.title} ({self.data.uid})"
            if self.extended_data:
                meta = self.extended_data.meta
                # Parse the timestamp
                now = datetime.now().astimezone()
                delta = now - meta.updated

                # Format relative time
                if delta.days > 365:
                    relative = f"{delta.days // 365} years ago"
                elif delta.days > 30:
                    relative = f"{delta.days // 30} months ago"
                elif delta.days > 0:
                    relative = f"{delta.days} days ago"
                elif delta.seconds > 3600:
                    relative = f"{delta.seconds // 3600} hours ago"
                elif delta.seconds > 60:
                    relative = f"{delta.seconds // 60} minutes ago"
                else:
                    relative = "just now"

                updated = f" updated {relative}"
                if meta.updated_by:
                    updated += f" by {meta.updated_by}"
                return f"{base_label}{updated}"
            return base_label

        def to_tree(self, parent: Tree) -> None:
            """Add this dashboard as a node to the parent tree."""
            parent.add(self.label)

        def to_obj(self):
            """Convert dashboard item to JSON-compatible representation."""
            return self.data

    class TreeFolderItem:
        """Represents a folder item in the folder tree structure."""

        children: list["TreeFolderItem | TreeDashboardItem"]

        def __init__(self, data: "GetFolderResponse | GetFoldersResponseItem") -> None:
            """Initialize folder item with API response data."""
            self.children = []
            self.data = data

        def __repr__(self) -> str:
            return f"TreeFolderItem({self.data.title})"

        @property
        def label(self) -> str:
            """Get the display label for the folder."""
            return f"📁 {self.data.title} ({self.data.uid})"

        def to_tree(self, parent: Tree | None = None) -> Tree:
            """Convert folder and its children to a rich Tree structure.

            Args:
                parent: Optional parent tree node to add this folder to

            Returns:
                The created tree node for this folder
            """
            r_tree = Tree(self.label) if parent is None else parent.add(self.label)

            for c in self.children:
                c.to_tree(r_tree)

            return r_tree

        def to_obj(self):
            """Convert folder and its children to JSON-compatible representation."""
            children_data = [c.to_obj() for c in self.children]
            if self.data:
                return {
                    "type": "dash-folder",
                    "children": children_data,
                } | self.data.model_dump(by_alias=True)
            return children_data

    folder_nodes: Mapping[str | None, TreeFolderItem] = {}

    async for root_uid, folders, dashboards in grafana.walk(
        folder_uid, recursive, include_dashboards
    ):
        if root_uid in folder_nodes:
            root_node = folder_nodes[root_uid]
        else:
            root_folder_data = await grafana.get_folder(root_uid)
            root_node = TreeFolderItem(root_folder_data)
            folder_nodes[root_uid] = root_node

        for folder in folders.root:
            if folder.uid not in folder_nodes:
                itm = TreeFolderItem(folder)
                folder_nodes[folder.uid] = itm
                root_node.children.append(itm)

        for dashboard in dashboards.root:
            extended_data = None
            if extended:
                extended_data = await grafana.get_dashboard(dashboard.uid)
            itm = TreeDashboardItem(dashboard, extended_data)
            root_node.children.append(itm)

    main_node = folder_nodes[folder_uid]
    if output_json:
        print_json(data=main_node.to_obj())
    else:
        rprint(main_node.to_tree())


@cli.command(name="sync")
@click.option(
    "--dst-url",
    envvar="GRAFANA_DST_URL",
    required=True,
    help="Destination Grafana URL",
)
@click.option(
    "--dst-api-key",
    envvar="GRAFANA_DST_API_KEY",
    help="Destination Grafana API key for token authentication",
)
@click.option(
    "--dst-username",
    envvar="GRAFANA_DST_USERNAME",
    help="Destination Grafana username for basic authentication",
)
@click.option(
    "--dst-password",
    envvar="GRAFANA_DST_PASSWORD",
    help="Destination Grafana password for basic authentication",
)
@click.option(
    "-f",
    "--folder-uid",
    default=FOLDER_GENERAL,
    help="Optional folder UID to sync only this folder and its subfolders",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    help="Sync folders recursively",
)
@click.option(
    "-d",
    "--include-dashboards",
    is_flag=True,
    help="Include dashboards in the sync",
)
@click.option(
    "-p",
    "--prune",
    is_flag=True,
    help="Remove dashboards in destination that don't exist in source",
)
@click.option(
    "--relocate-folders/--no-relocate-folders",
    default=True,
    help="Move folders to match source folder structure",
)
@click.option(
    "--relocate-dashboards/--no-relocate-dashboards",
    default=True,
    help="Move dashboards to match source folder structure",
)
@click.option(
    "--dst-parent-uid",
    help="Optional destination parent folder UID to sync everything under",
)
@click.option(
    "--migrate-datasources",
    is_flag=True,
    help="Migrate dashboard datasource references to match destination",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Only print modifying changes",
)
@click.pass_context
async def sync_folders(
    ctx: click.Context,
    dst_url: str,
    dst_api_key: str | None,
    dst_username: str | None,
    dst_password: str | None,
    folder_uid: str,
    recursive: bool,
    include_dashboards: bool,
    prune: bool,
    relocate_folders: bool,
    relocate_dashboards: bool,
    dst_parent_uid: str | None,
    migrate_datasources: bool,
    dry_run: bool,
) -> None:
    """Sync folders from source to destination Grafana instance."""
    src_grafana = ctx.ensure_object(GrafanaClient)
    async with GrafanaClient(
        dst_url, dst_api_key, dst_username, dst_password
    ) as dst_grafana:
        syncer = GrafanaSync(
            src_grafana,
            dst_grafana,
            dst_parent_uid=dst_parent_uid,
            migrate_datasources=migrate_datasources,
        )

        table = await syncer.get_datasource_mapping_cli_table()

        console = Console()
        console.print(table)

        await syncer.sync(
            folder_uid=folder_uid,
            recursive=recursive,
            include_dashboards=include_dashboards,
            prune=prune,
            relocate_folders=relocate_folders,
            relocate_dashboards=relocate_dashboards,
            dry_run=dry_run,
        )


@cli.command(name="backup")
@click.option(
    "-f",
    "--folder-uid",
    default=FOLDER_GENERAL,
    help="Optional folder UID to backup only this folder and its subfolders",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    help="Backup folders recursively",
)
@click.option(
    "-d",
    "--include-dashboards",
    is_flag=True,
    help="Include dashboards in the backup",
)
@click.option(
    "--backup-path",
    type=click.Path(),
    required=True,
    help="Path to store backup files",
)
@click.option(
    "--include-reports",
    is_flag=True,
    help="Include reports in the backup",
)
@click.pass_context
async def backup_folders(
    ctx: click.Context,
    folder_uid: str,
    recursive: bool,
    include_dashboards: bool,
    backup_path: str,
    include_reports: bool,
) -> None:
    """Backup folders and dashboards from Grafana instance to local storage."""
    grafana = ctx.ensure_object(GrafanaClient)
    backup = GrafanaBackup(grafana, backup_path)

    if folder_uid != FOLDER_GENERAL:
        # Backup the specified folder first
        await backup.backup_folder(folder_uid)

    if recursive:
        # Recursively backup from the specified folder
        await backup.backup_recursive(folder_uid, include_dashboards, include_reports)
    elif include_dashboards:
        # Non-recursive, just backup dashboards in the specified folder
        async for _, _, dashboards in grafana.walk(
            folder_uid,
            recursive=False,
            include_dashboards=True,
        ):
            for dashboard in dashboards.root:
                await backup.backup_dashboard(dashboard.uid)


@cli.command(
    name="generate",
    help="Generate random test folders and dashboards in Grafana instance.",
)
@click.option(
    "--num-folders",
    type=click.IntRange(min=0),
    default=5,
    help="Number of top-level folders to generate (min: 0)",
)
@click.option(
    "--max-subfolders",
    type=int,
    default=3,
    help="Maximum number of subfolders per folder",
)
@click.option(
    "--max-depth",
    type=int,
    default=2,
    help="Maximum folder nesting depth",
)
@click.option(
    "--max-dashboards",
    type=int,
    default=3,
    help="Maximum number of dashboards per folder",
)
@click.pass_context
async def generate_test_data(
    ctx: click.Context,
    num_folders: int,
    max_subfolders: int,
    max_depth: int,
    max_dashboards: int,
) -> None:
    try:
        grafana = ctx.ensure_object(GrafanaClient)
        await grafana.generate_test_data(
            num_folders=num_folders,
            max_subfolders=max_subfolders,
            max_depth=max_depth,
            max_dashboards=max_dashboards,
        )
        click.echo("Test data generation complete")
    except ImportError as ex:
        msg = (
            "Faker package is required for test data generation. "
            "Install it with: pip install 'grafana-sync[generate]'"
        )
        raise click.UsageError(msg) from ex


@cli.command(name="restore")
@click.option(
    "-f",
    "--folder-uid",
    help="Optional folder UID to restore only this folder",
)
@click.option(
    "-d",
    "--dashboard-uid",
    help="Optional dashboard UID to restore only this dashboard",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    help="Restore all folders and dashboards from backup",
)
@click.option(
    "--backup-path",
    type=click.Path(exists=True),
    required=True,
    help="Path to read backup files from",
)
@click.option(
    "--include-reports",
    is_flag=True,
    help="Include reports in the restore",
)
@click.pass_context
async def restore_folders(
    ctx: click.Context,
    folder_uid: str | None,
    dashboard_uid: str | None,
    recursive: bool,
    backup_path: str,
    include_reports: bool,
) -> None:
    """Restore folders and dashboards from local storage to Grafana instance."""
    grafana = ctx.ensure_object(GrafanaClient)
    restore = GrafanaRestore(grafana, backup_path)

    if recursive:
        await restore.restore_recursive(include_reports)
    elif folder_uid:
        await restore.restore_folder(folder_uid)
    elif dashboard_uid:
        await restore.restore_dashboard(dashboard_uid)
    else:
        msg = "Either --recursive, --folder-uid or --dashboard-uid must be specified"
        raise click.UsageError(msg)


@cli.command(name="logout-all")
@click.confirmation_option(
    prompt="Are you sure you want to logout all users?",
    help="This will invalidate all active sessions and force all users to login again",
)
@click.option(
    "--skip-username",
    help="Username to skip (e.g. current user)",
)
@click.pass_context
async def logout_all_users(ctx: click.Context, skip_username: str | None) -> None:
    """Logout all users from Grafana by invalidating all active sessions."""
    grafana = ctx.ensure_object(GrafanaClient)
    await grafana.logout_all_users(skip_username)
    click.echo("All users have been logged out")
