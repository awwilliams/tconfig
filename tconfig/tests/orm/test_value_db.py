
import pytest
from tconfig.orm.value import ValueDao
from .orm_utils import create_test_value


# pylint: disable=redefined-outer-name

@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_a():
    return create_test_value("A")


@pytest.mark.usefixtures("orm")
def test_jsonify_value_orm(val_a):
    json_str = val_a.to_json()
    val_deserialized = ValueDao.from_json(json_str)
    assert val_deserialized == val_a


@pytest.mark.usefixtures("orm")
def test_to_dict_orm(val_a):
    expected = {
        "name": "A",
        "uid": 1,
        "position": None
    }
    assert val_a.to_dict() == expected


def test_from_dict_orm(orm):
    v_dict = {
        "name": "A",
        "uid": 1,
        "position": 3,
    }
    val = ValueDao.from_dict(v_dict)
    orm.session.add(val)
    orm.session.commit()
    assert val.name == "A"
    assert val.uid == 1
    assert val.position == 3  # @UndefinedVariable # pylint: disable=no-member


@pytest.mark.usefixtures("orm")
def test_dict_round_trip_orm():
    v_orig = create_test_value("A", uid=1)
    value_dict = v_orig.to_dict()
    v_new = ValueDao.from_dict(value_dict)

    assert v_new == v_orig
