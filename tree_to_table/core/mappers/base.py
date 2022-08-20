from typing import TypeVar, Protocol

T = TypeVar("T")

ProtocolSource = TypeVar("ProtocolSource", contravariant=True)
ProtocolResult = TypeVar("ProtocolResult", covariant=True)


class MapperProtocol(Protocol[ProtocolSource, ProtocolResult]):
    def apply(self, obj: ProtocolSource) -> ProtocolResult:
        ...
