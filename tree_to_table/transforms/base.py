from typing import Generic, TypeVar, Dict, Any, Iterable, Type

from tree_to_table.mappers import Mapper


class Transform:
    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        raise NotImplementedError

    def transform(
        self, mappers: Dict[str, Mapper], data: Dict[Any, Any]
    ) -> Dict[str, Any]:
        return {name: mapper(data) for name, mapper in mappers.items()}


class OneToOneTransform(Transform):
    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        for item in data:
            yield self.transform(mappers, item)


class OneToManyTransform(Transform):
    split_field: str

    def __init__(self, split_field: str, default_val=None):
        self.split_field = split_field
        self.default_val = default_val

    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        for item in data:
            splits = item.pop(self.split_field, [self.default_val])
            for split in splits:
                yield self.transform(mappers, {self.split_field: split, **item})
