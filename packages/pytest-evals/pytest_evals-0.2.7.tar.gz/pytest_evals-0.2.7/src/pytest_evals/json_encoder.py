import dataclasses
import json
from enum import Enum
from typing import Callable

try:
    from pydantic import BaseModel

    HAVE_PYDANTIC = True
except ImportError:
    HAVE_PYDANTIC = False
    BaseModel = type(None)  # Create a dummy type that won't match anything

try:
    import pandas as pd

    def is_series(obj):  # pyright: ignore [reportRedeclaration]
        return isinstance(obj, pd.Series)

    def is_dataframe(obj):  # pyright: ignore [reportRedeclaration]
        return isinstance(obj, pd.DataFrame)
except ImportError:

    def is_series(obj):
        return False

    def is_dataframe(obj):
        return False


class AdvancedJsonEncoder(json.JSONEncoder):
    """JSON encoder that handles Pydantic models (if installed) and other special types."""

    def default(self, o):
        if HAVE_PYDANTIC and isinstance(o, BaseModel):
            return json.loads(o.model_dump_json())  # type: ignore
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)  # type: ignore
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, Callable):
            return f"<{o.__module__}.{o.__name__}>"
        if isinstance(o, type(None)):
            return None
        if is_series(o):
            return o.to_dict()
        if is_dataframe(o):
            return o.to_dict(orient="records")
        return super().default(o)
