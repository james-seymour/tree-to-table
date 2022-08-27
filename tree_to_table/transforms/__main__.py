from .base import Transform
from .transforms import OneToManyTransform
from ..mappers import Get

data = [
    {
        "split_key": {"service_ids": [1, 2, 3], "patient_ids": [100, 101, 102]},
        "other_key": 10,
    },
]
split_mappers = {
    "service_id": Get("split_key", Get("service_ids")),
    "patient_id": Get("split_key", Get("patient_ids")),
}
mappers = {"other": Get("other_key")}

p = OneToManyTransform(split_mappers)(mappers, data)
print(list(p))
