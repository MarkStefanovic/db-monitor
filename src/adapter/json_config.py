import json
import pathlib
import typing

from src import domain

__all__ = ("load", "PyodbcConfig",)


class PyodbcConfig(domain.Config):
    datasources: typing.List[domain.Datasource]


def load(*, path: pathlib.Path) -> PyodbcConfig:
    with path.open("r") as fh:
        data = json.load(fh)

        datasources = [domain.Datasource(**ds) for ds in data["datasources"]]

        jobs = [domain.Job(**ds) for ds in data["jobs"]]

        return PyodbcConfig(
            datasources=datasources,
            jobs=jobs,
            reports_per_row=data["reports_per_row"],
        )
