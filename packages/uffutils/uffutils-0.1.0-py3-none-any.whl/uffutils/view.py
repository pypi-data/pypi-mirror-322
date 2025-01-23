from enum import Enum
import json
from typing import Iterable, Protocol
from uffutils.uff.uffdata import UFFData


class AggregationMode(Enum):
    SUMMARY = 1
    FULL = 2


class IView(Protocol):

    @property
    def fields(self) -> list[str]: ...

    def as_dict(self) -> dict: ...


class UFFDataView(IView):

    def __init__(self, data: UFFData):
        self._data = data

    @property
    def fields(self) -> list[str]:
        return ["nodes", "datasets"]

    def as_dict(self) -> dict:
        return {
            "nodes": {
                "count": len(self._data.get_nodes()), 
                "list": self._data.get_nodes()
            }, 
            "datasets": {
                "count": len(self._data.get_set_types()),
                "types": self._data.get_set_type_count(), 
                "list": self._data.get_set_types()
            }
        }


class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs.pop("indent")
        super().__init__(*args, indent=2, **kwargs)

    def encode(self, obj):
        if isinstance(obj, list):
            return self._format_list(obj)
        return super().encode(obj)
    

    def _format_dict(self, d: dict) -> str: 
        ...
        

    def _format_list(self, obj):
        if len(obj) > 5:
            # Keep the first 2 and last 2 elements, add "..."
            shortened_list = obj[:2] + ["..."] + obj[-2:]
        else:
            shortened_list = obj

        # Represent the list horizontally
        return "[" + ", ".join(json.dumps(item, cls=CustomJSONEncoder) for item in shortened_list) + "]"
