from marshmallow import ValidationError

import pytest
from tconfig.core.data import GenerationRequest
from tconfig.api.schemas import GeneratorRequestSchema

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
def configs():
    return [
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
    ]


@pytest.fixture
def complete_configs():
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Fast"},
        {"Colour": "Red", "Music": "80s", "Pet": "Cat", "Speed": "Medium"},
        {"Colour": "Red", "Music": "20s", "Pet": "Dog", "Speed": "Slow"},
        {"Colour": "Green", "Music": "20s", "Pet": "Bird", "Speed": "Medium"},
        {"Colour": "Green", "Music": "70s", "Pet": "Cat", "Speed": "Slow"},
        {"Colour": "Green", "Music": "80s", "Pet": "Dog", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "80s", "Pet": "Bird", "Speed": "Slow"},
        {"Colour": "Blue", "Music": "20s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def partial_configs():
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Fast"},
        {"Colour": "Green", "Music": "80s", "Pet": "Dog", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "20s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def configs_with_none():
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": None},
        {"Colour": "Green", "Music": None, "Pet": "Cat", "Speed": "Slow"},
        {"Colour": "Blue", "Music": "20s", "Pet": None, "Speed": "Fast"},
        {"Colour": None, "Music": "80s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def incomplete_configs():
    return [
        {
            "Colour": "Red",
            "Music": "70s",
            "Pet": "Bird",
        },
        {"Colour": "Green", "Pet": "Cat", "Speed": "Slow"},
        {"Colour": "Blue", "Music": "20s", "Speed": "Fast"},
        {"Music": "80s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def configs_bad_values():
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Stopped"},
        {"Colour": "Green", "Music": "80s", "Pet": "Giraffe", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "60s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Yellow", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def configs_bad_parameters():
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Fast"},
        {"Age": "57", "Music": "80s", "Pet": "Dog", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "20s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def configs_extra_parameters():
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Fast"},
        {"Age": "57", "Colour": "Green", "Music": "80s", "Pet": "Dog", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "20s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.mark.usefixtures("orm")
def test_serialize_gen_req(parm_set, configs):
    gen_req = GenerationRequest(
        parameter_set=parm_set,
        algorithm_name="recursive",
        coverage_degree=2,
        existing_configurations=configs,
    )
    schema = GeneratorRequestSchema()
    schema_dict = schema.dump(gen_req)
    expected = {
        "algorithm_name": "recursive",
        "coverage_degree": 2,
        "existing_configurations": [
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
        "parameter_set": {
            "name": None,
            "parameters": [
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Colour",
                    "parameter_set": 1,
                    "position": 0,
                    "uid": 1,
                    "values": [
                        {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
                        {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
                        {"name": "Blue", "parameter": 1, "position": 2, "uid": 3},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Pet",
                    "parameter_set": 1,
                    "position": 1,
                    "uid": 2,
                    "values": [
                        {"name": "Bird", "parameter": 2, "position": 0, "uid": 4},
                        {"name": "Cat", "parameter": 2, "position": 1, "uid": 5},
                        {"name": "Dog", "parameter": 2, "position": 2, "uid": 6},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Speed",
                    "parameter_set": 1,
                    "position": 2,
                    "uid": 3,
                    "values": [
                        {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
                        {"name": "Medium", "parameter": 3, "position": 1, "uid": 8},
                        {"name": "Slow", "parameter": 3, "position": 2, "uid": 9},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Music",
                    "parameter_set": 1,
                    "position": 3,
                    "uid": 4,
                    "values": [
                        {"name": "70s", "parameter": 4, "position": 0, "uid": 10},
                        {"name": "80s", "parameter": 4, "position": 1, "uid": 11},
                        {"name": "20s", "parameter": 4, "position": 2, "uid": 12},
                    ],
                },
            ],
            "uid": 1,
            "position": None,
        },
    }
    assert schema_dict == expected


@pytest.mark.usefixtures("orm")
def test_deserialize(
    parm_set,
    red,
    green,
    blue,
    seventies,
    eighties,
    twenties,
    dog,
    cat,
    bird,
    fast,
    medium,
    slow,
):
    data = {
        "algorithm_name": "recursive",
        "coverage_degree": 2,
        "existing_configurations": [
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
        "parameter_set": {
            "name": None,
            "parameters": [
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Colour",
                    "parameter_set": 1,
                    "position": 0,
                    "uid": 1,
                    "values": [
                        {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
                        {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
                        {"name": "Blue", "parameter": 1, "position": 2, "uid": 3},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Pet",
                    "parameter_set": 1,
                    "position": 1,
                    "uid": 2,
                    "values": [
                        {"name": "Bird", "parameter": 2, "position": 0, "uid": 4},
                        {"name": "Cat", "parameter": 2, "position": 1, "uid": 5},
                        {"name": "Dog", "parameter": 2, "position": 2, "uid": 6},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Speed",
                    "parameter_set": 1,
                    "position": 2,
                    "uid": 3,
                    "values": [
                        {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
                        {"name": "Medium", "parameter": 3, "position": 1, "uid": 8},
                        {"name": "Slow", "parameter": 3, "position": 2, "uid": 9},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Music",
                    "parameter_set": 1,
                    "position": 3,
                    "uid": 4,
                    "values": [
                        {"name": "70s", "parameter": 4, "position": 0, "uid": 10},
                        {"name": "80s", "parameter": 4, "position": 1, "uid": 11},
                        {"name": "20s", "parameter": 4, "position": 2, "uid": 12},
                    ],
                },
            ],
            "position": None,
            "uid": 1,
        },
    }
    schema = GeneratorRequestSchema()
    gen_req = schema.load(data)
    assert gen_req.parameter_set == parm_set
    assert gen_req.algorithm_name == "recursive"
    assert gen_req.coverage_degree == 2


@pytest.mark.usefixtures("orm")
def test_create_ipo_genrequest_degree_too_high(
    parm_set,
    red,
    green,
    blue,
    seventies,
    eighties,
    twenties,
    dog,
    cat,
    bird,
    fast,
    medium,
    slow,
):
    data = {
        "algorithm_name": "ipo",
        "coverage_degree": 5,
        "existing_configurations": [],
        "parameter_set": {
            "name": None,
            "parameters": [
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Colour",
                    "parameter_set": 1,
                    "position": 0,
                    "uid": 1,
                    "values": [
                        {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
                        {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
                        {"name": "Blue", "parameter": 1, "position": 2, "uid": 3},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Pet",
                    "parameter_set": 1,
                    "position": 1,
                    "uid": 2,
                    "values": [
                        {"name": "Bird", "parameter": 2, "position": 0, "uid": 4},
                        {"name": "Cat", "parameter": 2, "position": 1, "uid": 5},
                        {"name": "Dog", "parameter": 2, "position": 2, "uid": 6},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Speed",
                    "parameter_set": 1,
                    "position": 2,
                    "uid": 3,
                    "values": [
                        {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
                        {"name": "Medium", "parameter": 3, "position": 1, "uid": 8},
                        {"name": "Slow", "parameter": 3, "position": 2, "uid": 9},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Music",
                    "parameter_set": 1,
                    "position": 3,
                    "uid": 4,
                    "values": [
                        {"name": "70s", "parameter": 4, "position": 0, "uid": 10},
                        {"name": "80s", "parameter": 4, "position": 1, "uid": 11},
                        {"name": "20s", "parameter": 4, "position": 2, "uid": 12},
                    ],
                },
            ],
            "position": None,
            "uid": 1,
        },
    }
    error_message = "Coverage degree 5 higher than number of parameters 4"
    with pytest.raises(ValidationError, match=error_message):
        schema = GeneratorRequestSchema()
        schema.load(data)


@pytest.mark.usefixtures("orm")
def test_create_ipo_genrequest_bad_degree(
    parm_set,
    red,
    green,
    blue,
    seventies,
    eighties,
    twenties,
    dog,
    cat,
    bird,
    fast,
    medium,
    slow,
):
    data = {
        "algorithm_name": "ipo",
        "coverage_degree": 0,
        "existing_configurations": [],
        "parameter_set": {
            "name": None,
            "parameters": [
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Colour",
                    "parameter_set": 1,
                    "position": 0,
                    "uid": 1,
                    "values": [
                        {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
                        {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
                        {"name": "Blue", "parameter": 1, "position": 2, "uid": 3},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Pet",
                    "parameter_set": 1,
                    "position": 1,
                    "uid": 2,
                    "values": [
                        {"name": "Bird", "parameter": 2, "position": 0, "uid": 4},
                        {"name": "Cat", "parameter": 2, "position": 1, "uid": 5},
                        {"name": "Dog", "parameter": 2, "position": 2, "uid": 6},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Speed",
                    "parameter_set": 1,
                    "position": 2,
                    "uid": 3,
                    "values": [
                        {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
                        {"name": "Medium", "parameter": 3, "position": 1, "uid": 8},
                        {"name": "Slow", "parameter": 3, "position": 2, "uid": 9},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Music",
                    "parameter_set": 1,
                    "position": 3,
                    "uid": 4,
                    "values": [
                        {"name": "70s", "parameter": 4, "position": 0, "uid": 10},
                        {"name": "80s", "parameter": 4, "position": 1, "uid": 11},
                        {"name": "20s", "parameter": 4, "position": 2, "uid": 12},
                    ],
                },
            ],
            "position": None,
            "uid": 1,
        },
    }
    error_message = "Invalid coverage degree '0'"
    with pytest.raises(ValidationError, match=error_message):
        schema = GeneratorRequestSchema()
        schema.load(data)


@pytest.mark.usefixtures("orm")
def test_create_genrequest_bad_algorithm(parm_set):
    data = {
        "algorithm_name": "not_an_algorithm",
        "coverage_degree": 2,
        "existing_configurations": [],
        "parameter_set": {
            "name": None,
            "parameters": [
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Colour",
                    "parameter_set": 1,
                    "position": 0,
                    "uid": 1,
                    "values": [
                        {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
                        {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
                        {"name": "Blue", "parameter": 1, "position": 2, "uid": 3},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Pet",
                    "parameter_set": 1,
                    "position": 1,
                    "uid": 2,
                    "values": [
                        {"name": "Bird", "parameter": 2, "position": 0, "uid": 4},
                        {"name": "Cat", "parameter": 2, "position": 1, "uid": 5},
                        {"name": "Dog", "parameter": 2, "position": 2, "uid": 6},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Speed",
                    "parameter_set": 1,
                    "position": 2,
                    "uid": 3,
                    "values": [
                        {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
                        {"name": "Medium", "parameter": 3, "position": 1, "uid": 8},
                        {"name": "Slow", "parameter": 3, "position": 2, "uid": 9},
                    ],
                },
                {
                    "excluded": [],
                    "excluded_by": [],
                    "name": "Music",
                    "parameter_set": 1,
                    "position": 3,
                    "uid": 4,
                    "values": [
                        {"name": "70s", "parameter": 4, "position": 0, "uid": 10},
                        {"name": "80s", "parameter": 4, "position": 1, "uid": 11},
                        {"name": "20s", "parameter": 4, "position": 2, "uid": 12},
                    ],
                },
            ],
            "position": None,
            "uid": 1,
        },
    }
    error_message = "Invalid algorithm name 'not_an_algorithm'"
    with pytest.raises(ValidationError, match=error_message):
        schema = GeneratorRequestSchema()
        schema.load(data)
