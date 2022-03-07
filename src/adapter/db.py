import functools

from src import domain

import sqlalchemy as sa

__all__ = ("fetch",)


@functools.cache
def create_engine(*, uri: str) -> sa.engine.Engine:
    engine = sa.create_engine(uri)
    return engine


def fetch(*, ds: domain.Datasource, sql: str) -> domain.Report:
    engine = create_engine(uri=ds.uri)

    with engine.connect() as con:
        result: sa.engine.CursorResult = con.execute(sa.text(sql))

        if key_map := result._metadata._keymap:  # noqa
            header = list(key_map.keys())
        else:
            header = []

        rows = [tuple(row._mapping.values()) for row in result]  # noqa

        return domain.Report(
            name=ds.name,
            header=header,
            rows=rows,
        )
