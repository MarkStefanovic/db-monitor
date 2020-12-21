import abc

import pydantic

__all__ = ("Datasource",)


class Datasource(pydantic.BaseModel, abc.ABC):
    name: str
    uri: str

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
