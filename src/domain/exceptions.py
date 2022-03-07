__all__ = ("InvalidJobSpecException",)


class DbMonitorException(Exception):
    """Base class for exceptions from db-monitor"""


class InvalidConfigurationSetting(DbMonitorException):
    def __init__(self, *, message: str):
        super().__init__(message)


class InvalidJobSpecException(DbMonitorException):
    def __init__(self, *, message: str):
        super().__init__(message)
