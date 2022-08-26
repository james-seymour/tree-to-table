from typing import Mapping, Callable, Any
from .base import Mapper, identity


class Get(Mapper):
    def __init__(self, key: str, next=identity):
        self.key = key
        super().__init__(next)

    def run(self, obj: Mapping):
        return obj.get(self.key)


class GetDefault(Mapper):
    def __init__(self, key: str, default: Any, next=identity):
        self.key = key
        self.default = default
        super().__init__(next)

    def run(self, obj: Mapping):
        return obj.get(self.key, self.default)


class Apply(Mapper):
    def __init__(self, apply_fn: Callable, next=identity):
        self.apply_fn = apply_fn
        super().__init__(next)

    def run(self, obj: Any):
        return self.apply_fn(obj)


class Choice(Mapper):
    def __init__(self, chooser: Callable, next=identity):
        self.chooser = chooser
        super().__init__(next)

    def run(self, obj):
        if obj:
            return self.chooser(obj)
        return None


class Replace(Mapper):
    def __init__(self, replacement, next=identity) -> None:
        self.replacement = replacement
        super().__init__(next)

    def run(self, _):
        return self.replacement
