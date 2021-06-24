import pydantic

__all__ = ("Job",)


class Job(pydantic.BaseModel):
    report_name: str
    sql_file: str
    datasource_name: str
    seconds_between_refreshes: pydantic.PositiveInt
    height: int

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1


