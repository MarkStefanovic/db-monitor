import dataclasses

__all__ = ("Datasource",)


@dataclasses.dataclass(frozen=True)
class Datasource:
    name: str
    uri: str

    def __str__(self) -> str:
        return f"Datasource [ name: {self.name} ]"
