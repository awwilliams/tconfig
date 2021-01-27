import pytest

from tconfig.api.schemas import ParameterSchema

from tconfig.tests.orm import test_utils


# pylint: disable=invalid-name, redefined-outer-name


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_1():
    return test_utils.create_test_value("V1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_2():
    return test_utils.create_test_value("V2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_3():
    return test_utils.create_test_value("V3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_4():
    return test_utils.create_test_value("V4")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_5():
    return test_utils.create_test_value("V5")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_new():
    return test_utils.create_test_value("VNEW")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_extra():
    return test_utils.create_test_value("VEXTRA")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def pz_four_values(val_1, val_2, val_3, val_4):
    return test_utils.create_test_parameter("Z", values=[val_1, val_2, val_3, val_4])


@pytest.mark.usefixtures("orm")
def test_schema_serialize(pz_four_values):
    parm_schema = ParameterSchema()
    p_dict = parm_schema.dump(pz_four_values)
    expected = {
        'excluded': [],
        'excluded_by': [],
        'name': 'Z',
        'parameter_set': None,
        'position': None,
        'uid': 1,
        'values': [
            {'name': 'V1', 'parameter': 1, 'position': 0, 'uid': 1},
            {'name': 'V2', 'parameter': 1, 'position': 1, 'uid': 2},
            {'name': 'V3', 'parameter': 1, 'position': 2, 'uid': 3},
            {'name': 'V4', 'parameter': 1, 'position': 3, 'uid': 4}
        ]
    }
    assert p_dict == expected


def test_schema_deserialize(orm, pz_four_values):
    parm_schema = ParameterSchema()
    p_dict = {
        'excluded': [],
        'excluded_by': [],
        'name': 'Z',
        'parameter_set': None,
        'position': None,
        'uid': 1,
        'values': [
            {'name': 'V1', 'parameter': 1, 'position': 0, 'uid': 1},
            {'name': 'V2', 'parameter': 1, 'position': 1, 'uid': 2},
            {'name': 'V3', 'parameter': 1, 'position': 2, 'uid': 3},
            {'name': 'V4', 'parameter': 1, 'position': 3, 'uid': 4}
        ]
    }
    p_loaded = parm_schema.load(p_dict, session=orm.session)
    assert p_loaded == pz_four_values
    assert p_loaded is pz_four_values


def test_schema_round_trip(orm, pz_four_values):
    parm_schema = ParameterSchema()
    schema_dict = parm_schema.dump(pz_four_values)
    p_loaded = parm_schema.load(schema_dict, session=orm.session)
    assert p_loaded == pz_four_values
    assert p_loaded is pz_four_values
