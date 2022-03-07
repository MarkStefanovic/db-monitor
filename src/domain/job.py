import dataclasses

__all__ = ("Job",)

from src.domain import exceptions


@dataclasses.dataclass(frozen=True)
class Job:
    report_name: str
    sql_file: str
    datasource_name: str
    seconds_between_refreshes: int
    height: int

    def __post_init__(self) -> None:
        if not self.report_name:
            raise exceptions.InvalidJobSpecException(
                message=f"report_name must be >= 0, but got {self.report_name!r}."
            )

        if not self.sql_file:
            raise exceptions.InvalidJobSpecException(
                message=f"sql_file must be >= 0, but got {self.sql_file!r}."
            )

        if not self.datasource_name:
            raise exceptions.InvalidJobSpecException(
                message=f"datasource_name must be >= 0, but got {self.datasource_name!r}."
            )

        if not self.seconds_between_refreshes > 0:
            raise exceptions.InvalidJobSpecException(
                message=f"seconds_between_refreshes must be >= 0, but got {self.seconds_between_refreshes!r}."
            )

        if not self.height > 0:
            raise exceptions.InvalidJobSpecException(
                message=f"height must be >= 0, but got {self.height!r}."
            )
