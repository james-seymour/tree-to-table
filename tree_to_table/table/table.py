from typing import Any, Dict, Iterable

from ..mappers import Mapper
from ..transforms import Transform, OneToOneTransform


class Column:
    def __init__(self, mapper: Mapper):
        self.mapper = mapper


class Table:
    transform: Transform = OneToOneTransform()

    @classmethod
    def mappers(cls) -> Dict[str, Mapper]:
        "A mapping of all class variables defined on this table that are Mappers"
        return {
            column_name: mapper
            for column_name, mapper in cls.__dict__.items()
            if issubclass(type(mapper), Mapper)
        }

    @classmethod
    def map(cls, data: Iterable[Dict]):
        "The main entrypoint for transforming a set of data"
        return cls.transform(cls.mappers(), data)
