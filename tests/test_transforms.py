import logging

from tree_to_table.transforms import OneToManyTransform
from tree_to_table.mappers import Get

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestOneToManyTransform:
    data = [
        {
            "patient_id": 69,
            "practitioner_id": 420,
            "service_ids": [1, 2, 3],
            "items_billed": [104, 105, 105],
            "amounts_billed": [45, 60, 75],
        },
        {
            "patient_id": 100,
            "practitioner_id": 421,
            "service_ids": [4, 5, 6],
            "items_billed": [10945, 2721, 932],
            "amounts_billed": [100, 120, 140],
        },
    ]

    def test_multiple_one_to_many(self):
        split_mappers = {
            "service_id": Get("service_ids"),
            "item_billed": Get("items_billed"),
            "amount_billed": Get("amounts_billed"),
        }

        mappers = {
            "patient_id": Get("patient_id"),
            "practitioner_id": Get("practitioner_id"),
        }

        transformed_generator = OneToManyTransform(split_mappers, keep_splits=True)(
            mappers, self.data
        )
        transformed = list(transformed_generator)

        transformed_expected = [
            {
                "patient_id": 69,
                "practitioner_id": 420,
                "service_id": 1,
                "item_billed": 104,
                "amount_billed": 45,
            },
            {
                "patient_id": 69,
                "practitioner_id": 420,
                "service_id": 2,
                "item_billed": 105,
                "amount_billed": 60,
            },
            {
                "patient_id": 69,
                "practitioner_id": 420,
                "service_id": 3,
                "item_billed": 105,
                "amount_billed": 75,
            },
            {
                "patient_id": 100,
                "practitioner_id": 421,
                "service_id": 4,
                "item_billed": 10945,
                "amount_billed": 100,
            },
            {
                "patient_id": 100,
                "practitioner_id": 421,
                "service_id": 5,
                "item_billed": 2721,
                "amount_billed": 120,
            },
            {
                "patient_id": 100,
                "practitioner_id": 421,
                "service_id": 6,
                "item_billed": 932,
                "amount_billed": 140,
            },
        ]

        assert transformed == transformed_expected
