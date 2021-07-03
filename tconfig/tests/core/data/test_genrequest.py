import numpy as np
import pandas as pd

import pytest

from tconfig.core.data import (
    Value,
    Parameter,
    ParameterSet,
    ConfigurationSet,
    GenerationRequest,
)
from tconfig.core.algorithms import RecursiveGenerator, IpoGenerator


@pytest.fixture
def red():
    return Value("Red", uid=1)


@pytest.fixture
def green():
    return Value("Green", uid=2)


@pytest.fixture
def blue():
    return Value("Blue", uid=3)


@pytest.fixture
def bird():
    return Value("Bird", uid=4)


@pytest.fixture
def cat():
    return Value("Cat", uid=5)


@pytest.fixture
def dog():
    return Value("Dog", uid=6)


@pytest.fixture
def fast():
    return Value("Fast", uid=7)


@pytest.fixture
def medium():
    return Value("Medium", uid=8)


@pytest.fixture
def slow():
    return Value("Slow", uid=9)


@pytest.fixture
def seventies():
    return Value("70s", uid=10)


@pytest.fixture
def eighties():
    return Value("80s", uid=11)


@pytest.fixture
def twenties():
    return Value("20s", uid=12)


@pytest.fixture
def colour(orm, red, green, blue):
    return Parameter("Colour", values=[red, green, blue])


@pytest.fixture
def pet(orm, bird, cat, dog):
    return Parameter("Pet", values=[bird, cat, dog])


@pytest.fixture
def speed(orm, fast, medium, slow):
    return Parameter("Speed", values=[fast, medium, slow])


@pytest.fixture
def music(orm, seventies, eighties, twenties):
    return Parameter("Music", values=[seventies, eighties, twenties])


@pytest.fixture
def parm_set(orm, colour, pet, speed, music):
    return ParameterSet(parameters=[colour, pet, speed, music])


@pytest.fixture
def complete_configs(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
    existing_configs = pd.DataFrame(
        [
            [red, bird, fast, seventies],
            [red, cat, medium, eighties],
            [red, dog, slow, twenties],
            [green, bird, medium, twenties],
            [green, cat, slow, seventies],
            [green, dog, fast, eighties],
            [blue, bird, slow, eighties],
            [blue, cat, fast, twenties],
            [blue, dog, medium, seventies],
        ],
        columns=["Colour", "Pet", "Speed", "Music"],
    )
    return ConfigurationSet(data_frame=existing_configs)


@pytest.fixture
def partial_configs(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
    existing_configs = pd.DataFrame(
        [
            [red, bird, fast, seventies],
            [green, dog, fast, eighties],
            [blue, cat, fast, twenties],
            [blue, dog, medium, seventies],
        ],
        columns=["Colour", "Pet", "Speed", "Music"],
    )
    return ConfigurationSet(data_frame=existing_configs)


@pytest.fixture
def configs_with_none(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
    existing_configs = pd.DataFrame(
        [
            [red, bird, pd.NA, seventies],
            [green, dog, fast, pd.NA],
            [blue, pd.NA, fast, twenties],
            [pd.NA, dog, medium, seventies],
        ],
        columns=["Colour", "Pet", "Speed", "Music"],
    )
    return ConfigurationSet(data_frame=existing_configs)


@pytest.fixture
def incomplete_configs(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
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
def configs_bad_values(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Stopped"},
        {"Colour": "Green", "Music": "80s", "Pet": "Giraffe", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "60s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Yellow", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def configs_bad_parameters(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Fast"},
        {"Age": "57", "Music": "80s", "Pet": "Dog", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "20s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


@pytest.fixture
def configs_extra_parameters(
    red, green, blue, bird, cat, dog, fast, medium, slow, seventies, eighties, twenties
):
    return [
        {"Colour": "Red", "Music": "70s", "Pet": "Bird", "Speed": "Fast"},
        {"Age": "57", "Colour": "Green", "Music": "80s", "Pet": "Dog", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "20s", "Pet": "Cat", "Speed": "Fast"},
        {"Colour": "Blue", "Music": "70s", "Pet": "Dog", "Speed": "Medium"},
    ]


def test_create_recursive_genrequest(parm_set):
    req = GenerationRequest(
        parameter_set=parm_set, coverage_degree=2, algorithm_name="recursive"
    )
    assert req.parameter_set == parm_set
    assert req.coverage_degree == 2
    assert req.algorithm_name == "recursive"
    assert req.existing_configurations is None

    gen = req.construct_generator()
    assert isinstance(gen, RecursiveGenerator)
    assert gen.coverage_degree == 2
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]
    assert gen.existing_configs is None


def test_create_recursive_genrequest_degree_too_high_algorithm(parm_set):
    error_message = (
        "Coverage degree higher than 2 not yet implemented for recursive algorithm"
    )
    with pytest.raises(ValueError, match=error_message):
        GenerationRequest(
            parameter_set=parm_set, coverage_degree=3, algorithm_name="recursive"
        )


def test_create_recursive_genrequest_degree_too_high_parameters(parm_set):
    error_message = "Coverage degree 5 higher than number of parameters 4"
    with pytest.raises(ValueError, match=error_message):
        GenerationRequest(
            parameter_set=parm_set, coverage_degree=5, algorithm_name="recursive"
        )


def test_create_recursive_genrequest_bad_degree(parm_set):
    error_message = "Invalid coverage degree '0'"
    with pytest.raises(ValueError, match=error_message):
        GenerationRequest(
            parameter_set=parm_set, coverage_degree=0, algorithm_name="recursive"
        )


def test_create_ipo_2_genrequest(parm_set):
    req = GenerationRequest(
        parameter_set=parm_set, coverage_degree=2, algorithm_name="ipo"
    )
    assert req.parameter_set == parm_set
    assert req.coverage_degree == 2
    assert req.algorithm_name == "ipo"
    assert req.existing_configurations is None

    gen = req.construct_generator()
    assert isinstance(gen, IpoGenerator)
    assert gen.coverage_degree == 2
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]
    assert gen.existing_configs is None


def test_create_ipo_3_genrequest(parm_set):
    req = GenerationRequest(
        parameter_set=parm_set, coverage_degree=3, algorithm_name="ipo"
    )
    assert req.parameter_set == parm_set
    assert req.coverage_degree == 3
    assert req.algorithm_name == "ipo"
    assert req.existing_configurations is None

    gen = req.construct_generator()
    assert isinstance(gen, IpoGenerator)
    assert gen.coverage_degree == 3
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]
    assert gen.existing_configs is None


def test_create_ipo_genrequest_degree_too_high(parm_set):
    error_message = "Coverage degree 5 higher than number of parameters 4"
    with pytest.raises(ValueError, match=error_message):
        GenerationRequest(
            parameter_set=parm_set, coverage_degree=5, algorithm_name="ipo"
        )


def test_create_ipo_genrequest_bad_degree(parm_set):
    error_message = "Invalid coverage degree '0'"
    with pytest.raises(ValueError, match=error_message):
        GenerationRequest(
            parameter_set=parm_set, coverage_degree=0, algorithm_name="ipo"
        )


def test_create_genrequest_bad_algorithm(parm_set):
    error_message = "Invalid algorithm name 'not_an_algorithm'"
    with pytest.raises(ValueError, match=error_message):
        GenerationRequest(parameter_set=parm_set, algorithm_name="not_an_algorithm")


def test_existing_configurations_complete(parm_set, complete_configs):
    req = GenerationRequest(
        parameter_set=parm_set,
        coverage_degree=2,
        algorithm_name="ipo",
        existing_configurations=complete_configs,
    )

    assert req.parameter_set == parm_set
    assert req.coverage_degree == 2
    assert req.algorithm_name == "ipo"
    assert req.existing_configurations == complete_configs

    gen = req.construct_generator()
    assert isinstance(gen, IpoGenerator)
    assert gen.coverage_degree == 2
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]

    expected_covering_array = np.array(
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
        ]
    )
    assert np.array_equal(gen.existing_configs, expected_covering_array)


def test_convert_configurations_none_entries(parm_set, configs_with_none):
    req = GenerationRequest(
        parameter_set=parm_set, existing_configurations=configs_with_none
    )
    assert req.parameter_set == parm_set
    assert req.coverage_degree == 2
    assert req.algorithm_name == "recursive"
    assert req.existing_configurations == configs_with_none

    gen = req.construct_generator()
    assert isinstance(gen, RecursiveGenerator)
    assert gen.coverage_degree == 2
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]

    expected = np.array(
        [
            [1, 1, 0, 1],
            [2, 3, 1, 0],
            [3, 0, 1, 3],
            [0, 3, 2, 1],
        ]
    )
    assert np.array_equal(gen.existing_configs, expected)


def test_create_recursive_genrequest_existing_configs(parm_set, partial_configs):
    req = GenerationRequest(
        parameter_set=parm_set,
        coverage_degree=2,
        algorithm_name="recursive",
        existing_configurations=partial_configs,
    )
    assert req.parameter_set == parm_set
    assert req.coverage_degree == 2
    assert req.algorithm_name == "recursive"
    assert req.existing_configurations == partial_configs

    gen = req.construct_generator()
    assert isinstance(gen, RecursiveGenerator)
    assert gen.coverage_degree == 2
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]
    expected = np.array(
        [
            [1, 1, 1, 1],
            [2, 3, 1, 2],
            [3, 2, 1, 3],
            [3, 3, 2, 1],
        ]
    )
    assert np.array_equal(gen.existing_configs, expected)


def test_create_ipo_genrequest_existing_configs(parm_set, partial_configs):
    req = GenerationRequest(
        parameter_set=parm_set,
        coverage_degree=2,
        algorithm_name="ipo",
        existing_configurations=partial_configs,
    )
    assert req.parameter_set == parm_set
    assert req.coverage_degree == 2
    assert req.algorithm_name == "ipo"
    assert req.existing_configurations == partial_configs

    gen = req.construct_generator()
    assert isinstance(gen, IpoGenerator)
    assert gen.coverage_degree == 2
    assert gen.num_parms == 4
    assert gen.num_values_per_parm == [3, 3, 3, 3]
    expected = np.array(
        [
            [1, 1, 1, 1],
            [2, 3, 1, 2],
            [3, 2, 1, 3],
            [3, 3, 2, 1],
        ]
    )
    assert np.array_equal(gen.existing_configs, expected)
