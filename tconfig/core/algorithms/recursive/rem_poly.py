"""
Created on Sep 18, 2017

@author: Alan Williams
"""
import itertools

from tconfig.core.algorithms.recursive.intmod import IntMod
from tconfig.core.algorithms.recursive.polymod import PolyMod


class RemainderPoly(PolyMod):
    quotient = PolyMod()

    def __repr__(self) -> str:
        return f"RemainderPoly(coef_list={self.coef_list})"

    def __add__(self, operand: "RemainderPoly") -> "RemainderPoly":
        coef_tuples = itertools.zip_longest(self, operand, fillvalue=IntMod(0))
        result_coefs = [a + b for a, b in coef_tuples]
        result = RemainderPoly(result_coefs)
        result.collapse_degree()
        return result

    def __mul__(self, operand: "RemainderPoly") -> "RemainderPoly":
        result_degree = self.degree + operand.degree
        result = RemainderPoly(coef_list=[IntMod(0)] * (result_degree + 1))

        for k in range(result_degree + 1):
            min_index = k - operand.degree if k - operand.degree > 0 else 0
            max_index = k if k < self.degree else self.degree
            for m in range(min_index, max_index + 1):  # pylint: disable=invalid-name
                result[k] = result[k] + self[m] * operand[k - m]
        result._residue()
        return result

    def _residue(self):
        qdegree = (
            len(RemainderPoly.quotient) - 1 if RemainderPoly.quotient.coef_list else -1
        )

        if qdegree > 0:
            while self.degree >= qdegree:
                factor = self[self.degree] // RemainderPoly.quotient[qdegree]
                for qindex in range(0, qdegree + 1):
                    cindex = self.degree - qdegree + qindex
                    self[cindex] = (
                        self[cindex] - factor * RemainderPoly.quotient[qindex]
                    )
                self.collapse_degree()

    @classmethod
    def constant(cls, value: int) -> "RemainderPoly":
        return cls([IntMod(value)])
