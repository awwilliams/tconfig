"""
Created on Sep 9, 2017

@author: Alan Williams
"""

import re
import numpy as np
import pandas as pd
import pytest

from tconfig.orm.parameter import ParameterDao
from tconfig.orm.parmset import ParameterSetDao

from .orm_utils import create_test_value, create_test_parameter, create_test_parameter_set


# pylint: disable=invalid-name, redefined-outer-name, too-many-arguments, too-many-locals

@pytest.mark.usefixtures("orm")
@pytest.fixture
def a1():
    return create_test_value("A1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def a2():
    return create_test_value("A2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def a3():
    return create_test_value("A3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def b1():
    return create_test_value("B1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def b2():
    return create_test_value("B2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def b3():
    return create_test_value("B3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def c1():
    return create_test_value("C1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def c2():
    return create_test_value("C2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def c3():
    return create_test_value("C3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d1():
    return create_test_value("D1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d2():
    return create_test_value("D2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d3():
    return create_test_value("D3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d4():
    return create_test_value("D4")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def e1():
    return create_test_value("E1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def e2():
    return create_test_value("E2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_a(a1, a2, a3):
    return create_test_parameter("A", values=[a1, a2, a3])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_b(b1, b2, b3):
    return create_test_parameter("B", values=[b1, b2, b3])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_c(c1, c2, c3):
    return create_test_parameter("C", values=[c1, c2, c3])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_d(d1, d2, d3, d4):
    return create_test_parameter("D", values=[d1, d2, d3, d4])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_e(e1, e2):
    return create_test_parameter("E", values=[e1, e2])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parmset_abc(parm_a, parm_b, parm_c):
    return create_test_parameter_set(parameters=[parm_a, parm_b, parm_c])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parmset_abcd(parm_a, parm_b, parm_c, parm_d):
    return create_test_parameter_set(parameters=[parm_a, parm_b, parm_c, parm_d])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parmset_abcde(parm_a, parm_b, parm_c, parm_d, parm_e):
    return create_test_parameter_set(parameters=[parm_a, parm_b, parm_c, parm_d, parm_e])


def test_parmset_jsonify():
    ps = ParameterSetDao.create_from_parm_and_value_sizes(3, 4)
    j = ps.to_json()
    x = ParameterSetDao.from_json(j)
    assert x == ps


def test_init_default():
    ps = ParameterSetDao()

    assert len(ps.parameters) == 0
    assert ps.parameters == []


def test_init_one_parm():
    p = ParameterDao.create_with_unnamed_values('Z', 4)

    plist = [p, ]
    ps = ParameterSetDao(plist)

    assert ps.parameters == plist
    assert ps.parameters is not plist  # copy, not reference


def test_init_two_parms():
    p1 = ParameterDao.create_with_unnamed_values("P1", 2)
    p2 = ParameterDao.create_with_unnamed_values("P2", 3)
    plist = [p1, p2]
    ps = ParameterSetDao(plist)

    assert len(ps.parameters) == 2
    assert ps.parameters == plist
    assert ps.parameters is not plist  # copy, not reference


def test_init_three_parms():
    p1 = ParameterDao.create_with_unnamed_values("P1", 4)
    p2 = ParameterDao.create_with_unnamed_values("P2", 6)
    p3 = ParameterDao.create_with_unnamed_values("P3", 2)
    plist = [p1, p2, p3]

    ps = ParameterSetDao(plist)

    assert len(ps.parameters) == 3
    assert ps.parameters == plist
    assert ps.parameters is not plist  # copy, not reference


def test_create_same_size_parms():
    ps = ParameterSetDao.create_from_parm_and_value_sizes(3, 4)

    p1 = ParameterDao.create_with_unnamed_values("1", 4)
    p2 = ParameterDao.create_with_unnamed_values("2", 4)
    p3 = ParameterDao.create_with_unnamed_values("3", 4)
    plist = [p1, p2, p3]
    ps_expected = ParameterSetDao(plist)

    assert all(
        pactual.name == pexpected.name
        for pactual, pexpected in zip(ps.parameters, ps_expected.parameters)
    )
    assert all(
        len(pactual) == len(pexpected)
        for pactual, pexpected in zip(ps.parameters, ps_expected.parameters)
    )


def test_create_different_size_parms():
    p1 = ParameterDao.create_with_unnamed_values("1", 4)
    p2 = ParameterDao.create_with_unnamed_values("2", 5)
    p3 = ParameterDao.create_with_unnamed_values("3", 3)
    plist = [p1, p2, p3]

    ps = ParameterSetDao(plist)

    assert ps.parameters == plist


@pytest.mark.usefixtures("orm")
def test_get_item(parmset_abcd, parm_c):
    assert parmset_abcd[2] == parm_c


@pytest.mark.usefixtures("orm")
def test_get_item_bad_index(parmset_abcd):
    with pytest.raises(IndexError, match="list index out of range"):
        _ = parmset_abcd[7]


@pytest.mark.usefixtures("orm")
def test_set_item(parmset_abcd, parm_a, parm_b, parm_d, parm_e):
    parmset_abcd[2] = parm_e

    assert parmset_abcd.parameters == [parm_a, parm_b, parm_e, parm_d]


@pytest.mark.usefixtures("orm")
def test_set_item_bad_index(parmset_abcd, parm_e):
    with pytest.raises(IndexError, match="list index out of range"):
        parmset_abcd[7] = parm_e


@pytest.mark.usefixtures("orm")
def test_delitem(parmset_abcd, parm_a, parm_b, parm_d):
    del parmset_abcd[2]

    assert parmset_abcd.parameters == [parm_a, parm_b, parm_d]


@pytest.mark.usefixtures("orm")
def test_delitem_missing(parmset_abcd):
    with pytest.raises(IndexError, match="list index out of range"):
        del parmset_abcd[7]


@pytest.mark.usefixtures("orm")
def test_append(parmset_abcd, parm_a, parm_b, parm_c, parm_d, parm_e):
    assert len(parmset_abcd) == 4

    parmset_abcd.append(parm_e)

    assert len(parmset_abcd) == 5

    assert parmset_abcd.parameters == [parm_a, parm_b, parm_c, parm_d, parm_e]


@pytest.mark.usefixtures("orm")
def test_extend(parmset_abc, parm_a, parm_b, parm_c, parm_d, parm_e):
    assert len(parmset_abc) == 3

    parmset_abc.extend([parm_d, parm_e])

    assert len(parmset_abc) == 5

    assert parmset_abc.parameters == [parm_a, parm_b, parm_c, parm_d, parm_e]


@pytest.mark.usefixtures("orm")
def test_insert(parmset_abcd, parm_a, parm_b, parm_c, parm_d, parm_e):
    assert len(parmset_abcd) == 4

    parmset_abcd.insert(3, parm_e)

    assert len(parmset_abcd) == 5
    assert parmset_abcd.parameters == [parm_a, parm_b, parm_c, parm_e, parm_d]


@pytest.mark.usefixtures("orm")
def test_remove(parmset_abcde, parm_a, parm_b, parm_c, parm_d, parm_e):
    parmset_abcde.remove(parm_d)

    assert parmset_abcde.parameters == [parm_a, parm_b, parm_c, parm_e]


@pytest.mark.usefixtures("orm")
def test_remove_missing(parmset_abcd, parm_e):
    error_message = re.escape("list.remove(x): x not in list")
    with pytest.raises(ValueError, match=error_message):
        parmset_abcd.remove(parm_e)


@pytest.mark.usefixtures("orm")
def test_pop(parmset_abcde, parm_a, parm_b, parm_c, parm_d, parm_e):
    popped_parm = parmset_abcde.pop()
    assert popped_parm == parm_e

    assert parmset_abcde.parameters == [parm_a, parm_b, parm_c, parm_d]


@pytest.mark.usefixtures("orm")
def test_pop_index(parmset_abcde, parm_a, parm_b, parm_c, parm_d, parm_e):
    popped_parm = parmset_abcde.pop(2)
    assert popped_parm == parm_c

    assert parmset_abcde.parameters == [parm_a, parm_b, parm_d, parm_e]


@pytest.mark.usefixtures("orm")
def test_index(parmset_abcde, parm_d):
    assert parmset_abcde.index(parm_d) == 3


@pytest.mark.usefixtures("orm")
def test_index_missing(parmset_abcd, parm_e):
    error_message = re.escape(f"{repr(parm_e)} is not in list")
    with pytest.raises(ValueError, match=error_message):
        parmset_abcd.index(parm_e)


@pytest.mark.usefixtures("orm")
def test_set_adjacent(parmset_abcde, parm_b, parm_d):
    parmset_abcde.set_adjacent(parm_b, parm_d, False)

    assert parm_d in parm_b.excluded
    assert parm_b in parm_d.excluded_by


@pytest.mark.usefixtures("orm")
def test_is_adjacent(parmset_abcde, parm_a, parm_b, parm_c, parm_d):
    parm_b.exclude_interaction_with(parm_d)

    assert not parmset_abcde.is_adjacent(parm_b, parm_d)
    assert parmset_abcde.is_adjacent(parm_a, parm_c)


@pytest.mark.usefixtures("orm")
def test_clear(parmset_abcde):
    parmset_abcde.clear()

    assert parmset_abcde.parameters == []


@pytest.mark.usefixtures("orm")
def test_to_dataframe(parmset_abcde, a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3, d4, e1, e2):
    df = parmset_abcde.to_dataframe()

    expected_df = pd.DataFrame([
        [a1, b1, c1, d1, e1],
        [a2, b2, c2, d2, e2],
        [a3, b3, c3, d3, np.NaN],
        [np.NaN, np.NaN, np.NaN, d4, np.NaN]
    ], columns=["A", "B", "C", "D", "E"])

    assert df.equals(expected_df)


@pytest.mark.usefixtures("orm")
def test_to_dict(parmset_abcde, parm_a, parm_b, parm_c, parm_d, parm_e):
    parmset_abcde.set_adjacent(parm_a, parm_c, False)
    parmset_abcde.set_adjacent(parm_b, parm_e, False)

    expected_dict = {
        "uid": 1,
        "parameters": [p.to_dict() for p in [parm_a, parm_b, parm_c, parm_d, parm_e]],
    }

    assert parmset_abcde.to_dict() == expected_dict


@pytest.mark.usefixtures("orm")
def test_from_dict(parm_a, parm_b, parm_c, parm_d, parm_e):
    parmset_dict = {
        "uid": 1,
        "parameters": [p.to_dict() for p in [parm_a, parm_b, parm_c, parm_d, parm_e]],
    }

    ps = ParameterSetDao.from_dict(parmset_dict)

    expected_ps = ParameterSetDao([parm_a, parm_b, parm_c, parm_d, parm_e], uid=1)

    assert ps == expected_ps


@pytest.mark.usefixtures("orm")
def test_dict_round_trip(parmset_abcde, parm_a, parm_b, parm_c, parm_e):
    parmset_abcde.set_adjacent(parm_a, parm_c, False)
    parmset_abcde.set_adjacent(parm_b, parm_e, False)

    parmset_dict = parmset_abcde.to_dict()

    ps_new = ParameterSetDao.from_dict(parmset_dict)
    assert ps_new == parmset_abcde
