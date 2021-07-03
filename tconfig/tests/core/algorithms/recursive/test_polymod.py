"""
Created on Sep 17, 2017

@author: Alan Williams
"""

import pytest

from tconfig.core.algorithms.recursive.intmod import IntMod
from tconfig.core.algorithms.recursive.polymod import PolyMod

# pylint: disable=invalid-name


def test_create():
    IntMod.modulus = 5
    p = PolyMod()

    assert p.coef_list == []

    with pytest.raises(ValueError, match="Degree of null polynomial undefined."):
        # noinspection PyStatementEffect
        p.degree  # pylint: disable=pointless-statement


def test_create_with_coefs():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2)])

    assert p.coef_list == [IntMod(2)]

    assert p.degree == 0


def test_degree():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2), IntMod(3), IntMod(0), IntMod(1), IntMod(4)])

    assert p.degree == 4


def test_str():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2), IntMod(3), IntMod(0), IntMod(1), IntMod(4)])

    assert str(p) == "4x^4 + x^3 + 3x + 2"


def test_str_degree_zero():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2)])

    assert str(p) == "2"


def test_str_zero_poly():
    IntMod.modulus = 5
    p = PolyMod([IntMod(0)])

    assert str(p) == "0"


def test_str_zero_handling():
    IntMod.modulus = 5
    p = PolyMod([IntMod(0), IntMod(0), IntMod(0), IntMod(4)])

    assert str(p) == "4x^3"


def test_str_one_poly():
    IntMod.modulus = 5
    p = PolyMod([IntMod(1)])

    assert str(p) == "1"


def test_str_one_handling():
    IntMod.modulus = 5
    p = PolyMod([IntMod(1), IntMod(1), IntMod(1)])

    assert str(p) == "x^2 + x + 1"


def test_collapse_degree():
    IntMod.modulus = 5
    p = PolyMod(
        [IntMod(0), IntMod(0), IntMod(0), IntMod(2), IntMod(1), IntMod(0), IntMod(0)]
    )
    p.collapse_degree()

    expected_p = PolyMod([IntMod(0), IntMod(0), IntMod(0), IntMod(2), IntMod(1)])

    assert p == expected_p


def test_collapse_degree_all_zeros():
    IntMod.modulus = 5
    p = PolyMod(
        [IntMod(0), IntMod(0), IntMod(0), IntMod(0), IntMod(0), IntMod(0), IntMod(0)]
    )
    p.collapse_degree()

    expected_p = PolyMod([IntMod(0)])

    assert p == expected_p


def test_collapse_to_one_poly():
    IntMod.modulus = 5
    p = PolyMod(
        [IntMod(1), IntMod(0), IntMod(0), IntMod(0), IntMod(0), IntMod(0), IntMod(0)]
    )
    p.collapse_degree()

    expected_p = PolyMod([IntMod(1)])

    assert p == expected_p


def test_enumerate():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2), IntMod(3), IntMod(4)])

    assert p.enumerate() == 117


def test_evaluate():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2), IntMod(3), IntMod(4)])

    assert p(IntMod(3)) == IntMod(2)


def test_reducible_false():
    IntMod.modulus = 5
    p = PolyMod([IntMod(2), IntMod(3), IntMod(4)])

    assert not p.is_reducible()


def test_reducible_true():
    IntMod.modulus = 5
    p = PolyMod([IntMod(0), IntMod(1)])

    assert p.is_reducible()


def test_reducible_factors():
    IntMod.modulus = 5
    p = PolyMod([IntMod(1), IntMod(2), IntMod(1)])

    assert p.is_reducible()
