"""
Created on Sep 16, 2017

@author: Alan Williams
"""

import pytest

from tconfig.core.algorithms.recursive.intmod import IntMod


# pylint: disable=invalid-name


def test_create_default():
    IntMod.modulus = 0
    a = IntMod()
    assert a.value == 0


def test_create_with_value():
    IntMod.modulus = 0
    a = IntMod(7)
    assert a.value == 7


def test_mod_create_with_value():
    IntMod.modulus = 5
    a = IntMod(7)
    assert a.value == 2


def test_mod_create_with_value_becomes_zero():
    IntMod.modulus = 5
    a = IntMod(10)
    assert a.value == 0


def test_mod_create_with_negative_value():
    IntMod.modulus = 5
    a = IntMod(-2)
    assert a.value == 3


def test_div():
    IntMod.modulus = 5
    a = IntMod(4)
    b = IntMod(3)

    assert a // b == IntMod(3)


def test_div_no_modulus():
    IntMod.modulus = 0
    a = IntMod(8)
    b = IntMod(4)

    assert a // b == IntMod(2)


def test_div_by_zero():
    IntMod.modulus = 5
    a = IntMod(4)
    b = IntMod(0)

    with pytest.raises(ZeroDivisionError):
        a // b  # pylint: disable=pointless-statement


def test_div_no_inverse():
    IntMod.modulus = 8
    a = IntMod(6)
    b = IntMod(4)

    with pytest.raises(ArithmeticError, match="No inverse for 6 with modulus 8"):
        a // b  # pylint: disable=pointless-statement


def test_equal_true():
    IntMod.modulus = 5
    a = IntMod(8)
    b = IntMod(3)

    assert a == b


def test_equal_false():
    IntMod.modulus = 5
    a = IntMod(9)
    b = IntMod(3)

    assert not a == b  # pylint: disable=unneeded-not


def test_not_equal_true():
    IntMod.modulus = 5
    a = IntMod(9)
    b = IntMod(3)

    assert a != b


def test_not_equal_false():
    IntMod.modulus = 5
    a = IntMod(8)
    b = IntMod(3)

    assert not a != b  # pylint: disable=unneeded-not


def test_plus():
    IntMod.modulus = 5
    a = IntMod(4)
    b = IntMod(4)

    assert a + b == IntMod(3)


def test_minus():
    IntMod.modulus = 5
    a = IntMod(1)
    b = IntMod(4)

    assert a - b == IntMod(2)


def test_times():
    IntMod.modulus = 5
    a = IntMod(3)
    b = IntMod(3)

    assert a * b == IntMod(4)


def test_increment():
    IntMod.modulus = 5
    a = IntMod(4)
    a += 1

    assert a == IntMod(0)


def test_increment_no_modulus():
    IntMod.modulus = 0
    a = IntMod(4)
    a += 1
    assert a == IntMod(5)


def test_str():
    IntMod.modulus = 5
    a = IntMod(4)

    assert str(a) == "4"
