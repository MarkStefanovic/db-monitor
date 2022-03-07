import dataclasses

from src.domain import datasource, job

__all__ = ("Config",)


@dataclasses.dataclass(frozen=True)
class Config:
    datasources: list[datasource.Datasource]
    jobs: list[job.Job]
    reports_per_row: int

    def __post_init__(self) -> None:
        assert self.reports_per_row > 0, f"reports_per_row must be > 0, but got {self.reports_per_row!r}."
