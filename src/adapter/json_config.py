import json
import typing

import pydantic

from src import domain

__all__ = ("load", "save")


class PyodbcConfig(domain.Config):
    datasources: typing.List[domain.Datasource]


@pydantic.validate_arguments
def load(filepath: pydantic.FilePath) -> PyodbcConfig:
    return PyodbcConfig.parse_file(filepath, content_type="json")


@pydantic.validate_arguments
def save(config: domain.Config, filepath: pydantic.FilePath) -> None:
    json_data = config.json(indent=2)
    with open(filepath, "w") as fh:
        json.dump(json_data, fh)
