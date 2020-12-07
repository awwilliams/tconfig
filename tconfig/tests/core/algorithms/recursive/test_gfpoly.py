"""
Created on Sep 25, 2017

@author: Alan Williams
"""

from tconfig.core.algorithms.recursive.field import Field
from tconfig.core.algorithms.recursive.gf_poly import GFPolynomial

FIELD_ORDER = 4
f = Field(FIELD_ORDER)

gf1 = GFPolynomial.create_from_field_and_value(f, 7, 2)
gf2 = GFPolynomial.create_from_field_and_value(f, 4, 2)


def test_to_string():
    assert str(gf1) == "x + 3"
    assert str(gf2) == "x"


def test_add():
    assert str(gf1 + gf2) == "3"


def test_mul():
    assert str(gf1 * gf2) == "x^2 + 3x"


def test_evaluate():
    assert str(gf1(f[2])) == "1"
