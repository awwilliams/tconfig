"""
Created on Sep 20, 2017

@author: Alan Williams
"""

import pytest

from tconfig.core.algorithms.recursive.intmod import IntMod
from tconfig.core.algorithms.recursive.rem_poly import RemainderPoly
from tconfig.core.algorithms.recursive.field import Field

# pylint: disable=invalid-name


def test_field_2():
    f = Field(2)
    assert f.elements == [RemainderPoly.constant(0), RemainderPoly.constant(1)]


def test_field_3():
    f = Field(3)
    assert f.elements == [
        RemainderPoly.constant(0),
        RemainderPoly.constant(1),
        RemainderPoly.constant(2),
    ]


def test_field_4():
    f = Field(4)
    assert [str(e) for e in f.elements] == ["0", "1", "x", "x + 1"]
    assert f.elements == [
        RemainderPoly(coef_list=[IntMod(0)]),
        RemainderPoly(coef_list=[IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(0), IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(1), IntMod(1)]),
    ]


def test_field_5():
    f = Field(5)
    assert f.elements == [
        RemainderPoly.constant(0),
        RemainderPoly.constant(1),
        RemainderPoly.constant(2),
        RemainderPoly.constant(3),
        RemainderPoly.constant(4),
    ]


def test_field_6():
    with pytest.raises(ArithmeticError, match="Field order 6 is not a prime power"):
        Field(6)


def test_field_7():
    f = Field(7)
    assert f.elements == [
        RemainderPoly.constant(0),
        RemainderPoly.constant(1),
        RemainderPoly.constant(2),
        RemainderPoly.constant(3),
        RemainderPoly.constant(4),
        RemainderPoly.constant(5),
        RemainderPoly.constant(6),
    ]


def test_field_8():
    f = Field(8)
    assert [str(e) for e in f.elements] == [
        "0",
        "1",
        "x",
        "x + 1",
        "x^2",
        "x^2 + 1",
        "x^2 + x",
        "x^2 + x + 1",
    ]
    assert f.elements == [
        RemainderPoly(coef_list=[IntMod(0)]),
        RemainderPoly(coef_list=[IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(0), IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(1), IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(0), IntMod(0), IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(1), IntMod(0), IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(0), IntMod(1), IntMod(1)]),
        RemainderPoly(coef_list=[IntMod(1), IntMod(1), IntMod(1)]),
    ]
