"""
Created on Sep 9, 2017

@author: Alan Williams
"""

import re
import numpy as np
import pandas as pd
import pytest

from tconfig.core.data import Value, Parameter, ParameterSet


# pylint: disable=invalid-name


@pytest.fixture
def a1():
    return Value("A1")


@pytest.fixture
def a2():
    return Value("A2")


@pytest.fixture
def a3():
    return Value("A3")


@pytest.fixture
def b1():
    return Value("B1")


@pytest.fixture
def b2():
    return Value("B2")


@pytest.fixture
def b3():
    return Value("B3")


@pytest.fixture
def c1():
    return Value("C1")


@pytest.fixture
def c2():
    return Value("C2")


@pytest.fixture
def c3():
    return Value("C3")


@pytest.fixture
def d1():
    return Value("D1")


@pytest.fixture
def d2():
    return Value("D2")


@pytest.fixture
def d3():
    return Value("D3")


@pytest.fixture
def d4():
    return Value("D4")


@pytest.fixture
def e1():
    return Value("E1")


@pytest.fixture
def e2():
    return Value("E2")


@pytest.fixture
def parm_1():
    return Parameter.create_with_unnamed_values("1", 3)


@pytest.fixture
def parm_2():
    return Parameter.create_with_unnamed_values("2", 3)


@pytest.fixture
def parm_3():
    return Parameter.create_with_unnamed_values("3", 3)


@pytest.fixture
def parm_4():
    return Parameter.create_with_unnamed_values("4", 4)


@pytest.fixture
def parm_5():
    return Parameter.create_with_unnamed_values("5", 2)


@pytest.fixture
def parm_6():
    return Parameter.create_with_unnamed_values("6", 5)


@pytest.fixture
def parm_7():
    return Parameter.create_with_unnamed_values("7", 2)


@pytest.fixture
def parm_set_5(parm_1, parm_2, parm_3, parm_4, parm_5):
    return ParameterSet([parm_1, parm_2, parm_3, parm_4, parm_5])


@pytest.fixture
def parm_a(a1, a2, a3):
    return Parameter("A", [a1, a2, a3])


@pytest.fixture
def parm_b(b1, b2, b3):
    return Parameter("B", [b1, b2, b3])


@pytest.fixture
def parm_c(c1, c2, c3):
    return Parameter("C", [c1, c2, c3])


@pytest.fixture
def parm_d(d1, d2, d3, d4):
    return Parameter("D", [d1, d2, d3, d4])


@pytest.fixture
def parm_e(a1, e1, e2):
    return Parameter("E", [e1, e2])


@pytest.fixture
def parmset_ae(parm_a, parm_b, parm_c, parm_d, parm_e):
    return ParameterSet([parm_a, parm_b, parm_c, parm_d, parm_e])


def test_parmset_jsonify():
    ps = ParameterSet.create_from_parm_and_value_sizes(3, 4)
    j = ps.to_json()
    x = ParameterSet.from_json(j)
    assert x == ps


def test_init_default():
    ps = ParameterSet()

    assert len(ps.parameters) == 0
    assert ps.parameters == []


def test_init_one_parm():
    p = Parameter.create_with_unnamed_values("Z", 4)

    plist = [
        p,
    ]
    ps = ParameterSet(plist)

    assert ps.parameters == plist
    assert ps.parameters is not plist  # copy, not reference


def test_init_two_parms():
    p1 = Parameter.create_with_unnamed_values("P1", 2)
    p2 = Parameter.create_with_unnamed_values("P2", 3)
    plist = [p1, p2]
    ps = ParameterSet(plist)

    assert len(ps.parameters) == 2
    assert ps.parameters == plist
    assert ps.parameters is not plist  # copy, not reference


def test_init_three_parms():
    p1 = Parameter.create_with_unnamed_values("P1", 4)
    p2 = Parameter.create_with_unnamed_values("P2", 6)
    p3 = Parameter.create_with_unnamed_values("P3", 2)
    plist = [p1, p2, p3]

    ps = ParameterSet(plist)

    assert len(ps.parameters) == 3
    assert ps.parameters == plist
    assert ps.parameters is not plist  # copy, not reference


def test_create_same_size_parms():
    ps = ParameterSet.create_from_parm_and_value_sizes(3, 4)

    p1 = Parameter.create_with_unnamed_values("1", 4)
    p2 = Parameter.create_with_unnamed_values("2", 4)
    p3 = Parameter.create_with_unnamed_values("3", 4)
    plist = [p1, p2, p3]
    ps_expected = ParameterSet(plist)

    assert all(
        pactual.name == pexpected.name
        for pactual, pexpected in zip(ps.parameters, ps_expected.parameters)
    )
    assert all(
        len(pactual) == len(pexpected)
        for pactual, pexpected in zip(ps.parameters, ps_expected.parameters)
    )


def test_create_different_size_parms():
    p1 = Parameter.create_with_unnamed_values("1", 4)
    p2 = Parameter.create_with_unnamed_values("2", 5)
    p3 = Parameter.create_with_unnamed_values("3", 3)
    plist = [p1, p2, p3]

    ps = ParameterSet(plist)

    assert ps.parameters == plist


def test_get_item(parm_set_5, parm_3):
    assert parm_set_5[2] == parm_3


def test_get_item_bad_index(parm_set_5):
    with pytest.raises(IndexError, match="list index out of range"):
        _ = parm_set_5[7]


def test_set_item(parm_set_5, parm_1, parm_2, parm_3, parm_5, parm_6):
    parm_set_5[3] = parm_6

    expected_plist = [parm_1, parm_2, parm_3, parm_6, parm_5]

    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_set_item_bad_index(parm_set_5, parm_6):
    with pytest.raises(IndexError, match="list assignment index out of range"):
        parm_set_5[7] = parm_6


def test_delitem(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5):
    del parm_set_5[3]

    expected_plist = [parm_1, parm_2, parm_3, parm_5]
    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_delitem_missing(parm_set_5):
    with pytest.raises(IndexError, match="list assignment index out of range"):
        del parm_set_5[7]


def test_append(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5, parm_6):
    assert len(parm_set_5) == 5

    parm_set_5.append(parm_6)

    assert len(parm_set_5) == 6

    expected_plist = [parm_1, parm_2, parm_3, parm_4, parm_5, parm_6]

    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_extend(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5, parm_6, parm_7):
    assert len(parm_set_5) == 5

    parm_set_5.extend([parm_6, parm_7])

    assert len(parm_set_5) == 7

    expected_plist = [parm_1, parm_2, parm_3, parm_4, parm_5, parm_6, parm_7]

    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_insert(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5, parm_6):
    assert len(parm_set_5) == 5

    parm_set_5.insert(3, parm_6)

    expected_plist = [parm_1, parm_2, parm_3, parm_6, parm_4, parm_5]

    assert len(parm_set_5) == 6
    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_insert_at_end(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5, parm_6):
    assert len(parm_set_5) == 5

    parm_set_5.insert(5, parm_6)

    assert len(parm_set_5) == 6

    expected_plist = [parm_1, parm_2, parm_3, parm_4, parm_5, parm_6]

    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_remove(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5):
    parm_set_5.remove(parm_4)

    expected_plist = [parm_1, parm_2, parm_3, parm_5]
    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_remove_missing(parm_set_5, parm_6):
    error_message = re.escape("list.remove(x): x not in list")
    with pytest.raises(ValueError, match=error_message):
        parm_set_5.remove(parm_6)


def test_pop(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5):
    popped_parm = parm_set_5.pop()
    assert popped_parm == parm_5

    expected_plist = [parm_1, parm_2, parm_3, parm_4]
    ps_expected = ParameterSet(expected_plist)
    assert parm_set_5.parameters == ps_expected.parameters


def test_pop_index(parm_set_5, parm_1, parm_2, parm_3, parm_4, parm_5):
    pop_index = 2

    popped_parm = parm_set_5.pop(pop_index)
    assert popped_parm == parm_3

    ps_expected = ParameterSet([parm_1, parm_2, parm_4, parm_5])
    assert parm_set_5.parameters == ps_expected.parameters


def test_index(parm_set_5, parm_4):
    assert parm_set_5.index(parm_4) == 3


def test_index_missing(parm_set_5, parm_7):
    error_message = re.escape(f"{repr(parm_7)} is not in list")
    with pytest.raises(ValueError, match=error_message):
        parm_set_5.index(parm_7)


def test_set_adjacent(parm_set_5, parm_2, parm_4):
    parm_set_5.set_adjacent(parm_2, parm_4, False)

    assert parm_4 in parm_2.excluded
    assert parm_2 in parm_4.excluded_by


def test_is_adjacent(parm_set_5, parm_1, parm_2, parm_3, parm_4):
    parm_2.exclude_interaction_with(parm_4)

    assert not parm_set_5.is_adjacent(parm_2, parm_4)
    assert parm_set_5.is_adjacent(parm_1, parm_3)


def test_clear(parm_set_5):
    parm_set_5.clear()

    assert parm_set_5.parameters == []


def test_to_dataframe(
    parmset_ae, a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3, d4, e1, e2
):
    df = parmset_ae.to_dataframe()

    expected_df = pd.DataFrame(
        [
            [a1, b1, c1, d1, e1],
            [a2, b2, c2, d2, e2],
            [a3, b3, c3, d3, np.NaN],
            [np.NaN, np.NaN, np.NaN, d4, np.NaN],
        ],
        columns=["A", "B", "C", "D", "E"],
    )

    assert df.equals(expected_df)


def test_to_dict(parmset_ae, parm_a, parm_b, parm_c, parm_d, parm_e):
    parmset_ae.set_adjacent(parm_a, parm_c, False)
    parmset_ae.set_adjacent(parm_b, parm_e, False)

    expected_dict = {
        "uid": str(parmset_ae.uid),
        "parameters": [p.to_dict() for p in [parm_a, parm_b, parm_c, parm_d, parm_e]],
    }

    assert parmset_ae.to_dict() == expected_dict


def test_from_dict(parmset_ae, parm_a, parm_b, parm_c, parm_d, parm_e):
    parmset_dict = {
        "uid": "337f7234-85a1-45a0-be77-0934ec232f21",
        "parameters": [p.to_dict() for p in [parm_a, parm_b, parm_c, parm_d, parm_e]],
        "adjacency": [
            [True, True, False, True, True],
            [True, True, True, True, False],
            [False, True, True, True, True],
            [True, True, True, True, True],
            [True, False, True, True, True],
        ],
    }

    ps = ParameterSet.from_dict(parmset_dict)

    expected_ps = ParameterSet(
        [parm_a, parm_b, parm_c, parm_d, parm_e],
        uid="337f7234-85a1-45a0-be77-0934ec232f21",
    )
    expected_ps.set_adjacent(parm_a, parm_c, False)
    expected_ps.set_adjacent(parm_b, parm_e, False)

    assert ps == expected_ps


def test_dict_round_trip(parmset_ae, parm_a, parm_b, parm_c, parm_e):
    parmset_ae.set_adjacent(parm_a, parm_c, False)
    parmset_ae.set_adjacent(parm_b, parm_e, False)

    parmset_dict = parmset_ae.to_dict()

    ps_new = ParameterSet.from_dict(parmset_dict)
    assert ps_new == parmset_ae
