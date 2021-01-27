import pytest

from tconfig.api.schemas import ValueSchema

from tconfig.tests.orm import test_utils


# pylint: disable=invalid-name, redefined-outer-name

@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_a():
    return test_utils.create_test_value("A")


@pytest.mark.usefixtures("orm")
def test_schema_serialize(val_a):
    value_schema = ValueSchema()
    v_dict = value_schema.dump(val_a)
    expected = {'position': None, 'uid': 1, 'parameter': None, 'name': 'A'}
    assert v_dict == expected


def test_schema_deserialize(orm, val_a):
    value_schema = ValueSchema()
    data = {'position': None, 'uid': 1, 'parameter': None, 'name': 'A'}
    v_loaded = value_schema.load(data, session=orm.session)
    assert v_loaded == val_a
    assert v_loaded is val_a


def test_schema_round_trip(orm, val_a):
    value_schema = ValueSchema()
    v_dict = value_schema.dump(val_a)
    v_loaded = value_schema.load(v_dict, session=orm.session)
    assert v_loaded == val_a
    assert v_loaded is val_a
