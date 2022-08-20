from __future__ import annotations
from typing import Mapping, Any, Union
from tree_to_table.core.mappers import Get, Apply

Data = Union[Any, Mapping[Any, Union[Any, "Data"]]]  # type: ignore


class TestGetMapper:
    data: Data = {"key_1": "value_1", "key_2": {"key_3": "value_3"}}

    def test_simple_get(self):
        assert Get("key_1")(self.data) == "value_1"

    def test_multiple_get(self):
        # TODO: Check types are working here correctly once implemented
        assert Get("key_2", Get("key_3"))(self.data) == "value_3"

    def test_no_key_get(self):
        assert Get("no_key_found")(self.data) == None

    def test_multiple_no_key_get(self):
        assert Get("no_key_found", Get("no_key_found"))(self.data) == None


class TestGetDefaultMapper:
    data: Data = {"key_1": "value_1", "key_2": {"key_3": "value_3"}}


class TestApplyMapper:
    data: Data = "unwanted/value_1"

    def test_simple_apply(self):
        def remove_unwanted(value: str):
            return value.split("/")[1]

        assert Apply(remove_unwanted)(self.data) == "value_1"

    def test_simple_apply_2(self):
        def return_hello(value: str):
            return "hello"

        assert Apply(return_hello)(self.data) == "hello"
