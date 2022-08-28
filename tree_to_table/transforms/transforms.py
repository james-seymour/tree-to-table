from typing import Dict, Iterable, Any, Callable, Mapping, Tuple

from .base import Transform
from ..mappers import Mapper


class OneToOneTransform(Transform):
    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        if not isinstance(data, Iterable):
            raise TypeError(
                "Cannot transform a non-iterable set of data. If only one row is required to transform, wrap it with a list"
            )

        for item_i, item in enumerate(data):
            if not isinstance(item, Mapping):
                raise TypeError(
                    f"Cannot transform row '{item}' at index {item_i} as it is not a Mapping"
                )

            yield self.transform(mappers, item)


class OneToManyTransform(Transform):
    def __init__(self, *split_mappers: Mapper, split_method=zip):
        self.split_mappers = split_mappers
        self.split_method = zip  # TODO: Get other split_methods working (itertools.zip_longest, itertools.product)

    def generate_split_mappers_dict(self, mappers: Dict[str, Mapper]):
        """Goal here is to nameify the split_mappers given

        The logic here is that if a split_mapper exists in the mappers then it should be kept after transform
        If not, then it still should be used to split one-to-many, but we don't need to keep the key in the transformed data
        """

        def get_mapper_name(split_mapper):
            for mapper_name, mapper in mappers.items():
                if split_mapper == mapper:
                    return mapper_name

            return str(hash(split_mapper))  # Default to using this mapper's unique hash

        # TODO: Definitely some performance optimisation here
        split_mappers_dict = {
            get_mapper_name(split_mapper): split_mapper
            for split_mapper in self.split_mappers
        }
        return split_mappers_dict

    def __call__(self, mappers: Dict[str, Mapper], data: Iterable[Dict]):

        split_mappers_dict = self.generate_split_mappers_dict(mappers)

        for row in data:
            split_iter_dict = self.transform(split_mappers_dict, row)

            if any(
                not isinstance(split_iter, Iterable)
                for split_iter in split_iter_dict.values()
            ):
                raise ValueError("Cannot perform one-to-many on a non-iterable value")

            # TODO: I dont think this preserves order here for generic Mappings
            # We are assuming split_iter_dict === dict(zip(split_iter_dict.keys(), split_iter_dict.values())), which I dont think is correct
            for split in self.split_method(*split_iter_dict.values()):
                transformed = self.transform(mappers, row)

                # TODO: Performance
                split_dict = {
                    split_key: split_val
                    for split_key, split_val in zip(split_iter_dict.keys(), split)
                    if split_key in mappers.keys()
                }  # Only save keys split key-vals which are defined in the desired mappers

                yield {
                    **transformed,
                    **split_dict,
                }  # Order here is important - we want our transformed split val to overwrite the raw data at split_key


class ManyToOneTransform(Transform):
    # Say we have some fields that we know are the SAME over multiple rows
    # Can we define a way to merge these rows into a single row in a nice way?
    # We could maybe do a recursive meta merge?
    pass


class FilterTransform(Transform):
    def __init__(self, filter_fn: Callable[[Any], bool]):
        self.filter_fn = filter_fn

    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        for item in data:
            if self.filter_fn(item):
                yield self.transform(mappers, item)


# TODO: Fix this dec to be current
def one_to_many(split_mappers):
    def _one_to_many(cls):
        cls._transform = OneToManyTransform(split_mappers)
        return cls

    return _one_to_many
