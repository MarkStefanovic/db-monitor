import dataclasses
import typing

__all__ = ("Report",)


@dataclasses.dataclass(frozen=True)
class Report:
    name: str
    header: list[str]
    rows: list[tuple[typing.Any, ...]]
