__all__ = ("InvalidJobSpecException",)


class DbMonitorException(Exception):
    """Base class for exceptions from db-monitor"""


class InvalidJobSpecException(Exception):
    def __init__(self, *, message: str):
        super().__init__(message)
