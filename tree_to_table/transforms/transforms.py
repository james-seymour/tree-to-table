from typing import Dict, Iterable, Any

from .base import Transform
from ..mappers import Mapper


class OneToOneTransform(Transform):
    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        for item in data:
            yield self.transform(mappers, item)


class OneToManyTransform(Transform):
    def __init__(
        self,
        split_mappers: Dict[str, Mapper],
        default_val=None,
        keep_splits=True,
    ):
        self.split_mappers = split_mappers
        self.default_val = default_val
        self.keep_splits = keep_splits

    def __call__(
        self,
        mappers: Dict[str, Mapper],
        data: Iterable[Dict[Any, Any]],
    ) -> Iterable[Dict[Any, Any]]:
        splits = [self.transform(self.split_mappers, item) for item in data]

        for split, row in zip(splits, data):
            # TODO: I dont think this preserves order here in some cases
            # We are assuming split === dict(zip(split.keys(), split.values())), which I dont think is correct
            for x in zip(*split.values()):
                transformed = self.transform(mappers, row)

                if self.keep_splits:
                    split_dict = dict(zip(split.keys(), x))
                    yield {**split_dict, **transformed}
                else:
                    yield transformed
