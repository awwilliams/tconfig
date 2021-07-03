import re
import pytest

from tconfig.core.data import Value, Parameter

VAL_1 = Value("1")
VAL_2 = Value("2")
VAL_3 = Value("3")
VAL_4 = Value("4")
NEW_VAL = Value("X")
SLICE_VAL = Value("S")


def test_jsonify_parm():
    p = Parameter("Z", [VAL_1, VAL_2])
    j = p.to_json()
    x = Parameter.from_json(j)
    assert x == p


def test_init_name_only():
    p = Parameter("Z")

    assert p.name == "Z"
    assert p.values == []


def test_init_name_values():
    plist = [VAL_1, VAL_2]

    p = Parameter("Z", plist)

    assert p.name == "Z"
    assert p.values == plist


def test_init_name_list_str():
    p = Parameter("Z", ["A", "B"])

    assert p.name == "Z"

    v1 = Value("A", uid=p.values[0].uid)
    v2 = Value("B", uid=p.values[1].uid)
    assert p.values == [v1, v2]


def test_series():
    p = Parameter("Z", [VAL_1, VAL_2])

    s = p.to_series()

    assert s.name == "Z"
    assert s.to_dict() == {0: VAL_1, 1: VAL_2}


def test_create_with_values():
    p = Parameter.create_with_unnamed_values("Z", 4)

    assert p.name == "Z"

    v1 = Value("1", uid=p.values[0].uid)
    v2 = Value("2", uid=p.values[1].uid)
    v3 = Value("3", uid=p.values[2].uid)
    v4 = Value("4", uid=p.values[3].uid)

    assert p.values == [v1, v2, v3, v4]


def test_len():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    assert len(p) == 4


def test_eq_true():
    p1 = Parameter("Z", [VAL_1, VAL_2])
    p2 = Parameter("Z", [VAL_1, VAL_2], uid=p1.uid)

    assert p1 == p2


def test_eq_diff_name():
    p1 = Parameter("Y", [VAL_1, VAL_2])
    p2 = Parameter("Z", [VAL_1, VAL_2])

    assert not p1 == p2  # pylint: disable=unneeded-not


def test_eq_diff_values():
    p1 = Parameter("Z", [VAL_1, VAL_2])
    p2 = Parameter("Z", [VAL_3, VAL_2])

    assert not p1 == p2  # pylint: disable=unneeded-not


def test_iter():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])
    result = []

    for value in p:
        result.append(value)

    assert result == [VAL_1, VAL_2, VAL_3, VAL_4]


def test_getitem():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    assert p[2] == VAL_3


def test_getitem_slice():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    assert p[1:3] == [VAL_2, VAL_3]


def test_getitem_mini_slice():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    assert p[1:2] == [
        VAL_2,
    ]


def test_setitem():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p[2] = NEW_VAL

    assert p.values == [VAL_1, VAL_2, NEW_VAL, VAL_4]


def test_delitem():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    del p[2]

    assert p.values == [VAL_1, VAL_2, VAL_4]


def test_set_name():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p.name = "X"

    p_expected = Parameter("X", [VAL_1, VAL_2, VAL_3, VAL_4], uid=p.uid)

    assert p == p_expected


def test_append():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p.append(NEW_VAL)

    assert p.values == [VAL_1, VAL_2, VAL_3, VAL_4, NEW_VAL]


def test_extend():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p.extend([NEW_VAL, SLICE_VAL])

    assert p.values == [VAL_1, VAL_2, VAL_3, VAL_4, NEW_VAL, SLICE_VAL]


def test_insert():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p.insert(1, NEW_VAL)

    assert p.values == [VAL_1, NEW_VAL, VAL_2, VAL_3, VAL_4]


def test_pop():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    popped_val = p.pop()

    assert popped_val == VAL_4
    assert p.values == [VAL_1, VAL_2, VAL_3]


def test_pop_index():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    popped_val = p.pop(2)

    assert popped_val == VAL_3
    assert p.values == [VAL_1, VAL_2, VAL_4]


def test_remove():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p.remove(VAL_3)

    assert p.values == [VAL_1, VAL_2, VAL_4]


def test_remove_missing():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    error_message = re.escape(f"list.remove(x): x not in list")
    with pytest.raises(ValueError, match=error_message):
        p.remove(NEW_VAL)


def test_clear():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    p.clear()

    assert p.name == "Z"
    assert p.values == []


def test_index():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    index = p.index(VAL_3)

    assert index == 2


def test_index_start():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    error_message = re.escape(f"{repr(VAL_1)} is not in list")
    with pytest.raises(ValueError, match=error_message):
        p.index(VAL_1, 2)


def test_index_start_stop():
    p = Parameter("Z", [VAL_1, VAL_2, VAL_3, VAL_4])

    error_message = re.escape(f"{repr(VAL_4)} is not in list")
    with pytest.raises(ValueError, match=error_message):
        p.index(VAL_4, 0, 2)


def test_to_dict():
    p = Parameter(
        "Z", [VAL_1, VAL_2, VAL_3, VAL_4], uid="337f7234-85a1-45a0-be77-0934ec232f21"
    )
    expected = {
        "name": "Z",
        "uid": "337f7234-85a1-45a0-be77-0934ec232f21",
        "values": [v.to_dict() for v in [VAL_1, VAL_2, VAL_3, VAL_4]],
    }
    assert p.to_dict() == expected


def test_from_dict():
    p_dict = {
        "name": "Z",
        "uid": "337f7234-85a1-45a0-be77-0934ec232f21",
        "values": [v.to_dict() for v in [VAL_1, VAL_2, VAL_3, VAL_4]],
    }
    p = Parameter.from_dict(p_dict)
    assert p.name == "Z"
    assert str(p.uid) == "337f7234-85a1-45a0-be77-0934ec232f21"
    assert p.values == [VAL_1, VAL_2, VAL_3, VAL_4]


def test_dict_round_trip():
    p_orig = Parameter(
        "Z", [VAL_1, VAL_2, VAL_3, VAL_4], uid="337f7234-85a1-45a0-be77-0934ec232f21"
    )

    parameter_dict = p_orig.to_dict()
    p_new = Parameter.from_dict(parameter_dict)

    assert p_new == p_orig
