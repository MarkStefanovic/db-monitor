import pathlib


__all__ = ("read",)


def read(file_path: pathlib.Path) -> str:
    with file_path.open("r") as fh:
        lines = fh.readlines()
        sql = " ".join(lines)
        return " ".join(sql.split())
