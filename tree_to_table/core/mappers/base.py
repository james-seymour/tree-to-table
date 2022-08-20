from typing import TypeVar, Protocol

T = TypeVar("T")

ProtocolSource = TypeVar("ProtocolSource", contravariant=True)
ProtocolResult = TypeVar("ProtocolResult", covariant=True)


class MapperProtocol(Protocol[ProtocolSource, ProtocolResult]):
    def apply(self, obj: ProtocolSource) -> ProtocolResult:
        ...


class Mapper:
    def __init__(self, next) -> None:
        self.next = next

    def run(self, obj):
        ...

    def __call__(self, obj):
        value = self.run(obj)
        if value is None:
            return None
        return self.next(value)


def identity(obj: T) -> T:
    return obj
