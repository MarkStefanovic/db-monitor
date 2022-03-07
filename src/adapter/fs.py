import functools
import os
import pathlib
import sys

__all__ = ("get_config_path", "get_icons_folder", "get_log_dir", "get_sql_folder",)


@functools.lru_cache
def get_root_dir() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        return pathlib.Path(getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))))
        # return pathlib.Path(os.path.dirname(sys.executable))
    else:
        path = pathlib.Path(sys.argv[0]).parent.parent
        assert path.name == "db-monitor", f"Expected the parent folder to be named db-monitor, but the path was {path.resolve()!s}."
        return path


@functools.lru_cache
def get_config_path() -> pathlib.Path:
    return _check_exists(get_root_dir() / "assets" / "config.json")


@functools.lru_cache
def get_icons_folder() -> pathlib.Path:
    return _check_exists(get_root_dir() / "assets" / "icons")


@functools.lru_cache
def get_log_dir() -> pathlib.Path:
    fp = get_root_dir() / "log"
    fp.mkdir(exist_ok=True)
    return fp


@functools.lru_cache
def get_sql_folder() -> pathlib.Path:
    return _check_exists(get_root_dir() / "assets" / "sql")


def _check_exists(fp: pathlib.Path) -> pathlib.Path:
    assert fp.exists(), f"{fp!s} does not exist."
    return fp


def read_sql_file(file_path: pathlib.Path) -> str:
    with file_path.open("r") as fh:
        lines = fh.readlines()
        sql = " ".join(lines)
        return " ".join(sql.split())
