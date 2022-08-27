from typing import ClassVar

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr

from ..transforms import Transform, OneToOneTransform, OneToManyTransform


class ORMAncestor:
    transform: ClassVar[Transform] = OneToOneTransform()

    @declared_attr
    def __tablename__(cls):
        return cls.__name__


ORMBase = declarative_base(name="ORMBase", cls=ORMAncestor)


class Invoice(ORMBase):
    service_id: Column(Integer, primary_key=True)
    yeet: Column(Integer)


print(ORMBase.registry)
