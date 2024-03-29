"""
Created on Sep 30, 2017

@author: Alan Williams
"""

import numpy as np
from tconfig.core.data import DEFAULT_NDARRAY_TYPE, ParameterSet
from tconfig.core.algorithms import RecursiveGenerator


# pylint: disable=invalid-name


def test_generate_configurations():
    ps = ParameterSet.create_from_parm_and_value_sizes(13, 3)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1],
            [1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1],
            [2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 1],
            [2, 2, 3, 1, 2, 2, 3, 1, 2, 2, 3, 1, 0],
            [2, 3, 1, 2, 2, 3, 1, 2, 2, 3, 1, 2, 0],
            [3, 1, 3, 2, 3, 1, 3, 2, 3, 1, 3, 2, 1],
            [3, 2, 1, 3, 3, 2, 1, 3, 3, 2, 1, 3, 0],
            [3, 3, 2, 1, 3, 3, 2, 1, 3, 3, 2, 1, 0],
            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2],
            [2, 2, 2, 2, 3, 3, 3, 3, 1, 1, 1, 1, 2],
            [3, 3, 3, 3, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 3],
            [2, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 3],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations2():
    ps = ParameterSet.create_from_parm_and_value_sizes(4, 3)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
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
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations3():
    ps = ParameterSet.create_from_parm_and_value_sizes(2, 3)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1],
            [2, 2],
            [3, 3],
            [2, 3],
            [3, 1],
            [1, 2],
            [3, 2],
            [1, 3],
            [2, 1],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations4():
    ps = ParameterSet.create_from_value_sizes([2, 3, 2])
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1],
            [1, 2, 2],
            [2, 1, 2],
            [2, 2, 1],
            [1, 3, 1],
            [2, 3, 2],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations5():
    ps = ParameterSet.create_from_parm_and_value_sizes(8, 2)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 2, 2, 1, 2, 2],
            [1, 2, 2, 1, 2, 2, 1, 2],
            [2, 1, 2, 2, 1, 2, 2, 1],
            [1, 1, 2, 2, 2, 2, 2, 2],
            [2, 2, 1, 1, 1, 2, 2, 2],
            [2, 2, 2, 2, 2, 1, 1, 1],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations6():
    ps = ParameterSet.create_from_value_sizes([2, 4, 2, 2])
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
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

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations7():
    ps = ParameterSet.create_from_parm_and_value_sizes(4, 6)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [6, 6, 6, 6],
            [3, 4, 5, 6],
            [4, 5, 6, 0],
            [5, 6, 0, 1],
            [6, 0, 1, 2],
            [0, 1, 2, 3],
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [6, 1, 3, 5],
            [0, 2, 4, 6],
            [1, 3, 5, 0],
            [2, 4, 6, 1],
            [3, 5, 0, 2],
            [4, 6, 1, 3],
            [5, 0, 2, 4],
            [2, 5, 1, 4],
            [3, 6, 2, 5],
            [4, 0, 3, 6],
            [5, 1, 4, 0],
            [6, 2, 5, 1],
            [0, 3, 6, 2],
            [1, 4, 0, 3],
            [5, 2, 6, 3],
            [6, 3, 0, 4],
            [0, 4, 1, 5],
            [1, 5, 2, 6],
            [2, 6, 3, 0],
            [3, 0, 4, 1],
            [4, 1, 5, 2],
            [1, 6, 4, 2],
            [2, 0, 5, 3],
            [3, 1, 6, 4],
            [4, 2, 0, 5],
            [5, 3, 1, 6],
            [6, 4, 2, 0],
            [0, 5, 3, 1],
            [4, 3, 2, 1],
            [5, 4, 3, 2],
            [6, 5, 4, 3],
            [0, 6, 5, 4],
            [1, 0, 6, 5],
            [2, 1, 0, 6],
            [3, 2, 1, 0],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations8():
    ps = ParameterSet.create_from_parm_and_value_sizes(9, 6)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 2, 2, 2, 2, 2, 2, 2, 2],
            [0, 3, 3, 3, 3, 3, 3, 3, 3],
            [0, 4, 4, 4, 4, 4, 4, 4, 4],
            [0, 5, 5, 5, 5, 5, 5, 5, 5],
            [0, 6, 6, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 1, 2, 3, 4, 5, 6],
            [0, 0, 0, 2, 1, 4, 3, 6, 5],
            [0, 1, 2, 0, 0, 5, 6, 3, 4],
            [0, 2, 1, 0, 0, 6, 5, 4, 3],
            [0, 3, 4, 5, 6, 0, 0, 1, 2],
            [0, 4, 3, 6, 5, 0, 0, 2, 1],
            [0, 5, 6, 3, 4, 1, 2, 0, 0],
            [0, 6, 5, 4, 3, 2, 1, 0, 0],
            [1, 0, 1, 3, 5, 2, 0, 6, 4],
            [1, 0, 2, 4, 6, 1, 0, 5, 3],
            [1, 1, 0, 5, 3, 0, 2, 4, 6],
            [1, 2, 0, 6, 4, 0, 1, 3, 5],
            [1, 3, 5, 0, 1, 6, 4, 2, 0],
            [1, 4, 6, 0, 2, 5, 3, 1, 0],
            [1, 5, 3, 1, 0, 4, 6, 0, 2],
            [1, 6, 4, 2, 0, 3, 5, 0, 1],
            [2, 0, 2, 5, 4, 6, 3, 0, 1],
            [2, 0, 1, 6, 3, 5, 4, 0, 2],
            [2, 1, 0, 3, 6, 4, 5, 2, 0],
            [2, 2, 0, 4, 5, 3, 6, 1, 0],
            [2, 3, 6, 1, 0, 2, 0, 4, 5],
            [2, 4, 5, 2, 0, 1, 0, 3, 6],
            [2, 5, 4, 0, 2, 0, 1, 6, 3],
            [2, 6, 3, 0, 1, 0, 2, 5, 4],
            [3, 0, 3, 2, 6, 5, 1, 4, 0],
            [3, 0, 4, 1, 5, 6, 2, 3, 0],
            [3, 1, 5, 0, 4, 3, 0, 6, 2],
            [3, 2, 6, 0, 3, 4, 0, 5, 1],
            [3, 3, 0, 6, 2, 1, 5, 0, 4],
            [3, 4, 0, 5, 1, 2, 6, 0, 3],
            [3, 5, 1, 4, 0, 0, 3, 2, 6],
            [3, 6, 2, 3, 0, 0, 4, 1, 5],
            [4, 0, 4, 0, 3, 1, 6, 2, 5],
            [4, 0, 3, 0, 4, 2, 5, 1, 6],
            [4, 1, 6, 2, 5, 0, 4, 0, 3],
            [4, 2, 5, 1, 6, 0, 3, 0, 4],
            [4, 3, 0, 4, 0, 5, 2, 6, 1],
            [4, 4, 0, 3, 0, 6, 1, 5, 2],
            [4, 5, 2, 6, 1, 3, 0, 4, 0],
            [4, 6, 1, 5, 2, 4, 0, 3, 0],
            [5, 0, 5, 6, 0, 4, 2, 1, 3],
            [5, 0, 6, 5, 0, 3, 1, 2, 4],
            [5, 1, 3, 4, 2, 6, 0, 0, 5],
            [5, 2, 4, 3, 1, 5, 0, 0, 6],
            [5, 3, 1, 2, 4, 0, 6, 5, 0],
            [5, 4, 2, 1, 3, 0, 5, 6, 0],
            [5, 5, 0, 0, 6, 2, 4, 3, 1],
            [5, 6, 0, 0, 5, 1, 3, 4, 2],
            [6, 0, 6, 4, 1, 0, 5, 3, 2],
            [6, 0, 5, 3, 2, 0, 6, 4, 1],
            [6, 1, 4, 6, 0, 2, 3, 5, 0],
            [6, 2, 3, 5, 0, 1, 4, 6, 0],
            [6, 3, 2, 0, 5, 4, 1, 0, 6],
            [6, 4, 1, 0, 6, 3, 2, 0, 5],
            [6, 5, 0, 2, 3, 6, 0, 1, 4],
            [6, 6, 0, 1, 4, 5, 0, 2, 3],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations9():
    ps = ParameterSet.create_from_parm_and_value_sizes(16, 2)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1],
            [2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
            [2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 0],
            [2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 0],
            [2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations10():
    ps = ParameterSet.create_from_parm_and_value_sizes(32, 2)
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
            ],
            [
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                1,
                1,
            ],
            [
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                1,
                1,
                1,
            ],
            [
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                2,
                2,
                1,
                0,
                0,
                0,
            ],
            [
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
            ],
            [
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                0,
                0,
                0,
            ],
            [
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                1,
            ],
            [
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                0,
            ],
            [
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                1,
            ],
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                2,
                2,
            ],
            [
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                1,
                2,
            ],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations11():
    ps = ParameterSet.create_from_value_sizes([6, 6, 8, 6])
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [6, 6, 6, 6],
            [0, 0, 7, 0],
            [4, 5, 6, 0],
            [5, 6, 7, 1],
            [6, 0, 1, 2],
            [0, 1, 2, 3],
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
            [0, 2, 4, 6],
            [1, 3, 5, 0],
            [2, 4, 6, 1],
            [3, 5, 7, 2],
            [4, 6, 1, 3],
            [5, 0, 2, 4],
            [6, 1, 3, 5],
            [3, 6, 2, 5],
            [4, 0, 3, 6],
            [5, 1, 4, 0],
            [6, 2, 5, 1],
            [0, 3, 6, 2],
            [1, 4, 7, 3],
            [2, 5, 1, 4],
            [6, 3, 7, 4],
            [0, 4, 1, 5],
            [1, 5, 2, 6],
            [2, 6, 3, 0],
            [3, 0, 4, 1],
            [4, 1, 5, 2],
            [5, 2, 6, 3],
            [2, 0, 5, 3],
            [3, 1, 6, 4],
            [4, 2, 7, 5],
            [5, 3, 1, 6],
            [6, 4, 2, 0],
            [0, 5, 3, 1],
            [1, 6, 4, 2],
            [5, 4, 3, 2],
            [6, 5, 4, 3],
            [0, 6, 5, 4],
            [1, 0, 6, 5],
            [2, 1, 7, 6],
            [3, 2, 1, 0],
            [4, 3, 2, 1],
            [1, 1, 8, 1],
            [2, 2, 8, 2],
            [3, 3, 8, 3],
            [4, 4, 8, 4],
            [5, 5, 8, 5],
            [6, 6, 8, 6],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)


def test_generate_configurations_web_example():
    ps = ParameterSet.create_from_value_sizes([3, 8, 2, 2])
    gen = RecursiveGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array(
        [
            [1, 1, 1, 1],
            [1, 2, 2, 2],
            [1, 3, 0, 0],
            [2, 1, 2, 0],
            [2, 2, 0, 1],
            [2, 3, 1, 2],
            [3, 1, 0, 2],
            [3, 2, 1, 0],
            [3, 3, 2, 1],
            [1, 4, 1, 1],
            [2, 4, 2, 2],
            [3, 4, 0, 0],
            [1, 5, 1, 1],
            [2, 5, 2, 2],
            [3, 5, 0, 0],
            [1, 6, 1, 1],
            [2, 6, 2, 2],
            [3, 6, 0, 0],
            [1, 7, 1, 1],
            [2, 7, 2, 2],
            [3, 7, 0, 0],
            [1, 8, 1, 1],
            [2, 8, 2, 2],
            [3, 8, 0, 0],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(cs, cs_expected)
