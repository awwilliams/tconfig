
from tconfig.core.data import Value


def test_jsonify_value():
    v = Value("1")
    j = v.to_json()
    x = Value.from_json(j)
    assert x == v


def test_to_dict():
    v = Value("A", uid="337f7234-85a1-45a0-be77-0934ec232f21")
    expected = {
        "name": "A",
        "uid": "337f7234-85a1-45a0-be77-0934ec232f21"
    }
    assert v.to_dict() == expected


def test_from_dict():
    v_dict = {
        "name": "A",
        "uid": "337f7234-85a1-45a0-be77-0934ec232f21"
    }
    v = Value.from_dict(v_dict)
    assert v.name == "A"
    assert str(v.uid) == "337f7234-85a1-45a0-be77-0934ec232f21"


def test_dict_round_trip():
    v_orig = Value("A", uid="337f7234-85a1-45a0-be77-0934ec232f21")
    value_dict = v_orig.to_dict()
    v_new = Value.from_dict(value_dict)

    assert v_new == v_orig
    assert v_new.uid == v_orig.uid
