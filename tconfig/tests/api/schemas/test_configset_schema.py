"""
Created on Sep 9, 2017

@author: Alan Williams
"""
import numpy as np
from marshmallow import INCLUDE
import pytest

from tconfig.core.data import ConfigurationSet

from tconfig.tests.orm import test_utils


# pylint: disable=invalid-name, redefined-outer-name


@pytest.mark.usefixtures("orm")
@pytest.fixture
def red():
    return test_utils.create_test_value("Red")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def green():
    return test_utils.create_test_value("Green")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def blue():
    return test_utils.create_test_value("Blue")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def bird():
    return test_utils.create_test_value("Bird")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def cat():
    return test_utils.create_test_value("Cat")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def dog():
    return test_utils.create_test_value("Dog")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def fast():
    return test_utils.create_test_value("Fast")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def medium():
    return test_utils.create_test_value("Medium")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def slow():
    return test_utils.create_test_value("Slow")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def seventies():
    return test_utils.create_test_value("70s")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def eighties():
    return test_utils.create_test_value("80s")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def twenties():
    return test_utils.create_test_value("20s")


@pytest.mark.usefixtures("orm")
@pytest.fixture
def colour(red, green, blue):
    return test_utils.create_test_parameter("Colour", values=[red, green, blue])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def pet(bird, cat, dog):
    return test_utils.create_test_parameter("Pet", values=[bird, cat, dog])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def speed(fast, medium, slow):
    return test_utils.create_test_parameter("Speed", values=[fast, medium, slow])


@pytest.mark.usefixtures("orm")
@pytest.fixture
def music(seventies, eighties, twenties):
    return test_utils.create_test_parameter(
        "Music", values=[seventies, eighties, twenties]
    )


@pytest.mark.usefixtures("orm")
@pytest.fixture
def parm_set(colour, pet, speed, music):
    return test_utils.create_test_parameter_set(parameters=[colour, pet, speed, music])


@pytest.fixture
def covering_array():
    return np.array(
        [
            [1, 1, 1, 1],
            [1, 2, 2, 2],
            [1, 3, 3, 3],
            [2, 1, 2, 3],
            [2, 2, 3, 1],
            [2, 3, 1, 2],
            [3, 1, 3, 2],
            [3, 2, 1, 3],
            [3, 3, 2, 1],
        ],
        dtype=np.uint8,
    )


@pytest.mark.usefixtures("orm")
@pytest.fixture
def config_set(parm_set, covering_array):
    return ConfigurationSet(parameter_set=parm_set, covering_array=covering_array)


@pytest.mark.usefixtures("orm")
def test_schema_serialize(config_set):
    from tconfig.api.schemas.configset import ConfigSetSchema

    configset_schema = ConfigSetSchema()
    schema_dict = configset_schema.dump(config_set)
    expected = {
        "configurations": [
            {
                "Colour": {"name": "Red", "uid": 1},
                "Music": {"name": "70s", "uid": 10},
                "Pet": {"name": "Bird", "uid": 4},
                "Speed": {"name": "Fast", "uid": 7},
            },
            {
                "Colour": {"name": "Red", "uid": 1},
                "Music": {"name": "80s", "uid": 11},
                "Pet": {"name": "Cat", "uid": 5},
                "Speed": {"name": "Medium", "uid": 8},
            },
            {
                "Colour": {"name": "Red", "uid": 1},
                "Music": {"name": "20s", "uid": 12},
                "Pet": {"name": "Dog", "uid": 6},
                "Speed": {"name": "Slow", "uid": 9},
            },
            {
                "Colour": {"name": "Green", "uid": 2},
                "Music": {"name": "20s", "uid": 12},
                "Pet": {"name": "Bird", "uid": 4},
                "Speed": {"name": "Medium", "uid": 8},
            },
            {
                "Colour": {"name": "Green", "uid": 2},
                "Music": {"name": "70s", "uid": 10},
                "Pet": {"name": "Cat", "uid": 5},
                "Speed": {"name": "Slow", "uid": 9},
            },
            {
                "Colour": {"name": "Green", "uid": 2},
                "Music": {"name": "80s", "uid": 11},
                "Pet": {"name": "Dog", "uid": 6},
                "Speed": {"name": "Fast", "uid": 7},
            },
            {
                "Colour": {"name": "Blue", "uid": 3},
                "Music": {"name": "80s", "uid": 11},
                "Pet": {"name": "Bird", "uid": 4},
                "Speed": {"name": "Slow", "uid": 9},
            },
            {
                "Colour": {"name": "Blue", "uid": 3},
                "Music": {"name": "20s", "uid": 12},
                "Pet": {"name": "Cat", "uid": 5},
                "Speed": {"name": "Fast", "uid": 7},
            },
            {
                "Colour": {"name": "Blue", "uid": 3},
                "Music": {"name": "70s", "uid": 10},
                "Pet": {"name": "Dog", "uid": 6},
                "Speed": {"name": "Medium", "uid": 8},
            },
        ],
        "parameter_names": ["Colour", "Pet", "Speed", "Music"],
    }
    assert schema_dict == expected


@pytest.mark.usefixtures("orm")
def test_schema_deserialize(orm, config_set):
    from tconfig.api.schemas.configset import ConfigSetSchema

    configset_schema = ConfigSetSchema()
    configset_dict = {
        "configurations": [
            {
                "Colour": {"name": "Red", "uid": 1},
                "Music": {"name": "70s", "uid": 10},
                "Pet": {"name": "Bird", "uid": 4},
                "Speed": {"name": "Fast", "uid": 7},
            },
            {
                "Colour": {"name": "Red", "uid": 1},
                "Music": {"name": "80s", "uid": 11},
                "Pet": {"name": "Cat", "uid": 5},
                "Speed": {"name": "Medium", "uid": 8},
            },
            {
                "Colour": {"name": "Red", "uid": 1},
                "Music": {"name": "20s", "uid": 12},
                "Pet": {"name": "Dog", "uid": 6},
                "Speed": {"name": "Slow", "uid": 9},
            },
            {
                "Colour": {"name": "Green", "uid": 2},
                "Music": {"name": "20s", "uid": 12},
                "Pet": {"name": "Bird", "uid": 4},
                "Speed": {"name": "Medium", "uid": 8},
            },
            {
                "Colour": {"name": "Green", "uid": 2},
                "Music": {"name": "70s", "uid": 10},
                "Pet": {"name": "Cat", "uid": 5},
                "Speed": {"name": "Slow", "uid": 9},
            },
            {
                "Colour": {"name": "Green", "uid": 2},
                "Music": {"name": "80s", "uid": 11},
                "Pet": {"name": "Dog", "uid": 6},
                "Speed": {"name": "Fast", "uid": 7},
            },
            {
                "Colour": {"name": "Blue", "uid": 3},
                "Music": {"name": "80s", "uid": 11},
                "Pet": {"name": "Bird", "uid": 4},
                "Speed": {"name": "Slow", "uid": 9},
            },
            {
                "Colour": {"name": "Blue", "uid": 3},
                "Music": {"name": "20s", "uid": 12},
                "Pet": {"name": "Cat", "uid": 5},
                "Speed": {"name": "Fast", "uid": 7},
            },
            {
                "Colour": {"name": "Blue", "uid": 3},
                "Music": {"name": "70s", "uid": 10},
                "Pet": {"name": "Dog", "uid": 6},
                "Speed": {"name": "Medium", "uid": 8},
            },
        ],
        "parameter_names": ["Colour", "Pet", "Speed", "Music"],
    }
    config_set_loaded = configset_schema.load(configset_dict, unknown=INCLUDE)
    assert config_set_loaded == config_set
