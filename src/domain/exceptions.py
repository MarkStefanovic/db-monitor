__all__ = ("InvalidJobSpecException",)

import pathlib


class DbMonitorException(Exception):
    """Base class for exceptions from db-monitor"""


class FileDoesNotExist(DbMonitorException):
    def __init__(self, *, path: pathlib.Path):
        super().__init__(f"The path, {path.resolve()!s} does not exist.")


class InvalidConfigurationSetting(DbMonitorException):
    def __init__(self, *, message: str):
        super().__init__(message)


class InvalidJobSpecException(DbMonitorException):
    def __init__(self, *, message: str):
        super().__init__(message)
