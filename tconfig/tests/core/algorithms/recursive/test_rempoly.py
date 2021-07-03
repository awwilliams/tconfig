"""
Created on Sep 19, 2017

@author: Alan Williams
"""

from tconfig.core.algorithms.recursive.intmod import IntMod
from tconfig.core.algorithms.recursive.polymod import PolyMod
from tconfig.core.algorithms.recursive.rem_poly import RemainderPoly

# pylint: disable=invalid-name


def test_create_no_quotient():
    IntMod.modulus = 0
    rp = RemainderPoly(
        coef_list=[IntMod(1), IntMod(4), IntMod(6), IntMod(4), IntMod(1)]
    )
    x = str(rp)
    assert x == "x^4 + 4x^3 + 6x^2 + 4x + 1"


def test_create_with_quotient():
    IntMod.modulus = 7
    qp = PolyMod([IntMod(1), IntMod(2), IntMod(1)])
    RemainderPoly.quotient = qp
    rp = RemainderPoly([IntMod(1), IntMod(4), IntMod(6), IntMod(4), IntMod(1)])
    rp._residue()  # pylint: disable=protected-access
    x = str(rp)
    assert x == "0"


def test_plus_no_quotient():
    IntMod.modulus = 2
    rp1 = RemainderPoly(coef_list=[IntMod(0), IntMod(1)])
    rp2 = RemainderPoly(coef_list=[IntMod(1), IntMod(1)])
    rp = rp1 + rp2

    rp_expected = RemainderPoly(coef_list=[IntMod(1)])

    assert rp == rp_expected


def test_plus_different_degrees():
    IntMod.modulus = 2
    rp1 = RemainderPoly(coef_list=[IntMod(0), IntMod(1)])
    rp2 = RemainderPoly(coef_list=[IntMod(1), IntMod(1), IntMod(1)])
    rp = rp1 + rp2

    rp_expected = RemainderPoly(coef_list=[IntMod(1), IntMod(0), IntMod(1)])

    assert rp == rp_expected


def test_times():
    IntMod.modulus = 3
    qp = PolyMod([IntMod(1), IntMod(1), IntMod(1)])
    RemainderPoly.quotient = qp

    rp1 = RemainderPoly(coef_list=[IntMod(1), IntMod(1)])
    rp2 = RemainderPoly(coef_list=[IntMod(1), IntMod(1)])
    rp = rp1 * rp2

    rp_expected = RemainderPoly(coef_list=[IntMod(0), IntMod(1)])

    assert rp == rp_expected


def test_times_no_residue_needed():
    IntMod.modulus = 3
    qp = PolyMod([IntMod(1), IntMod(1), IntMod(1), IntMod(1)])
    RemainderPoly.quotient = qp

    rp1 = RemainderPoly(coef_list=[IntMod(1), IntMod(1)])
    rp2 = RemainderPoly(coef_list=[IntMod(1), IntMod(1)])
    rp = rp1 * rp2

    rp_expected = RemainderPoly(coef_list=[IntMod(1), IntMod(2), IntMod(1)])

    assert rp == rp_expected
