
import re

import pytest

from tconfig.orm.value import ValueDao
from tconfig.orm.parameter import ParameterDao
from .orm_utils import create_test_value, create_test_parameter


# pylint: disable=invalid-name, redefined-outer-name

@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_1():
    return create_test_value("V1")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_2():
    return create_test_value("V2")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_3():
    return create_test_value("V3")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_4():
    return create_test_value("V4")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_5():
    return create_test_value("V5")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_new():
    return create_test_value("VNEW")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def val_extra():
    return create_test_value("VEXTRA")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def pz_four_values(val_1, val_2, val_3, val_4):
    return create_test_parameter("Z", values=[val_1, val_2, val_3, val_4])


@pytest.mark.usefixtures("orm")
def test_jsonify_parm(val_1, val_2):
    p = create_test_parameter("Z", values=[val_1, val_2])
    j = p.to_json()
    x = ParameterDao.from_json(j)
    assert x == p


@pytest.mark.usefixtures("orm")
def test_init_name_only():
    p = create_test_parameter("Z")

    assert p.name == "Z"
    assert p.values == []


@pytest.mark.usefixtures("orm")
def test_init_name_values(val_1, val_2):
    value_list = [val_1, val_2]
    p = create_test_parameter("Z", values=value_list)

    assert p.name == "Z"
    assert p.values == value_list


@pytest.mark.usefixtures("orm")
def test_init_name_list_str():
    p = create_test_parameter("Z", values=["A", "B"])

    assert p.name == "Z"

    v1 = ValueDao("A", uid=p.values[0].uid)
    v2 = ValueDao("B", uid=p.values[1].uid)
    assert p.values == [v1, v2]


@pytest.mark.usefixtures("orm")
def test_series(val_1, val_2):
    p = create_test_parameter("Z", values=[val_1, val_2])

    s = p.to_series()

    assert s.name == "Z"
    assert s.to_dict() == {0: val_1, 1: val_2}


def test_create_with_values(orm):
    p = ParameterDao.create_with_unnamed_values("Z", 4)
    orm.session.add(p)
    orm.session.commit()

    assert p.name == "Z"

    v1 = ValueDao("1", uid=p.values[0].uid)
    v2 = ValueDao("2", uid=p.values[1].uid)
    v3 = ValueDao("3", uid=p.values[2].uid)
    v4 = ValueDao("4", uid=p.values[3].uid)

    assert p.values == [v1, v2, v3, v4]


@pytest.mark.usefixtures("orm")
def test_len(pz_four_values):
    assert len(pz_four_values) == 4


@pytest.mark.usefixtures("orm")
def test_eq_true(val_1, val_2, val_3, val_4):
    p1 = create_test_parameter("Z", values=[val_1, val_2, val_3, val_4])
    p2 = ParameterDao("Z", [ValueDao("V1"), ValueDao(
        "V2"), ValueDao("V3"), ValueDao("V4")])

    assert p1 == p2


@pytest.mark.usefixtures("orm")
def test_eq_diff_name(val_1, val_2, val_3, val_4):
    p1 = create_test_parameter("Y", values=[val_1, val_2, val_3, val_4])
    p2 = ParameterDao("Z", [ValueDao("V1"), ValueDao(
        "V2"), ValueDao("V3"), ValueDao("V4")])

    assert not p1 == p2  # pylint: disable=unneeded-not


@pytest.mark.usefixtures("orm")
def test_eq_diff_values(val_1, val_2, val_3, val_4):
    p1 = create_test_parameter("Z", values=[val_1, val_2])
    p2 = create_test_parameter("Z", values=[val_3, val_4])

    assert not p1 == p2  # pylint: disable=unneeded-not


@pytest.mark.usefixtures("orm")
def test_iter(pz_four_values, val_1, val_2, val_3, val_4):
    result = []
    for value in pz_four_values:
        result.append(value)

    assert result == [val_1, val_2, val_3, val_4]


@pytest.mark.usefixtures("orm")
def test_getitem(pz_four_values, val_3):
    assert pz_four_values[2] == val_3


@pytest.mark.usefixtures("orm")
def test_getitem_slice(pz_four_values, val_2, val_3):
    assert pz_four_values[1:3] == [val_2, val_3]


@pytest.mark.usefixtures("orm")
def test_getitem_mini_slice(pz_four_values, val_2):
    assert pz_four_values[1:2] == [val_2, ]


@pytest.mark.usefixtures("orm")
def test_setitem(pz_four_values, val_1, val_2, val_4, val_new):
    pz_four_values[2] = val_new
    pz_four_values.update()

    assert pz_four_values.values == [val_1, val_2, val_new, val_4]


@pytest.mark.usefixtures("orm")
def test_delitem(pz_four_values, val_1, val_2, val_4):
    del pz_four_values[2]

    assert pz_four_values.values == [val_1, val_2, val_4]


@pytest.mark.usefixtures("orm")
def test_set_name(pz_four_values):
    pz_four_values.name = "X"

    assert pz_four_values.name == "X"


@pytest.mark.usefixtures("orm")
def test_append(pz_four_values, val_1, val_2, val_3, val_4, val_new):
    pz_four_values.append(val_new)

    assert pz_four_values.values == [val_1, val_2, val_3, val_4, val_new]


@pytest.mark.usefixtures("orm")
def test_extend(pz_four_values, val_1, val_2,
                val_3, val_4, val_new, val_extra):
    pz_four_values.extend([val_new, val_extra])

    assert pz_four_values.values == [
        val_1, val_2, val_3, val_4, val_new, val_extra]


@pytest.mark.usefixtures("orm")
def test_insert(pz_four_values, val_1, val_2, val_3, val_4, val_new):
    pz_four_values.insert(1, val_new)

    assert pz_four_values.values == [val_1, val_new, val_2, val_3, val_4]


@pytest.mark.usefixtures("orm")
def test_pop(pz_four_values, val_1, val_2, val_3, val_4):
    popped_val = pz_four_values.pop()

    assert popped_val == val_4
    assert pz_four_values.values == [val_1, val_2, val_3]


@pytest.mark.usefixtures("orm")
def test_pop_index(pz_four_values, val_1, val_2, val_3, val_4):
    popped_val = pz_four_values.pop(2)

    assert popped_val == val_3
    assert pz_four_values.values == [val_1, val_2, val_4]


@pytest.mark.usefixtures("orm")
def test_remove(pz_four_values, val_1, val_2, val_3, val_4):
    pz_four_values.remove(val_3)

    assert pz_four_values.values == [val_1, val_2, val_4]


@pytest.mark.usefixtures("orm")
def test_remove_missing(pz_four_values, val_new):
    error_message = re.escape("list.remove(x): x not in list")
    with pytest.raises(ValueError, match=error_message):
        pz_four_values.remove(val_new)


@pytest.mark.usefixtures("orm")
def test_clear(pz_four_values):
    pz_four_values.clear()

    assert pz_four_values.name == "Z"
    assert pz_four_values.values == []


@pytest.mark.usefixtures("orm")
def test_index(pz_four_values, val_3):
    index = pz_four_values.index(val_3)

    assert index == 2


@pytest.mark.usefixtures("orm")
def test_index_start(pz_four_values, val_1):
    error_message = re.escape(f'{repr(val_1)} is not in list')
    with pytest.raises(ValueError, match=error_message):
        pz_four_values.index(val_1, 2)


@pytest.mark.usefixtures("orm")
def test_index_start_stop(pz_four_values, val_4):
    error_message = re.escape(f'{repr(val_4)} is not in list')
    with pytest.raises(ValueError, match=error_message):
        pz_four_values.index(val_4, 0, 2)


@pytest.mark.usefixtures("orm")
def test_to_dict(val_1, val_2, val_3, val_4):
    value_list = [val_1, val_2, val_3, val_4]
    p = create_test_parameter(
        "Z",
        values=value_list,
        uid="337f7234-85a1-45a0-be77-0934ec232f21"
    )
    expected = {
        "name": "Z",
        "uid": 1,
        "position": None,
        "values": [v.to_dict() for v in [val_1, val_2, val_3, val_4]],
    }
    assert p.to_dict() == expected


def test_from_dict(orm, val_1, val_2, val_3, val_4):
    p_dict = {
        "name": "Z",
        "uid": 1,
        "position": 4,
        "values": [v.to_dict() for v in [val_1, val_2, val_3, val_4]]
    }
    p = ParameterDao.from_dict(p_dict)
    orm.session.add(p)
    orm.session.commit()

    assert p.name == "Z"
    assert p.uid == 1
    assert p.position == 4  # pylint: disable=no-member
    assert p.values == [val_1, val_2, val_3, val_4]


@pytest.mark.usefixtures("orm")
def test_dict_round_trip(val_1, val_2, val_3, val_4):
    p_orig = ParameterDao("Z", [val_1, val_2, val_3, val_4], uid=1)

    parameter_dict = p_orig.to_dict()
    p_new = ParameterDao.from_dict(parameter_dict)

    assert p_new == p_orig
