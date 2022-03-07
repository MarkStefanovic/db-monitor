import dataclasses

from src.domain import datasource, exceptions, job

__all__ = ("Config",)


@dataclasses.dataclass(frozen=True)
class Config:
    datasources: list[datasource.Datasource]
    jobs: list[job.Job]
    reports_per_row: int

    def __post_init__(self) -> None:
        if len(self.datasources) == 0:
            raise exceptions.InvalidConfigurationSetting(
                message=f"At least 1 datasource must be provided in config.json."
            )

        if len(self.jobs) == 0:
            raise exceptions.InvalidConfigurationSetting(
                message=f"At least 1 job must be provided in config.json."
            )

        if not self.reports_per_row > 0:
            raise exceptions.InvalidConfigurationSetting(
                message=f"reports_per_row must be > 0, but got {self.reports_per_row!r}."
            )
