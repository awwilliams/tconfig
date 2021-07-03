"""
Created on Sep 19, 2017

@author: Alan Williams
"""
import math
import itertools
from copy import copy, deepcopy
from typing import Iterator

from tconfig.core.algorithms.recursive import IntMod
from tconfig.core.algorithms.recursive import PolyMod
from tconfig.core.algorithms.recursive import RemainderPoly

from tconfig.core.algorithms.recursive import utils


def _find_irreducible_poly(degree: int) -> PolyMod:
    zero = IntMod(0)
    pcoefs = []
    for _ in range(0, degree):
        pcoefs.append(copy(IntMod(0)))
    pcoefs.append(copy(IntMod(1)))
    result = PolyMod(pcoefs)
    while result.is_reducible():
        index = 0
        result[index] += 1
        while result[index] == zero:
            index += 1
            if index > degree:
                raise ArithmeticError(f"No irreducible polynomial of degree {degree}")
            result[index] += 1
    return result


class Field(object):
    def __init__(self, order: int = 0):
        self.elements = []
        self.order = order
        if order > 0:
            self._generate(order)

    def __repr__(self) -> str:
        return f"Field(order={self.order})"

    def __str__(self) -> str:
        return f"Field: order={self.order}, elements={self.elements}"

    def __iter__(self) -> Iterator[RemainderPoly]:
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, key) -> RemainderPoly:
        return self.elements[key]

    def __setitem__(self, key: int, value: RemainderPoly):
        self.elements[key] = value

    def __delitem__(self, key: int):
        self.elements.pop(key)

    def __eq__(self, other: "Field") -> bool:
        return all(
            s == o for (s, o) in itertools.zip_longest(self.elements, other.elements)
        )

    def __hash__(self) -> int:
        return hash(self.elements)

    def _generate(self, order: int):
        # Set up vector of Galois field elements

        prime_factor = utils.is_prime_power(order)
        if prime_factor == 1:
            # Order is prime

            # Field is integers modulo order.  Set IntMod modulus

            IntMod.modulus = order

            # Field elements are RemainderPolys, with simple IntMod coefficients, 0 to order - 1

            for value in range(0, order):
                self.elements.append(RemainderPoly(coef_list=[IntMod(value)]))

        elif prime_factor > 0:
            # Order = primeFactor ^ quoDegree, where quoDegree is an
            # integer > 1

            # Set modulus for IntMod coefficients to be primeFactor

            IntMod.modulus = prime_factor

            # Find irreducible polynomial of degree quoDegree

            quo_degree = int(math.log(order, prime_factor))
            quotient = _find_irreducible_poly(quo_degree)

            # Irreducible polynomial becomes quotient polynomial for
            # extending the field of integers modulo primeFactor (which has
            # order = primeFactor) to a field with order
            # primeFactor ^ quoDegree

            RemainderPoly.quotient = quotient

            # Field elements will be the set of equivalence classes of
            # polynomial residues with respect to the quotient polynomial.
            # These residues will be polynomials of (maximum) degree
            # quoDegree - 1.

            degree = quo_degree - 1

            # Because the polynomial coefficients are IntMods, there are
            # only 'primeFactor' possibilities for each coefficient.
            # Therefore, there are exactly primeFactor * quoDegree
            # polynomials, which is exactly what we want for the number of
            # elements in the field.

            # Generate possible polynomials in enumeration order.  That is,
            # start with all coefficients as zero.  Increment the constant
            # coefficient.  When the constant coefficient increments to
            # zero, increment next coefficient, and keep going until some
            # coefficient increments to a non-zero value.

            # Generate field element zero.  Take copy of polynomial to avoid
            # anomalies.

            element_generator = RemainderPoly(coef_list=[])
            for _ in range(0, degree + 1):
                element_generator.coef_list.append(copy(IntMod(0)))
            next_element = deepcopy(element_generator)
            next_element.collapse_degree()
            self.elements.append(next_element)

            # Generate rest of elements
            for _ in range(1, order):

                # Try next polynomial, by incrementing constant coefficient.

                increment_index = 0
                element_generator[increment_index] += 1

                # If current coefficient is zero after increment, we have
                # looped through the entire set of values mod modulus.
                # Increment the coefficient of next higher degree.  Continue
                # until the increment operation produces a non-zero
                # coefficient.  The for loop limits us so that we don't
                # increment the final coefficient to zero and overflow the
                # array.

                while element_generator[increment_index] == IntMod(0):
                    increment_index += 1
                    element_generator[increment_index] += 1

                # Take copy of polynomial, and create new element

                next_element = deepcopy(element_generator)
                next_element.collapse_degree()
                self.elements.append(next_element)
        else:
            # order is invalid
            raise ArithmeticError(f"Field order {order} is not a prime power")
