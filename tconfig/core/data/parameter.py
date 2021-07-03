"""
Module for parameter with discrete, named values.
"""

from typing import Union, List, Iterator, Iterable, Optional

import pandas as pd

from .jsonserializable import JsonSerializable, UidType
from .value import Value


# pylint: disable=unsubscriptable-object


class Parameter(JsonSerializable):
    """
    Class representing a parameter in a test configuration.  A parameter has a
    name, and a collection of Value objects.

    Parameter can be serialized to be passed from a web interface to
    server API.
    """

    value_class = Value

    def __init__(
        self,
        name="",
        values: Optional[List[Union[str, Value]]] = None,
        uid: UidType = None,
    ):
        """
        Initialization:  provide name and optional list of parameter
        values.  If provided, collection can be a list or dictionary.  Contents
        can be Value objects or strings.  If contents are strings, new Value
        instances are created with those names.
        """
        super().__init__(uid=uid)

        self.name = name
        vlist = []
        if isinstance(values, list):
            if all(isinstance(a, Value) for a in values):
                vlist = values
            else:
                vlist = [self.value_class(name) for name in values]
        if hasattr(self, "values"):
            self.values.extend(vlist)  # pylint: disable=access-member-before-definition
        else:
            self.values = vlist
        self.excluded = []
        self.excluded_by = []

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Parameter(name="{self.name}", uid="{self.uid}", values={self.values})'

    def __eq__(self, other: "Parameter") -> bool:
        return (
            all(getattr(self, attr) == getattr(other, attr) for attr in ["uid", "name"])
            and self.values == other.values
        )

    def __hash__(self) -> int:
        return hash((self.name, getattr(self, "uid"), self.values))

    def __iter__(self) -> Iterator[Value]:
        return iter(self.values)

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: Union[slice, int]) -> Value:
        return self.values[index]

    def __setitem__(self, index: Union[slice, int], value: Value):
        self.values[index] = value

    def __delitem__(self, index: Union[slice, int]):
        del self.values[index]

    def to_series(self) -> pd.Series:
        return pd.Series(data=self.values, name=self.name)

    def append(self, value: Value) -> None:
        self.values.append(value)

    def extend(self, value_iterable: Iterable[Value]) -> None:
        self.values.extend(value_iterable)

    def insert(self, index, value: Value) -> None:
        self.values.insert(index, value)

    def remove(self, value: Value) -> None:
        self.values.remove(value)

    def pop(self, *args) -> Value:
        return self.values.pop(*args)

    def clear(self) -> None:
        self.values.clear()

    def index(self, *args) -> int:
        return self.values.index(*args)

    @classmethod
    def create_with_unnamed_values(cls, name: str, num_values: int) -> "Parameter":
        return cls(name, [cls.value_class(str(x)) for x in range(1, num_values + 1)])

    def to_dict(self):
        result = super().to_dict()
        result.update({"name": self.name, "values": [v.to_dict() for v in self.values]})
        return result

    @classmethod
    def from_dict(cls, cls_dict):
        values = [cls.value_class.from_dict(v_dict) for v_dict in cls_dict["values"]]
        return cls(cls_dict["name"], values=values, uid=cls_dict["uid"])

    def exclude_interaction_with(self, other_parm):
        if self.interacts_with(other_parm):
            self.excluded.append(other_parm)
            other_parm.excluded_by.append(self)

    def restore_interaction_with(self, other_parm):
        if self.is_excluding(other_parm):
            self.excluded.remove(other_parm)
            other_parm.excluded_by.remove(self)
        if self.is_excluded_by(other_parm):
            self.excluded_by.remove(other_parm)

    def is_excluding(self, other_parm):
        return other_parm in self.excluded

    def is_excluded_by(self, other_parm):
        return other_parm in self.excluded_by

    def interacts_with(self, other_parm):
        return not self.is_excluding(other_parm) and not self.is_excluded_by(other_parm)
