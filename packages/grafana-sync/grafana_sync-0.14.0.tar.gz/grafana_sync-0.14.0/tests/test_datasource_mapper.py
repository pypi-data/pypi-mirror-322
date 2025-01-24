import importlib.resources

import pytest

from grafana_sync.api.models import GetDashboardResponse
from grafana_sync.dashboards.models import (
    DashboardData,
    DataSource,
    DSRef,
    Panel,
    Target,
    Templating,
    TemplatingItem,
    TemplatingItemCurrent,
)

from . import dashboards, responses


def read_db(filename: str) -> DashboardData:
    ref = importlib.resources.files(dashboards) / filename
    with importlib.resources.as_file(ref) as path, open(path, "rb") as f:
        return DashboardData.model_validate_json(f.read())


def read_response(filename: str) -> GetDashboardResponse:
    ref = importlib.resources.files(responses) / filename
    with importlib.resources.as_file(ref) as path, open(path, "rb") as f:
        return GetDashboardResponse.model_validate_json(f.read())


def test_ds_inheritance():
    db = DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource=DataSource(
                    type="influxdb",
                    uid="orig-uid",
                ),
                targets=[
                    Target(
                        datasource=DataSource(uid="${DataSource}"),
                    )
                ],
            )
        ],
    )

    db.update_datasources({"orig-uid": DSRef(uid="new-uid", name="InfluxDB")})

    assert db == DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource=DataSource(
                    type="influxdb",
                    uid="new-uid",
                ),
                targets=[
                    Target(
                        datasource=DataSource(uid="${DataSource}"),
                    )
                ],
            )
        ],
    )


@pytest.mark.parametrize(
    ("filename", "ct"),
    [
        ("haproxy-2-full.json", 0),
        ("host-overview.json", 0),
        ("simple-ds-var.json", 1),
        ("simple-novar.json", 2),
    ],
)
def test_update_datasources(filename, ct):
    db = read_db(filename)

    assert ct == db.update_datasources(
        {"P1809F7CD0C75ACF3": DSRef(uid="foobar", name="foobar")}
    )


@pytest.mark.parametrize(
    ("filename", "ct"),
    [
        ("get-dashboard-datasource-string.json", 1),
        ("get-dashboard-panel-target.json", 1),
    ],
)
def test_update_classic_datasource_from_response(filename, ct):
    res = read_response(filename)
    db = res.dashboard

    ds_config = {
        "InfluxDB Produktion Telegraf": DataSource(
            type="influxdb", uid="influxdb-prod-telegraf"
        )
    }

    db.upgrade_datasources(ds_config)

    assert ct == db.update_datasources(
        {
            "influxdb-prod-telegraf": DSRef(uid="foobar", name="foobar"),
            "influx": DSRef(uid="foobar", name="foobar"),
        }
    )


def test_upgrade_variable_template_datasource():
    db = DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource="$datasource",
                targets=[
                    Target(
                        expr="sum(up == 1)",
                        refId="A",
                    )
                ],
            )
        ],
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(
                        text="Old Prometheus", value="Old Prometheus"
                    ),
                    name="datasource",
                    query="prometheus",
                    type="datasource",
                ),
                TemplatingItem(
                    current=TemplatingItemCurrent(),
                    datasource="$datasource",
                    name="Cluster",
                    query="label_values(kube_pod_info,cluster)",
                    type="query",
                ),
            ]
        ),
    )

    db.upgrade_datasources(
        ds_config={"Old Prometheus": DataSource(type="prometheus", uid="old-uid")}
    )

    db.update_datasources(
        ds_map={"old-uid": DSRef(uid="new-uid", name="New Prometheus")}
    )

    assert db == DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource="$datasource",
                targets=[
                    Target(
                        expr="sum(up == 1)",
                        refId="A",
                    )
                ],
            )
        ],
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(
                        text="New Prometheus", value="new-uid"
                    ),
                    name="datasource",
                    query="prometheus",
                    type="datasource",
                ),
                TemplatingItem(
                    current=TemplatingItemCurrent(),
                    datasource="$datasource",
                    name="Cluster",
                    query="label_values(kube_pod_info,cluster)",
                    type="query",
                ),
            ]
        ),
    )


def test_upgrade_string_datasource():
    db = DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource="My InfluxDB",
                targets=[
                    Target(
                        dsType="influxdb",
                        refId="A",
                    )
                ],
            )
        ],
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(text="dev", value="dev"),
                    datasource="My InfluxDB",
                    label="Environment",
                    name="datasource",
                    query='SHOW TAG VALUES WITH KEY ="environment"',
                    type="query",
                ),
            ]
        ),
    )

    db.upgrade_datasources(
        ds_config={
            "My InfluxDB": DataSource(uid="influx", type="influxdb"),
        }
    )

    assert db == DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource=DataSource(type="influxdb", uid="influx"),
                targets=[
                    Target(
                        dsType="influxdb",
                        refId="A",
                    )
                ],
            )
        ],
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(text="dev", value="dev"),
                    datasource=DataSource(type="influxdb", uid="influx"),
                    label="Environment",
                    name="datasource",
                    query='SHOW TAG VALUES WITH KEY ="environment"',
                    type="query",
                ),
            ]
        ),
    )


def test_upgrade_nested_string_datasource():
    db = DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource="My InfluxDB",
                panels=[Panel(datasource="My InfluxDB")],
            )
        ],
    )

    db.upgrade_datasources(
        ds_config={
            "My InfluxDB": DataSource(uid="influx", type="influxdb"),
        }
    )

    assert db == DashboardData(
        uid="test",
        title="test",
        panels=[
            Panel(
                datasource=DataSource(type="influxdb", uid="influx"),
                panels=[Panel(datasource=DataSource(type="influxdb", uid="influx"))],
            )
        ],
    )


def test_map_template_query_datasource():
    db = DashboardData(
        uid="test",
        title="test",
        templating=Templating(
            list=[
                TemplatingItem(
                    datasource=DataSource(type="influxdb", uid="old-uid"),
                    name="Cluster",
                    query="label_values(kube_pod_info,cluster)",
                    type="query",
                ),
            ]
        ),
    )

    db.update_datasources(ds_map={"old-uid": DSRef(uid="new-uid", name="influxdb")})

    assert db == DashboardData(
        uid="test",
        title="test",
        templating=Templating(
            list=[
                TemplatingItem(
                    datasource=DataSource(type="influxdb", uid="new-uid"),
                    name="Cluster",
                    query="label_values(kube_pod_info,cluster)",
                    type="query",
                ),
            ]
        ),
    )


def test_map_template_datasource_name():
    db = DashboardData(
        uid="test",
        title="test",
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(
                        selected=False,
                        text="My Old Datasource",
                        value="My Old Datasource",
                    ),
                    name="datasource",
                    query="influxdb",
                    type="datasource",
                ),
            ]
        ),
    )

    db.upgrade_datasources(
        {"My Old Datasource": DataSource(uid="old-uid", type="influxdb")}
    )

    assert db == DashboardData(
        uid="test",
        title="test",
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(
                        selected=False,
                        text="My Old Datasource",
                        value="old-uid",
                    ),
                    name="datasource",
                    query="influxdb",
                    type="datasource",
                ),
            ]
        ),
    )

    db.update_datasources(
        ds_map={"old-uid": DSRef(uid="new-uid", name="My New Datasource")}
    )

    assert db == DashboardData(
        uid="test",
        title="test",
        templating=Templating(
            list=[
                TemplatingItem(
                    current=TemplatingItemCurrent(
                        selected=False,
                        text="My New Datasource",
                        value="new-uid",
                    ),
                    name="datasource",
                    query="influxdb",
                    type="datasource",
                ),
            ]
        ),
    )
