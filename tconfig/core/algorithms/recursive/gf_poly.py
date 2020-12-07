"""
Created on Sep 16, 2017

@author: Alan Williams
"""

import itertools
from typing import List, Iterator
from tconfig.core.algorithms.recursive.field import Field
from tconfig.core.algorithms.recursive.rem_poly import RemainderPoly


class GFPolynomial(object):

    def __init__(self, coef_list: List[RemainderPoly]):
        self.coef_list = [] if coef_list is None else coef_list

    @classmethod
    def create_from_field_and_value(cls, field: Field, value: int, max_degree: int):
        coef_list = []
        for _ in range(0, max_degree + 1):
            coef = value % field.order
            coef_list.append(field[coef])
            value = value // field.order
        return GFPolynomial(coef_list=coef_list)

    def __repr__(self) -> str:
        return f"GFPolynomial(coef_list={self.coef_list})"

    def __iter__(self) -> Iterator:
        return iter(self.coef_list)

    def __len__(self):
        return len(self.coef_list)

    def __getitem__(self, key):
        return self.coef_list[key]

    def __setitem__(self, key, value):
        self.coef_list[key] = value

    def __delitem__(self, key):
        self.coef_list.pop(key)

    def __eq__(self, other):
        return all(s == o for (s, o) in itertools.zip_longest(self, other))

    def __hash__(self):
        return hash(self.coef_list)

    def __call__(self, xval):
        """
        Evaluate Galois field polynomial at field element value.

        Returns an integer representing the result of evaluation.  The integer is the "enumeration"
        value of the Galois field element, which is its index in the field (range 0...order - 1).
        If the field is {x[0], ..., x[n-1]}, and the polynomial evaluates to x[j], this function
        returns the value of j.  The type of 'xval' is expected to be a RemainderPoly.
        """
        result = RemainderPoly.constant(0)
        term = RemainderPoly.constant(1)
        for coef in self:
            result = result + coef * term
            term = term * xval
        return result.enumerate()

    @property
    def degree(self):
        if self.coef_list:
            return len(self.coef_list) - 1
        raise ValueError("Degree of null polynomial undefined.")

    def __add__(self, operand):
        coef_tuples = itertools.zip_longest(
            self, operand, fillvalue=RemainderPoly.constant(0))
        result_coefs = [a + b for a, b in coef_tuples]
        result = GFPolynomial(coef_list=result_coefs)
        return result

    def __mul__(self, operand):
        result_degree = self.degree + operand.degree
        result = GFPolynomial(
            coef_list=[RemainderPoly.constant(0)] * (result_degree + 1))

        for k in range(result_degree + 1):
            min_index = k - operand.degree if k - operand.degree > 0 else 0
            max_index = k if k < self.degree else self.degree
            for m in range(min_index, max_index + 1):  # pylint: disable=invalid-name
                result[k] = result[k] + self[m] * operand[k - m]
        return result

    def __str__(self):
        if self.degree == 0 or all(c.enumerate() == 0 for c in self):
            return str(self[0])

        content = []
        for index, coef in reversed(list(enumerate(self))):
            ecoef = coef.enumerate()
            if ecoef != 0:
                content.append("{}{}{}".format(
                    str(ecoef) if ecoef != 1 or index == 0 else '',
                    'x' if index >= 1 else '',
                    f'^{index}' if index >= 2 else ''
                ))
        return ' + '.join(content)
