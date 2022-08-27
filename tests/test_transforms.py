import logging

from tree_to_table.transforms import OneToManyTransform
from tree_to_table.mappers import Get

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestOneToManyTransform:
    data = [{"split_key": [1, 2, 3], "other_key": 10}]

    def test_simple_one_to_many(self):
        logger.info("hello")
        split_mappers = {"splitted": Get("split_key")}
        mappers = {"other": Get("other_key")}
        logger.debug(OneToManyTransform(split_mappers)(mappers, self.data))
