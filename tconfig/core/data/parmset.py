import itertools
from typing import Optional, List, Iterator, Collection

import pandas as pd

from .jsonserializable import JsonSerializable, UidType
from .parameter import Parameter


# pylint: disable=unsubscriptable-object

class ParameterSet(JsonSerializable):
    parameter_class = Parameter

    def __init__(self, parameters: Optional[List[Parameter]] = None,
                 uid: UidType = None):
        super().__init__(uid=uid)
        self.parameters = [] if parameters is None else list(parameters)

    def __iter__(self) -> Iterator[Parameter]:
        return iter(self.parameters)

    def __len__(self) -> int:
        return len(self.parameters)

    def __getitem__(self, index) -> Parameter:
        return self.parameters[index]

    def __setitem__(self, index, parameter: Parameter):
        self.parameters[index] = parameter

    def __delitem__(self, index):
        del self.parameters[index]

    def __eq__(self, other: "ParameterSet") -> bool:
        if not isinstance(other, ParameterSet):
            return False
        return all(
            s == o for (s, o) in itertools.zip_longest(
                self.parameters, other.parameters))

    def __hash__(self) -> int:
        return hash((getattr(self, 'uid'), self.parameters))

    def __repr__(self) -> str:
        return f"ParameterSet: parameters={self.parameters}"

    @classmethod
    def create_from_parm_and_value_sizes(
            cls, num_parms: int, num_values: int) -> "ParameterSet":
        return cls([
            cls.parameter_class.create_with_unnamed_values(str(index), num_values)
            for index in range(1, num_parms + 1)
        ])

    @classmethod
    def create_from_value_sizes(
            cls, value_size_list: List[int]) -> "ParameterSet":
        return cls([
            cls.parameter_class.create_with_unnamed_values(str(index + 1), value_size)
            for index, value_size in enumerate(value_size_list)
        ])

    def to_dataframe(self) -> pd.DataFrame:
        return pd.concat([p.to_series() for p in self], axis=1)

    def append(self, parameter: Parameter) -> None:
        self.parameters.append(parameter)

    def extend(self, parm_iterable: Collection[Parameter]) -> None:
        self.parameters.extend(parm_iterable)

    def insert(self, index: int, parameter: Parameter):
        self.parameters.insert(index, parameter)

    def remove(self, parameter: Parameter):
        self.parameters.remove(parameter)

    def pop(self, *args) -> Parameter:
        return self.parameters.pop(*args)

    def clear(self) -> None:
        self.parameters.clear()

    def index(self, *args) -> int:
        return self.parameters.index(*args)

    def set_adjacent(self, parm_1: Parameter, parm_2: Parameter,
                     adjacent: bool) -> None:
        if adjacent:
            parm_1.restore_interaction_with(parm_2)
        else:
            parm_1.exclude_interaction_with(parm_2)

    def is_adjacent(self, parm_1: Parameter, parm_2: Parameter) -> bool:
        return parm_1.interacts_with(parm_2)

    def to_dict(self):
        result = super().to_dict()
        result.update({
            "parameters": [p.to_dict() for p in self.parameters],
        })
        return result

    @classmethod
    def from_dict(cls, cls_dict):
        parameters = [cls.parameter_class.from_dict(p_dict)
                      for p_dict in cls_dict["parameters"]]
        uid = cls_dict["uid"]
        return cls(parameters, uid=uid)

    def find_parameter_index_for_value(self, value):
        for parameter in self:
            try:
                index = parameter.index(value)
                return parameter, index
            except ValueError:
                continue
        return None, -1
