from typing import Mapping, Callable, Any, Dict, Optional
from .base import Mapper, identity, Source, Result, FinalResult


class Get(Mapper[Dict[str, Result], Result, FinalResult]):
    def __init__(self, key: str, next=identity):
        self.key = key
        super().__init__(next)

    def apply(self, obj: Dict[str, Result]) -> Optional[Result]:
        return obj.get(self.key)


class GetDefault(Mapper[Dict[str, Result], Result, FinalResult]):
    def __init__(self, key: str, default: Any, next=identity):
        self.key = key
        self.default = default
        super().__init__(next)

    def apply(self, obj: Mapping):
        return obj.get(self.key, self.default)


class Nested(Mapper[Source, Source, Dict[str, FinalResult]]):
    def __init__(self, nexts: Dict[str, Callable[[Source], FinalResult]]) -> None:
        self.nexts = nexts

    def apply(self, obj: Source) -> Source:
        return obj

    def __call__(self, obj) -> Dict[str, FinalResult]:
        return {key: mapper(obj) for key, mapper in self.nexts.items()}


class Apply(Mapper):
    def __init__(self, apply_fn: Callable, next=identity):
        self.apply_fn = apply_fn
        super().__init__(next)

    def apply(self, obj: Any):
        return self.apply_fn(obj)


class Choice(Mapper):
    def __init__(self, chooser: Callable, next=identity):
        self.chooser = chooser
        super().__init__(next)

    def apply(self, obj):
        if obj:
            return self.chooser(obj)
        return None


class Replace(Mapper):
    def __init__(self, replacement, next=identity) -> None:
        self.replacement = replacement
        super().__init__(next)

    def apply(self, _):
        return self.replacement
