import typing

import pydantic

__all__ = ("Report",)


class Report(pydantic.BaseModel):
    name: str
    header: typing.List[str]
    rows: typing.List[typing.List[typing.Any]]

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
