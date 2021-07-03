import numpy as np
import pandas as pd

from tconfig.core.data import (
    Value,
    Parameter,
    ParameterSet,
    ConfigurationSet,
    DEFAULT_NDARRAY_TYPE,
)

RED = Value("Red")
GREEN = Value("Green")
BLUE = Value("Blue")

BIRD = Value("Bird")
CAT = Value("Cat")
DOG = Value("Dog")
FISH = Value("Fish")

FAST = Value("Fast")
MEDIUM = Value("Medium")
SLOW = Value("Slow")

SEVENTIES = Value("70s")
EIGHTIES = Value("80s")
TWENTIES = Value("20s")


def test_generate_configurations():
    """
    Verify that a parameter set and a covering array with
    no "don't care" values present is correctly converted
    to a data frame with the correct column headings and
    value names.
    """
    p1 = Parameter("Colour", [RED, GREEN, BLUE])
    p2 = Parameter("Pet", [BIRD, CAT, DOG])
    p3 = Parameter("Speed", [FAST, MEDIUM, SLOW])
    p4 = Parameter("Music", [SEVENTIES, EIGHTIES, TWENTIES])

    parameter_set = ParameterSet([p1, p2, p3, p4])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array(
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
    configurations = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )
    actual_configurations = configurations.configs

    expected_configurations = pd.DataFrame(
        [
            [RED, BIRD, FAST, SEVENTIES],
            [RED, CAT, MEDIUM, EIGHTIES],
            [RED, DOG, SLOW, TWENTIES],
            [GREEN, BIRD, MEDIUM, TWENTIES],
            [GREEN, CAT, SLOW, SEVENTIES],
            [GREEN, DOG, FAST, EIGHTIES],
            [BLUE, BIRD, SLOW, EIGHTIES],
            [BLUE, CAT, FAST, TWENTIES],
            [BLUE, DOG, MEDIUM, SEVENTIES],
        ],
        columns=["Colour", "Pet", "Speed", "Music"],
    )

    assert actual_configurations.equals(expected_configurations)


def test_generate_configurations_with_dont_care():
    """
    Verify that a parameter set and a covering array that
    contains a "don't care" value is correctly converted
    to a data frame, where the "don't care" value becomes
    Pandas' pd.NA value.
    """
    p1 = Parameter("Colour", [RED, GREEN])
    p2 = Parameter("Pet", [BIRD, CAT, DOG, FISH])
    p3 = Parameter("Speed", [FAST, SLOW])
    p4 = Parameter("Music", [EIGHTIES, TWENTIES])

    parameter_set = ParameterSet([p1, p2, p3, p4])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array(
        [
            [1, 1, 1, 1],
            [1, 2, 2, 1],
            [2, 1, 2, 1],
            [2, 2, 1, 0],
            [2, 2, 2, 2],
            [1, 1, 1, 2],
            [1, 3, 1, 1],
            [2, 3, 2, 2],
            [1, 4, 1, 1],
            [2, 4, 2, 2],
        ]
    )
    configurations = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )
    actual_configurations = configurations.configs

    expected_configurations = pd.DataFrame(
        [
            [RED, BIRD, FAST, EIGHTIES],
            [RED, CAT, SLOW, EIGHTIES],
            [GREEN, BIRD, SLOW, EIGHTIES],
            [GREEN, CAT, FAST, pd.NA],
            [GREEN, CAT, SLOW, TWENTIES],
            [RED, BIRD, FAST, TWENTIES],
            [RED, DOG, FAST, EIGHTIES],
            [GREEN, DOG, SLOW, TWENTIES],
            [RED, FISH, FAST, EIGHTIES],
            [GREEN, FISH, SLOW, TWENTIES],
        ],
        columns=["Colour", "Pet", "Speed", "Music"],
    )

    assert actual_configurations.equals(expected_configurations)


def test_configset_len():
    """
    Verify that a parameter set and a covering array with
    no "don't care" values present is correctly converted
    to a data frame with the correct column headings and
    value names.
    """
    p1 = Parameter("Colour", [RED, GREEN, BLUE])
    p2 = Parameter("Pet", [BIRD, CAT, DOG])
    p3 = Parameter("Speed", [FAST, MEDIUM, SLOW])
    p4 = Parameter("Music", [SEVENTIES, EIGHTIES, TWENTIES])

    parameter_set = ParameterSet([p1, p2, p3, p4])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array(
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
    configurations = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )

    assert len(configurations) == 9


def test_configset_getitem():
    """
    Verify that a parameter set and a covering array with
    no "don't care" values present is correctly converted
    to a data frame with the correct column headings and
    value names.
    """
    p1 = Parameter("Colour", [RED, GREEN, BLUE])
    p2 = Parameter("Pet", [BIRD, CAT, DOG])
    p3 = Parameter("Speed", [FAST, MEDIUM, SLOW])
    p4 = Parameter("Music", [SEVENTIES, EIGHTIES, TWENTIES])

    parameter_set = ParameterSet([p1, p2, p3, p4])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array(
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
    configurations = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )

    expected = pd.Series(
        {
            "Colour": GREEN,
            "Pet": BIRD,
            "Speed": MEDIUM,
            "Music": TWENTIES,
        }
    )
    actual = configurations[3]
    assert pd.Series.equals(actual, expected)


def test_configset_iterate():
    """
    Verify that a parameter set and a covering array with
    no "don't care" values present is correctly converted
    to a data frame with the correct column headings and
    value names.
    """
    p1 = Parameter("Colour", [RED, GREEN])
    p2 = Parameter("Pet", [CAT, DOG])
    p3 = Parameter("Speed", [FAST, SLOW])

    parameter_set = ParameterSet([p1, p2, p3])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array([[1, 1, 1], [1, 2, 2], [2, 1, 2], [2, 2, 1]])
    configurations = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )

    expected = [
        pd.Series(
            {
                "Colour": RED,
                "Pet": CAT,
                "Speed": FAST,
            }
        ),
        pd.Series(
            {
                "Colour": RED,
                "Pet": DOG,
                "Speed": SLOW,
            }
        ),
        pd.Series(
            {
                "Colour": GREEN,
                "Pet": CAT,
                "Speed": SLOW,
            }
        ),
        pd.Series(
            {
                "Colour": GREEN,
                "Pet": DOG,
                "Speed": FAST,
            }
        ),
    ]
    for index, actual in enumerate(configurations):
        assert pd.Series.equals(actual, expected[index])


def test_equals():
    """
    Verify that a parameter set and a covering array that
    contains a "don't care" value is correctly converted
    to a data frame, where the "don't care" value becomes
    Pandas' pd.NA value.
    """
    p1 = Parameter("Colour", [RED, GREEN])
    p2 = Parameter("Pet", [BIRD, CAT, DOG, FISH])
    p3 = Parameter("Speed", [FAST, SLOW])
    p4 = Parameter("Music", [EIGHTIES, TWENTIES])

    parameter_set = ParameterSet([p1, p2, p3, p4])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array(
        [
            [1, 1, 1, 1],
            [1, 2, 2, 1],
            [2, 1, 2, 1],
            [2, 2, 1, 0],
            [2, 2, 2, 2],
            [1, 1, 1, 2],
            [1, 3, 1, 1],
            [2, 3, 2, 2],
            [1, 4, 1, 1],
            [2, 4, 2, 2],
        ]
    )
    # configs1 = ConfigurationSet(parameter_set, covering_array)
    # configs2 = ConfigurationSet(parameter_set, covering_array)
    configs1 = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )
    configs2 = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )

    assert configs1 is not configs2
    assert configs1 == configs2


def test_to_dict():
    p1 = Parameter("Colour", [RED, GREEN])
    p2 = Parameter("Pet", [CAT, DOG])
    p3 = Parameter("Speed", [FAST, SLOW])

    parameter_set = ParameterSet([p1, p2, p3])

    # Covering array from...
    # generator = RecursiveGenerator(parameter_set, 2)
    # covering_array = generator.generate_covering_array()

    covering_array = np.array([[1, 1, 1], [1, 2, 2], [2, 1, 2], [2, 2, 1]])
    configurations = ConfigurationSet(
        parameter_set=parameter_set, covering_array=covering_array
    )

    expected = {
        "configurations": [
            {"Colour": "Red", "Pet": "Cat", "Speed": "Fast"},
            {"Colour": "Red", "Pet": "Dog", "Speed": "Slow"},
            {"Colour": "Green", "Pet": "Cat", "Speed": "Slow"},
            {"Colour": "Green", "Pet": "Dog", "Speed": "Fast"},
        ]
    }
    actual = configurations.to_dict()
    assert actual == expected


def test_dataframe_to_covering_array():
    p1 = Parameter("Colour", [RED, GREEN])
    p2 = Parameter("Pet", [BIRD, CAT, DOG, FISH])
    p3 = Parameter("Speed", [FAST, SLOW])
    p4 = Parameter("Music", [EIGHTIES, TWENTIES])

    parameter_set = ParameterSet([p1, p2, p3, p4])
    dataframe = pd.DataFrame(
        [
            [RED, BIRD, FAST, EIGHTIES],
            [RED, CAT, SLOW, EIGHTIES],
            [GREEN, BIRD, SLOW, EIGHTIES],
            [GREEN, CAT, FAST, pd.NA],
            [GREEN, CAT, SLOW, TWENTIES],
            [RED, BIRD, FAST, TWENTIES],
            [RED, DOG, FAST, EIGHTIES],
            [GREEN, DOG, SLOW, TWENTIES],
            [RED, FISH, FAST, EIGHTIES],
            [GREEN, FISH, SLOW, TWENTIES],
        ],
        columns=["Colour", "Pet", "Speed", "Music"],
    )
    covering_array = ConfigurationSet.dataframe_to_covering_array(
        dataframe, parameter_set
    )
    expected = np.array(
        [
            [1, 1, 1, 1],
            [1, 2, 2, 1],
            [2, 1, 2, 1],
            [2, 2, 1, 0],
            [2, 2, 2, 2],
            [1, 1, 1, 2],
            [1, 3, 1, 1],
            [2, 3, 2, 2],
            [1, 4, 1, 1],
            [2, 4, 2, 2],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )
    assert np.array_equal(covering_array, expected)
