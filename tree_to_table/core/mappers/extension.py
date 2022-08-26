from .base import Mapper


class Coalesce(Mapper):
    def __init__(self, *mappers):
        self.mappers = mappers

    def apply(self, obj):
        for mapper in self.mappers:
            result = mapper(obj)
            if result:
                return result
        return None


class ContextChoice(Mapper):
    def __init__(
        self,
        context,
        mapper,
    ) -> None:
        self.context = context
        self.mapper = mapper

    def apply(self, obj):
        realised_context = {name: mapper(obj) for name, mapper in self.context.items()}
        return self.mapper(realised_context)(obj)
