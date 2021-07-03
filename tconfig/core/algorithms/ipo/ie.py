"""
Created on Oct 3, 2017

@author: Alan Williams
"""

from collections import UserDict
from typing import Tuple


class InteractionElement(UserDict):
    def __repr__(self) -> str:
        return f"InteractionElement(value_dict={self.data})"

    def __str__(self) -> str:
        return str(self.data)

    # noinspection PyTypeChecker
    def _key(self) -> Tuple[int, int]:
        return tuple((k, self[k]) for k in sorted(self.keys()))

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: "InteractionElement") -> bool:
        # noinspection PyProtectedMember
        return self._key() == other._key()  # pylint: disable=protected-access

    @property
    def degree(self) -> int:
        return len(self)

    def get_ie_excepting_parm(self, parm_index: int) -> "InteractionElement":
        result = InteractionElement(self.data)
        del result[parm_index]
        return result
