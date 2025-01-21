import json
import sys
from dataclasses import dataclass
from enum import Enum
from unittest.mock import patch

import pandas as pd
from pydantic import BaseModel

from pytest_evals.json_encoder import AdvancedJsonEncoder


# Test structures
@dataclass
class Person:
    name: str
    age: int


class Color(Enum):
    RED = "red"
    BLUE = "blue"


class User(BaseModel):
    name: str
    age: int


def test_advanced_json_encoder():
    """Test all AdvancedJsonEncoder functionality"""
    # Setup test data
    person = Person(name="John", age=30)
    data = {
        "person": person,
        "color": Color.RED,
        "basic": {"num": 42, "list": [1, 2]},
    }

    # Test encoding and decoding
    encoded = json.dumps(data, cls=AdvancedJsonEncoder)
    decoded = json.loads(encoded)

    # Verify results
    assert decoded["person"] == {"name": "John", "age": 30}
    assert decoded["color"] == "red"
    assert decoded["basic"] == {"num": 42, "list": [1, 2]}


def test_pydantic_encoding():
    """Test Pydantic model encoding"""
    user = User(name="John", age=30)
    encoded = json.dumps(user, cls=AdvancedJsonEncoder)
    assert json.loads(encoded) == {"name": "John", "age": 30}


def test_function_encoding():
    """Test error on unsupported type"""
    assert (
        json.dumps(lambda x: x, cls=AdvancedJsonEncoder)
        == '"<tests.test_json_encoder.<lambda>>"'
    )


def test_pandas_import_error():
    """Test the fallback functions when pandas is not available"""
    test_obj = object()

    with patch.dict("sys.modules", {"pandas": None}):
        # Import the functions directly inside the patch context
        from pytest_evals.json_encoder import is_series, is_dataframe

        # Test both fallback functions
        assert not is_series(test_obj)
        assert not is_dataframe(test_obj)


def test_dataframe_encoding():
    """Test error on unsupported type"""
    assert (
        json.dumps(pd.DataFrame([{"field": "value"}]), cls=AdvancedJsonEncoder)
        == '[{"field": "value"}]'
    )


def test_series_encoding():
    """Test error on unsupported type"""
    assert (
        json.dumps(pd.Series([1, 2, 3]), cls=AdvancedJsonEncoder)
        == '{"0": 1, "1": 2, "2": 3}'
    )


# Test for json_encoder.py ImportError case
def test_pydantic_import_error():
    with patch.dict(sys.modules, {"pydantic": None}):
        # Force reload of the module to trigger ImportError
        import importlib
        import pytest_evals.json_encoder

        importlib.reload(pytest_evals.json_encoder)

        assert not pytest_evals.json_encoder.HAVE_PYDANTIC
        assert pytest_evals.json_encoder.BaseModel is type(None)
