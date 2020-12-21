import typing

import pydantic

from src.domain import datasource, job

__all__ = ("Config",)


class Config(pydantic.BaseModel):
    log_dir: pydantic.DirectoryPath
    datasources: typing.List[datasource.Datasource]
    jobs: typing.List[job.Job]
    reports_per_row: pydantic.PositiveInt
