from collections.abc import Generator, Mapping

from pydantic import BaseModel, ConfigDict, Field

from grafana_sync.exceptions import UnmappedDatasourceError


class DSRef(BaseModel):
    uid: str
    name: str


class DataSource(BaseModel):
    type_: str | None = Field(alias="type", default=None)
    uid: str

    model_config = ConfigDict(extra="allow")

    @property
    def is_variable(self):
        return self.uid.startswith("${") and self.uid.endswith("}")

    def update(self, ds_map: Mapping[str, DSRef], strict=False) -> bool:
        if self.is_variable:
            return False

        if self.uid not in ds_map:
            if strict:
                raise UnmappedDatasourceError(self.uid)
            return False

        self.uid = ds_map[self.uid].uid
        return True


class Target(BaseModel):
    expr: str | None = None
    ref_id: str | None = Field(alias="refId", default=None)
    datasource: DataSource | None = None
    ds_type: str | None = Field(alias="dsType", default=None)

    model_config = ConfigDict(extra="allow")

    @property
    def all_datasources(self) -> Generator[DataSource, None, None]:
        if self.datasource is not None:
            yield self.datasource


class Panel(BaseModel):
    datasource: DataSource | str | None = None
    targets: list[Target] | None = None
    panels: list["Panel"] | None = None

    model_config = ConfigDict(extra="allow")

    @property
    def has_variable_datasource(self) -> bool:
        return isinstance(self.datasource, str) and self.datasource.startswith("$")

    @property
    def all_datasources(self) -> Generator[DataSource, None, None]:
        if self.datasource is not None:
            if isinstance(self.datasource, str):
                if not self.has_variable_datasource:
                    msg = f"please run upgrade_datasource to resolve datasource `{self.datasource}`"
                    raise ValueError(msg)
            else:
                yield self.datasource

        if self.targets is not None:
            for t in self.targets:
                yield from t.all_datasources

        if self.panels is not None:
            for p in self.panels:
                yield from p.all_datasources

    def upgrade_datasource(self, ds_config: Mapping[str, DataSource]) -> None:
        """Upgrade string-datasource into an datasource object.

        Older Grafana versions used to put a string (name) into the datasource field.
        """
        if isinstance(self.datasource, str) and not self.has_variable_datasource:
            self.datasource = ds_config[self.datasource]

        if self.panels is not None:
            for p in self.panels:
                p.upgrade_datasource(ds_config)

    def update_datasources(
        self,
        ds_map: Mapping[str, DSRef],
        strict=False,
    ) -> int:
        ct = 0

        for ds in self.all_datasources:
            if ds.update(ds_map, strict):
                ct += 1

        return ct


class TemplatingItemCurrent(BaseModel):
    text: str | list[str] | None = None
    value: str | list[str] | None = None
    selected: bool | None = None

    model_config = ConfigDict(extra="allow")

    def upgrade_datasource(self, ds_config: Mapping[str, DataSource]) -> None:
        if not isinstance(self.text, str):
            return

        if not isinstance(self.value, str):
            return

        if ds := ds_config.get(self.value, None):
            self.value = ds.uid

    def update_datasource(self, ds_map: Mapping[str, DSRef], strict=False) -> bool:
        if not isinstance(self.text, str):
            return False

        if not isinstance(self.value, str):
            return False

        if self.value not in ds_map:
            if strict:
                raise UnmappedDatasourceError(self.value)
            return False

        self.text = ds_map[self.value].name
        self.value = ds_map[self.value].uid

        return True


class TemplatingItemQuery(BaseModel):
    model_config = ConfigDict(extra="allow")


class TemplatingItem(BaseModel):
    current: TemplatingItemCurrent | None = None
    name: str | None = None
    label: str | None = None
    query: str | TemplatingItemQuery | None = None
    datasource: DataSource | str | None = None
    type_: str = Field(alias="type")

    model_config = ConfigDict(extra="allow")

    @property
    def all_datasources(self) -> Generator[DataSource, None, None]:
        if self.datasource is not None and isinstance(self.datasource, DataSource):
            yield self.datasource

    @property
    def has_variable_datasource(self) -> bool:
        return isinstance(self.datasource, str) and self.datasource.startswith("$")

    def upgrade_datasources(self, ds_config: Mapping[str, DataSource]) -> None:
        if self.type_ == "datasource" and self.current is not None:
            self.current.upgrade_datasource(ds_config)

        if (
            self.type_ == "query"
            and self.datasource is not None
            and isinstance(self.datasource, str)
            and not self.has_variable_datasource
        ):
            self.datasource = ds_config[self.datasource]

    def update_datasources(self, ds_map: Mapping[str, DSRef], strict=False) -> int:
        ct = 0

        if (
            self.type_ == "datasource"
            and self.current is not None
            and self.current.update_datasource(ds_map, strict)
        ):
            ct += 1

        if (
            self.type_ == "query"
            and self.datasource is not None
            and isinstance(self.datasource, DataSource)
            and self.datasource.update(ds_map, strict)
        ):
            ct += 1

        return ct


class Templating(BaseModel):
    list_: list[TemplatingItem] | None = Field(alias="list", default=None)

    model_config = ConfigDict(extra="allow")

    @property
    def all_datasources(self) -> Generator[DataSource, None, None]:
        if self.list_ is not None:
            for t in self.list_:
                yield from t.all_datasources

    def upgrade_datasources(self, ds_config: Mapping[str, DataSource]) -> None:
        """Upgrade string-datasource into an datasource object.

        Older Grafana versions used to put a string (name) into the datasource field.
        """
        if self.list_ is None:
            return

        for t in self.list_:
            t.upgrade_datasources(ds_config)

    def update_datasources(self, ds_map: Mapping[str, DSRef], strict=False) -> int:
        if self.list_ is None:
            return 0

        ct = 0

        for t in self.list_:
            ct += t.update_datasources(ds_map, strict)

        return ct


class DashboardData(BaseModel):
    uid: str
    title: str
    version: int | None = None

    panels: list[Panel] | None = None
    templating: Templating | None = None

    model_config = ConfigDict(extra="allow")

    @property
    def all_datasources(self) -> Generator[DataSource, None, None]:
        if self.panels is not None:
            for p in self.panels:
                yield from p.all_datasources

        if self.templating is not None:
            yield from self.templating.all_datasources

    @property
    def datasource_count(self) -> int:
        return len(list(self.all_datasources))

    @property
    def variable_datasource_count(self) -> int:
        return len([ds for ds in self.all_datasources if ds.is_variable])

    def upgrade_datasources(self, ds_config: Mapping[str, DataSource]) -> None:
        if self.panels is not None:
            for p in self.panels:
                p.upgrade_datasource(ds_config)

        if self.templating is not None:
            self.templating.upgrade_datasources(ds_config)

    def update_datasources(
        self,
        ds_map: Mapping[str, DSRef],
        strict=False,
    ) -> int:
        ct = 0

        if self.panels is not None:
            for p in self.panels:
                ct += p.update_datasources(ds_map, strict)

        if self.templating is not None:
            ct += self.templating.update_datasources(ds_map, strict)

        return ct
