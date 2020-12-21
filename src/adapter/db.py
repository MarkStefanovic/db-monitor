import pyodbc

from src import domain

__all__ = ("fetch",)


def fetch(ds: domain.Datasource, sql: str) -> domain.Report:
    with pyodbc.connect(ds.uri) as con:
        with con.cursor() as cur:
            rows = [list(row) for row in cur.execute(sql).fetchall()]
            header = [col[0] for col in cur.description]
            return domain.Report(name=ds.name, header=header, rows=rows)
