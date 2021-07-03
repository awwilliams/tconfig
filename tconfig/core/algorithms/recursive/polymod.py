"""
Created on Sep 16, 2017

@author: Alan Williams
"""

import itertools
from typing import Union, Optional, Iterable, Iterator

from tconfig.core.algorithms.recursive.intmod import IntMod


class PolyMod(object):
    def __init__(self, coef_list: Optional[Iterable[IntMod]] = None):
        self.coef_list = [] if coef_list is None else list(coef_list)

    def __str__(self) -> str:
        if self.degree == 0 or all(c.value == 0 for c in self):
            return str(self.coef_list[0])

        zero = IntMod(0)
        one = IntMod(1)

        content = []
        for index, coef in reversed(list(enumerate(self))):
            if coef != zero:
                content.append(
                    "{}{}{}".format(
                        str(coef) if coef != one or index == 0 else "",
                        "x" if index >= 1 else "",
                        f"^{index}" if index >= 2 else "",
                    )
                )
        return " + ".join(content)

    def __repr__(self) -> str:
        return f"PolyMod(coef_list={self.coef_list})"

    def __iter__(self) -> Iterator[IntMod]:
        return iter(self.coef_list)

    def __len__(self) -> int:
        return len(self.coef_list)

    def __getitem__(self, key: int) -> IntMod:
        return self.coef_list[key]

    def __setitem__(self, key: int, value: IntMod):
        self.coef_list[key] = value

    def __delitem__(self, key: int):
        self.coef_list.pop(key)

    def __eq__(self, other: "PolyMod") -> bool:
        return all(s == o for (s, o) in itertools.zip_longest(self, other))

    def __hash__(self) -> int:
        return hash(self.coef_list)

    def __call__(self, const_term: Union[IntMod, int]) -> IntMod:
        value = const_term if isinstance(const_term, IntMod) else IntMod(const_term)
        result = IntMod(0)
        term = IntMod(1)
        for coef in self:
            result = result + coef * term
            term = term * value
        return result

    @property
    def degree(self) -> int:
        if self.coef_list:
            return len(self.coef_list) - 1
        raise ValueError("Degree of null polynomial undefined.")

    def collapse_degree(self):
        while len(self.coef_list) > 1 and self.coef_list[-1].value == 0:
            self.coef_list.pop()

    def enumerate(self) -> int:
        result = 0
        term = 1
        for coef in self:
            result = result + coef.value * term
            term = term * IntMod.modulus
        return result

    def is_reducible(self) -> bool:
        zero = IntMod(0)

        value = IntMod(0)
        if self(value) == zero:
            return True

        value += 1
        while value != zero:
            # Check if p(value) = 0.
            if self(value) == zero:
                # If p( value )=0, then ( x - value ) factors p
                return True
            value += 1

        return False
