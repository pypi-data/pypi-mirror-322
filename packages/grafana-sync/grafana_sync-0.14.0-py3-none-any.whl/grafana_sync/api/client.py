import logging
import os
import random
import ssl
from collections.abc import AsyncGenerator
from typing import Self
from urllib.parse import urlparse

import certifi
import httpx
from httpx import Response

from grafana_sync.api.models import (
    CreateDatasourceResponse,
    CreateFolderResponse,
    CreateReportResponse,
    DashboardData,
    DatasourceDefinition,
    GetDashboardResponse,
    GetDatasourcesResponse,
    GetFolderResponse,
    GetFoldersResponse,
    GetReportResponse,
    GetReportsResponse,
    SearchDashboardsResponse,
    UpdateDashboardRequest,
    UpdateDashboardResponse,
    UpdateFolderResponse,
)
from grafana_sync.exceptions import (
    ExistingDashboardsError,
    ExistingDatasourcesError,
    ExistingFoldersError,
    GrafanaApiError,
)

logger = logging.getLogger(__name__)

# reserved Grafana folder name for the top-level directory
FOLDER_GENERAL = "general"

# virtual folder
FOLDER_SHAREDWITHME = "sharedwithme"


class GrafanaClient:
    def __init__(
        self,
        url: str,
        api_key: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Create a Grafana API client from connection parameters."""
        self.url = url
        self.api_key = api_key
        parsed_url = urlparse(url)
        logging.debug("Parsing URL: %s", url)
        host = parsed_url.hostname or "localhost"
        protocol = parsed_url.scheme or "https"
        port = parsed_url.port

        # Extract credentials from URL if present
        if parsed_url.username and parsed_url.password and not (username or password):
            username = parsed_url.username
            password = parsed_url.password

        self.username = username
        self.password = password

        if api_key:
            auth = (api_key, "")
        elif username and password:
            auth = (username, password)
        else:
            msg = "Either --api-key or both --username and --password must be provided (via parameters or URL)"
            raise ValueError(msg)

        # Construct base URL
        base_url = f"{protocol}://{host}"
        if port:
            base_url = f"{base_url}:{port}"

        url_path_prefix = parsed_url.path.strip("/")
        if url_path_prefix:
            base_url = f"{base_url}/{url_path_prefix}"

        # Create SSL context using environment variables or certifi
        ssl_context = ssl.create_default_context(
            cafile=os.getenv("REQUESTS_CA_BUNDLE")
            or os.getenv("SSL_CERT_FILE")
            or certifi.where(),
            capath=os.getenv("SSL_CERT_DIR"),
        )

        self.client = httpx.AsyncClient(
            base_url=base_url,
            auth=auth,
            headers={"Content-Type": "application/json"},
            follow_redirects=True,
            verify=ssl_context,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.client.aclose()

    def _log_request(self, response: Response) -> None:
        """Log request and response details at debug level."""
        logger.debug(
            "HTTP %s %s\nHeaders: %s\nRequest Body: %s\nResponse Status: %d\nResponse Body: %s",
            response.request.method,
            response.request.url,
            response.request.headers,
            response.request.content.decode() if response.request.content else "None",
            response.status_code,
            response.text,
        )

    def _handle_error(self, response: Response) -> None:
        """Handle error responses from Grafana API.

        Args:
            response: The HTTP response to check

        Raises:
            GrafanaApiError: If the response indicates an error
        """
        self._log_request(response)
        if response.is_error:
            raise GrafanaApiError(response)

    async def create_folder(
        self, title: str, uid: str | None = None, parent_uid: str | None = None
    ) -> CreateFolderResponse:
        """Create a new folder in Grafana.

        Args:
            title: The title of the folder
            uid: Optional unique identifier. Will be auto-generated if not provided
            parent_uid: Optional parent folder UID for nested folders

        Returns:
            CreateFolderResponse: The created folder details

        Raises:
            HTTPError: If the request fails
        """
        data = {"title": title}
        if uid:
            data["uid"] = uid
        if parent_uid:
            data["parentUid"] = parent_uid

        response = await self.client.post("/api/folders", json=data)
        self._handle_error(response)
        return CreateFolderResponse.model_validate_json(response.content)

    async def delete_folder(self, uid: str) -> None:
        """Delete a folder in Grafana.

        Args:
            uid: The unique identifier of the folder to delete

        Raises:
            HTTPError: If the request fails
        """
        response = await self.client.delete(f"/api/folders/{uid}")
        self._handle_error(response)

    async def get_folders(self, parent_uid: str | None = None) -> GetFoldersResponse:
        """Get all folders in Grafana, optionally filtered by parent UID.

        Args:
            parent_uid: Optional parent folder UID to filter by

        Returns:
            GetFoldersResponse: List of folders

        Raises:
            GrafanaApiError: If the request fails
        """
        params = {}
        if parent_uid and parent_uid != FOLDER_GENERAL:
            params["parentUid"] = parent_uid

        response = await self.client.get("/api/folders", params=params)
        self._handle_error(response)
        return GetFoldersResponse.model_validate_json(response.content)

    async def get_folder(self, uid: str) -> GetFolderResponse:
        """Get a specific folder by UID.

        Args:
            uid: The unique identifier of the folder

        Returns:
            GetFolderResponse: The folder details

        Raises:
            GrafanaApiError: If the request fails or folder doesn't exist
        """
        response = await self.client.get(f"/api/folders/{uid}")
        self._handle_error(response)
        return GetFolderResponse.model_validate_json(response.content)

    async def update_folder(
        self,
        uid: str,
        title: str,
        version: int | None = None,
        parent_uid: str | None = None,
        overwrite: bool = False,
    ) -> UpdateFolderResponse:
        """Update a folder in Grafana.

        Args:
            uid: The unique identifier of the folder to update
            title: The new title for the folder
            version: Current version of the folder (required unless overwrite=True)
            parent_uid: Optional new parent folder UID
            overwrite: Whether to overwrite existing folder with same name

        Returns:
            UpdateFolderResponse: The updated folder details

        Raises:
            GrafanaApiError: If the request fails
            ValueError: If version is not provided and overwrite is False
        """
        if not overwrite and version is None:
            msg = "version must be provided when overwrite=False"
            raise ValueError(msg)

        data = {
            "title": title,
            "overwrite": overwrite,
        }
        if not overwrite:
            data["version"] = version
        if parent_uid:
            data["parentUid"] = parent_uid

        response = await self.client.put(f"/api/folders/{uid}", json=data)
        self._handle_error(response)
        return UpdateFolderResponse.model_validate_json(response.content)

    async def move_folder(self, uid: str, new_parent_uid: str | None = None) -> None:
        """Move a folder to a new parent folder.

        Args:
            uid: The unique identifier of the folder to move
            new_parent_uid: The UID of the new parent folder, or None for root

        Returns:
            UpdateFolderResponse: The updated folder details

        Raises:
            GrafanaApiError: If the request fails
        """
        # Update folder with new parent
        response = await self.client.post(
            f"/api/folders/{uid}/move", json={"parentUid": new_parent_uid}
        )
        self._handle_error(response)

    async def search_dashboards(
        self,
        folder_uids: list[str] | None = None,
        query: str | None = None,
        tag: list[str] | None = None,
        type_: str = "dash-db",
    ) -> SearchDashboardsResponse:
        """Search for dashboards in Grafana.

        Args:
            folder_uids: Optional list of folder UIDs to search in
            query: Optional search query string
            tag: Optional list of tags to filter by
            type_: Type of dashboard to search for (default: dash-db)

        Returns:
            SearchDashboardsResponse: List of matching dashboards

        Raises:
            GrafanaApiError: If the request fails
        """
        params: dict = {"type": type_}

        if folder_uids:
            params["folderUIDs"] = ",".join(folder_uids)
        if query:
            params["query"] = query
        if tag:
            params["tag"] = tag

        response = await self.client.get("/api/search", params=params)
        self._handle_error(response)
        return SearchDashboardsResponse.model_validate_json(response.content)

    async def update_dashboard(
        self, dashboard_data: DashboardData, folder_uid: str | None = None
    ) -> UpdateDashboardResponse:
        """Update or create a dashboard in Grafana.

        Args:
            dashboard_data: The complete dashboard model (must include uid)
            folder_uid: Optional folder UID to move dashboard to

        Returns:
            UpdateDashboardResponse: The updated dashboard details

        Raises:
            GrafanaApiError: If the request fails
        """
        # Prepare the dashboard update payload
        payload = UpdateDashboardRequest(
            dashboard=dashboard_data,
            message="Dashboard updated via API",
            overwrite=True,
            folderUid=None if folder_uid == FOLDER_GENERAL else folder_uid,
        )

        response = await self.client.post(
            "/api/dashboards/db",
            json=payload.model_dump(exclude={"dashboard": {"id"}}, by_alias=True),
        )
        self._handle_error(response)
        return UpdateDashboardResponse.model_validate_json(response.content)

    async def delete_dashboard(self, uid: str) -> None:
        """Delete a dashboard in Grafana.

        Args:
            uid: The unique identifier of the dashboard to delete

        Raises:
            GrafanaApiError: If the request fails
        """
        response = await self.client.delete(f"/api/dashboards/uid/{uid}")
        self._handle_error(response)

    async def get_dashboard(self, uid: str) -> GetDashboardResponse:
        """Get a dashboard by its UID.

        Args:
            uid: The unique identifier of the dashboard

        Returns:
            GetDashboardResponse: The dashboard details including meta information

        Raises:
            GrafanaApiError: If the request fails or dashboard doesn't exist
        """
        response = await self.client.get(f"/api/dashboards/uid/{uid}")
        self._handle_error(response)
        return GetDashboardResponse.model_validate_json(response.content)

    async def get_datasources(self) -> GetDatasourcesResponse:
        response = await self.client.get("/api/datasources")
        self._handle_error(response)
        return GetDatasourcesResponse.model_validate_json(response.content)

    async def create_datasource(
        self, ds: DatasourceDefinition
    ) -> CreateDatasourceResponse:
        response = await self.client.post(
            "/api/datasources", json=ds.model_dump(by_alias=True)
        )
        self._handle_error(response)
        return CreateDatasourceResponse.model_validate_json(response.content)

    async def delete_datasource(self, uid: str) -> None:
        """Delete a datasource in Grafana."""
        response = await self.client.delete(f"/api/datasources/uid/{uid}")
        self._handle_error(response)

    async def get_reports(self) -> GetReportsResponse:
        """Get all reports.

        Returns:
            GetReportsResponse: List of reports

        Raises:
            GrafanaApiError: If the request fails
        """
        response = await self.client.get("/api/reports")
        self._handle_error(response)
        return GetReportsResponse.model_validate_json(response.content)

    async def get_report(self, report_id: int) -> GetReportResponse:
        """Get a report by its ID.

        Args:
            report_id: The unique identifier of the report

        Returns:
            GetReportResponse: The report details

        Raises:
            GrafanaApiError: If the request fails
        """
        response = await self.client.get(f"/api/reports/{report_id}")
        self._handle_error(response)
        return GetReportResponse.model_validate_json(response.content)

    async def create_report(self, report: GetReportResponse) -> CreateReportResponse:
        """Create a new report.

        Args:
            report: The report data

        Returns:
            CreateReportResponse: The created report

        Raises:
            GrafanaApiError: If the request fails
        """
        response = await self.client.post(
            "/api/reports", json=report.model_dump(exclude={"id"}, by_alias=True)
        )
        self._handle_error(response)
        return CreateReportResponse.model_validate_json(response.content)

    async def delete_report(self, report_id: int) -> None:
        """Delete a report.

        Args:
            report_id: The unique identifier of the report

        Raises:
            GrafanaApiError: If the request fails
        """
        response = await self.client.delete(f"/api/reports/{report_id}")
        self._handle_error(response)

    async def logout_all_users(self, skip_username: str | None = None) -> None:
        """Logout all users from Grafana by invalidating their sessions.

        This fetches all users and logs each one out individually.

        Args:
            skip_username: Optional username to skip (e.g. current user)

        Raises:
            GrafanaApiError: If the request fails or user doesn't have admin privileges
        """
        # Get all users
        response = await self.client.get("/api/users")
        self._handle_error(response)
        users = response.json()

        # Logout each user individually
        for user in users:
            if skip_username and user["login"] == skip_username:
                continue
            user_id = user["id"]
            response = await self.client.post(f"/api/admin/users/{user_id}/logout")
            self._handle_error(response)

    async def walk(
        self,
        folder_uid: str = FOLDER_GENERAL,
        recursive: bool = False,
        include_dashboards: bool = True,
    ) -> AsyncGenerator[tuple[str, GetFoldersResponse, SearchDashboardsResponse], None]:
        """Walk through Grafana folder structure, similar to os.walk.

        Args:
            folder_uid: The folder UID to start walking from (default: "general")
            recursive: Whether to recursively walk through subfolders
            include_dashboards: Whether to include dashboards in the results

        Yields:
            Tuple of (folder_uid, subfolders, dashboards)
        """
        logger.debug("fetching folders for folder_uid %s", folder_uid)
        subfolders = await self.get_folders(parent_uid=folder_uid)

        if include_dashboards:
            logger.debug("searching dashboards for folder_uid %s", folder_uid)
            dashboards = await self.search_dashboards(
                folder_uids=[folder_uid],
                type_="dash-db",
            )
        else:
            dashboards = SearchDashboardsResponse(root=[])

        yield folder_uid, subfolders, dashboards

        if recursive:
            for folder in subfolders.root:
                async for res in self.walk(folder.uid, recursive, include_dashboards):
                    yield res

    async def generate_test_data(
        self,
        num_folders: int = 5,
        max_subfolders: int = 3,
        max_depth: int = 2,
        max_dashboards: int = 3,
    ) -> None:
        """Generate random test folders and dashboards.

        Args:
            num_folders: Number of top-level folders to create
            max_subfolders: Maximum number of subfolders per folder
            max_depth: Maximum folder nesting depth
            max_dashboards: Maximum number of dashboards per folder
        """
        from faker import Faker

        fake = Faker()

        async def create_folder_tree(depth: int, parent_uid: str | None = None) -> None:
            if depth > max_depth:
                return

            # Create random number of folders at this level
            num_subfolders = random.randint(0, max_subfolders)
            for _ in range(num_subfolders):
                title = fake.unique.company()
                folder = await self.create_folder(title=title, parent_uid=parent_uid)

                # Create random dashboards in this folder
                num_dash = random.randint(0, max_dashboards)
                for _ in range(num_dash):
                    dash_title = fake.catch_phrase()
                    dashboard = {
                        "uid": fake.unique.uuid4(),
                        "title": dash_title,
                        "tags": [fake.word() for _ in range(random.randint(0, 3))],
                        "timezone": "browser",
                        "panels": [],
                        "version": 1,
                    }
                    await self.update_dashboard(
                        DashboardData.model_validate(dashboard), folder_uid=folder.uid
                    )

                # Recursively create subfolders
                await create_folder_tree(depth + 1, folder.uid)

        # Create top-level folders
        for _ in range(num_folders):
            await create_folder_tree(0, None)

    async def check_pristine(self) -> None:
        datasources = (await self.get_datasources()).root
        if len(datasources) > 0:
            raise ExistingDatasourcesError(len(datasources))

        folders = (await self.get_folders()).root
        if len(folders) > 0:
            raise ExistingFoldersError(len(folders))

        # Check for dashboards in the general folder
        dashboards = (await self.search_dashboards()).root
        if len(dashboards) > 0:
            raise ExistingDashboardsError(len(dashboards))

    async def delete_all_folders_and_dashboards_and_datasources(self) -> None:
        """Delete all dashboards, folders and datasources in the Grafana instance.

        Dashboards are deleted first, then folders, since folders cannot be deleted
        while containing dashboards. Then datasources are deleted.
        """
        # First delete all dashboards
        dashboards = (await self.search_dashboards()).root
        for dashboard in dashboards:
            logger.debug("Deleting dashboard %s", dashboard.uid)
            await self.delete_dashboard(dashboard.uid)

        # Then delete all folders
        folders = (await self.get_folders()).root
        for folder in folders:
            logger.debug("Deleting folder %s", folder.uid)
            await self.delete_folder(folder.uid)

        datasources = (await self.get_datasources()).root
        for ds in datasources:
            logger.debug("Deleting datasource %s", ds.uid)
            await self.delete_datasource(ds.uid)
