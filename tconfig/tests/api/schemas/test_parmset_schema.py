"""
Created on Sep 9, 2017

@author: Alan Williams
"""

import pytest

from tconfig.api.schemas import ParameterSchema, ParameterSetSchema

from tconfig.orm import orm_utils
from tconfig.tests.orm import test_utils


# pylint: disable=invalid-name, redefined-outer-name


@pytest.mark.usefixtures("orm")
@pytest.fixture
def a1():
    return test_utils.create_test_value("A1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def a2():
    return test_utils.create_test_value("A2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def a3():
    return test_utils.create_test_value("A3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def b1():
    return test_utils.create_test_value("B1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def b2():
    return test_utils.create_test_value("B2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def b3():
    return test_utils.create_test_value("B3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def c1():
    return test_utils.create_test_value("C1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def c2():
    return test_utils.create_test_value("C2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def c3():
    return test_utils.create_test_value("C3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d1():
    return test_utils.create_test_value("D1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d2():
    return test_utils.create_test_value("D2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d3():
    return test_utils.create_test_value("D3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def d4():
    return test_utils.create_test_value("D4")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def e1():
    return test_utils.create_test_value("E1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def e2():
    return test_utils.create_test_value("E2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_a(a1, a2, a3):
    return test_utils.create_test_parameter("A", values=[a1, a2, a3])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_b(b1, b2, b3):
    return test_utils.create_test_parameter("B", values=[b1, b2, b3])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_c(c1, c2, c3):
    return test_utils.create_test_parameter("C", values=[c1, c2, c3])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_d(d1, d2, d3, d4):
    return test_utils.create_test_parameter("D", values=[d1, d2, d3, d4])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_e(e1, e2):
    return test_utils.create_test_parameter("E", values=[e1, e2])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parmset_abcde(parm_a, parm_b, parm_c, parm_d, parm_e):
    return test_utils.create_test_parameter_set(
        parameters=[parm_a, parm_b, parm_c, parm_d, parm_e]
    )


@pytest.mark.usefixtures("orm")
def test_schema_serialize(parmset_abcde, parm_a, parm_b, parm_c, parm_e):
    parmset_abcde.set_adjacent(parm_a, parm_c, False)
    parmset_abcde.set_adjacent(parm_b, parm_e, False)
    orm_utils.orm_commit(parmset_abcde, "update")

    parmset_schema = ParameterSetSchema()
    schema_dict = parmset_schema.dump(parmset_abcde)
    expected = {
        "name": None,
        "parameters": [
            {
                "excluded": [3],
                "excluded_by": [],
                "name": "A",
                "parameter_set": 1,
                "position": 0,
                "uid": 1,
                "values": [
                    {"name": "A1", "parameter": 1, "position": 0, "uid": 1},
                    {"name": "A2", "parameter": 1, "position": 1, "uid": 2},
                    {"name": "A3", "parameter": 1, "position": 2, "uid": 3},
                ],
            },
            {
                "excluded": [5],
                "excluded_by": [],
                "name": "B",
                "parameter_set": 1,
                "position": 1,
                "uid": 2,
                "values": [
                    {"name": "B1", "parameter": 2, "position": 0, "uid": 4},
                    {"name": "B2", "parameter": 2, "position": 1, "uid": 5},
                    {"name": "B3", "parameter": 2, "position": 2, "uid": 6},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [1],
                "name": "C",
                "parameter_set": 1,
                "position": 2,
                "uid": 3,
                "values": [
                    {"name": "C1", "parameter": 3, "position": 0, "uid": 7},
                    {"name": "C2", "parameter": 3, "position": 1, "uid": 8},
                    {"name": "C3", "parameter": 3, "position": 2, "uid": 9},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [],
                "name": "D",
                "parameter_set": 1,
                "position": 3,
                "uid": 4,
                "values": [
                    {"name": "D1", "parameter": 4, "position": 0, "uid": 10},
                    {"name": "D2", "parameter": 4, "position": 1, "uid": 11},
                    {"name": "D3", "parameter": 4, "position": 2, "uid": 12},
                    {"name": "D4", "parameter": 4, "position": 3, "uid": 13},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [2],
                "name": "E",
                "parameter_set": 1,
                "position": 4,
                "uid": 5,
                "values": [
                    {"name": "E1", "parameter": 5, "position": 0, "uid": 14},
                    {"name": "E2", "parameter": 5, "position": 1, "uid": 15},
                ],
            },
        ],
        "position": None,
        "uid": 1,
    }

    assert schema_dict == expected


def test_schema_deserialize(orm, parmset_abcde, parm_a, parm_b, parm_c, parm_e):
    parmset_abcde.set_adjacent(parm_a, parm_c, False)
    parmset_abcde.set_adjacent(parm_b, parm_e, False)
    orm_utils.orm_commit(parmset_abcde, "update")

    parmset_schema = ParameterSetSchema()
    parmset_dict = {
        "name": None,
        "parameters": [
            {
                "excluded": [3],
                "excluded_by": [],
                "name": "A",
                "parameter_set": 1,
                "position": 0,
                "uid": 1,
                "values": [
                    {"name": "A1", "parameter": 1, "position": 0, "uid": 1},
                    {"name": "A2", "parameter": 1, "position": 1, "uid": 2},
                    {"name": "A3", "parameter": 1, "position": 2, "uid": 3},
                ],
            },
            {
                "excluded": [5],
                "excluded_by": [],
                "name": "B",
                "parameter_set": 1,
                "position": 1,
                "uid": 2,
                "values": [
                    {"name": "B1", "parameter": 2, "position": 0, "uid": 4},
                    {"name": "B2", "parameter": 2, "position": 1, "uid": 5},
                    {"name": "B3", "parameter": 2, "position": 2, "uid": 6},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [1],
                "name": "C",
                "parameter_set": 1,
                "position": 2,
                "uid": 3,
                "values": [
                    {"name": "C1", "parameter": 3, "position": 0, "uid": 7},
                    {"name": "C2", "parameter": 3, "position": 1, "uid": 8},
                    {"name": "C3", "parameter": 3, "position": 2, "uid": 9},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [],
                "name": "D",
                "parameter_set": 1,
                "position": 3,
                "uid": 4,
                "values": [
                    {"name": "D1", "parameter": 4, "position": 0, "uid": 10},
                    {"name": "D2", "parameter": 4, "position": 1, "uid": 11},
                    {"name": "D3", "parameter": 4, "position": 2, "uid": 12},
                    {"name": "D4", "parameter": 4, "position": 3, "uid": 13},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [2],
                "name": "E",
                "parameter_set": 1,
                "position": 4,
                "uid": 5,
                "values": [
                    {"name": "E1", "parameter": 5, "position": 0, "uid": 14},
                    {"name": "E2", "parameter": 5, "position": 1, "uid": 15},
                ],
            },
        ],
        "position": None,
        "uid": 1,
    }
    ps_loaded = parmset_schema.load(parmset_dict, session=orm.session)
    assert ps_loaded == parmset_abcde
    assert ps_loaded is parmset_abcde


def test_schema_round_trip(orm, parmset_abcde, parm_a, parm_b, parm_c, parm_e):
    parmset_abcde.set_adjacent(parm_a, parm_c, False)
    parmset_abcde.set_adjacent(parm_b, parm_e, False)
    orm_utils.orm_commit(parmset_abcde, "update")

    parmset_schema = ParameterSetSchema()
    parm_schema = ParameterSchema()
    parmset_dict = parmset_schema.dump(parmset_abcde)
    ps_loaded = parmset_schema.load(parmset_dict, session=orm.session)
    assert ps_loaded == parmset_abcde
    assert ps_loaded is parmset_abcde

    parm_b_dict = parmset_schema.dump(parm_b)
    parm_b_loaded = parm_schema.load(parm_b_dict, session=orm.session)
    assert parm_b_loaded == parm_b
    assert parm_b_loaded is parm_b

    parm_e_dict = parmset_schema.dump(parm_e)
    parm_e_loaded = parm_schema.load(parm_e_dict, session=orm.session)
    assert parm_e_loaded == parm_e
    assert parm_e_loaded is parm_e
