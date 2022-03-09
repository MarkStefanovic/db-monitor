import typing

__all__ = ("Worker",)


class Worker(typing.Protocol):
    def run(self) -> None:
        """Run the job"""
