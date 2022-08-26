from .base import Mapper


class Coalesce(Mapper):
    def __init__(self, *mappers):
        self.mappers = mappers

    def __call__(self, obj):
        return self.run(obj)

    def run(self, obj):
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

    def __call__(self, obj):
        return self.run(obj)

    def run(self, obj):
        realised_context = {name: mapper(obj) for name, mapper in self.context.items()}
        return self.mapper(realised_context)(obj)
