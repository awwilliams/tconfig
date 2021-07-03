"""
Created on Sep 28, 2017

@author: Alan Williams
"""

import numpy as np

from tconfig.core.algorithms.generator import DEFAULT_NDARRAY_TYPE
from tconfig.core.algorithms.recursive.orthog import OrthogonalArrayGenerator


# pylint: disable=invalid-name


def test_generate_oa_has_field():
    oa_gen = OrthogonalArrayGenerator(
        num_values=3, degree=2, dtype=DEFAULT_NDARRAY_TYPE
    )
    oa = oa_gen.generate_oa()
    oa_expected = np.array(
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

    assert np.array_equal(oa, oa_expected)


def test_generate_oa_no_field():
    oa_gen = OrthogonalArrayGenerator(
        num_values=6, degree=2, dtype=DEFAULT_NDARRAY_TYPE
    )
    oa = oa_gen.generate_oa()
    oa_expected = np.array(
        [
            [1, 1, 1],
            [1, 2, 2],
            [1, 3, 3],
            [1, 4, 4],
            [1, 5, 5],
            [1, 6, 6],
            [2, 1, 2],
            [2, 2, 3],
            [2, 3, 4],
            [2, 4, 5],
            [2, 5, 6],
            [2, 6, 1],
            [3, 1, 3],
            [3, 2, 4],
            [3, 3, 5],
            [3, 4, 6],
            [3, 5, 1],
            [3, 6, 2],
            [4, 1, 4],
            [4, 2, 5],
            [4, 3, 6],
            [4, 4, 1],
            [4, 5, 2],
            [4, 6, 3],
            [5, 1, 5],
            [5, 2, 6],
            [5, 3, 1],
            [5, 4, 2],
            [5, 5, 3],
            [5, 6, 4],
            [6, 1, 6],
            [6, 2, 1],
            [6, 3, 2],
            [6, 4, 3],
            [6, 5, 4],
            [6, 6, 5],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(oa, oa_expected)


def test_basic_array_repeat():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    ba = oa_gen.basic_array(repeat_factor=2)
    ba_expected = np.array(
        [
            [1, 1, 2, 2, 2, 2, 2, 2],
            [1, 1, 3, 3, 3, 3, 3, 3],
            [2, 2, 1, 1, 2, 2, 3, 3],
            [2, 2, 2, 2, 3, 3, 1, 1],
            [2, 2, 3, 3, 1, 1, 2, 2],
            [3, 3, 1, 1, 3, 3, 2, 2],
            [3, 3, 2, 2, 1, 1, 3, 3],
            [3, 3, 3, 3, 2, 2, 1, 1],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(ba, ba_expected)


def test_basic_array_no_repeat():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    ba = oa_gen.basic_array(repeat_factor=1)
    ba_expected = np.array(
        [
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

    assert np.array_equal(ba, ba_expected)


def test_reduced_array_repeat():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    ra = oa_gen.reduced_array(repeat_factor=2)
    ra_expected = np.array(
        [
            [1, 1, 2, 2, 3, 3],
            [2, 2, 3, 3, 1, 1],
            [3, 3, 1, 1, 2, 2],
            [1, 1, 3, 3, 2, 2],
            [2, 2, 1, 1, 3, 3],
            [3, 3, 2, 2, 1, 1],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(ra, ra_expected)


def test_reduced_array_no_repeat():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    ra = oa_gen.reduced_array(repeat_factor=1)
    ra_expected = np.array(
        [
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2],
            [1, 3, 2],
            [2, 1, 3],
            [3, 2, 1],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(ra, ra_expected)


def test_two_to_n_block():
    oa_gen = OrthogonalArrayGenerator(
        num_values=3, degree=2, dtype=DEFAULT_NDARRAY_TYPE
    )
    ttn = oa_gen.two_to_n_block(repeat_factor=4)
    ttn_expected = np.array(
        [
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [3, 3, 3, 3],
            [3, 3, 3, 3],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(ttn, ttn_expected)


def test_oversized_parameter():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    op = oa_gen.oversized_parameter(6, 7, 12, 3)
    op_expected = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3],
            [1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3],
            [1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 6, 3, 3, 3, 3],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(op, op_expected)


def test_oversized_parameter_2():
    oa_gen = OrthogonalArrayGenerator(num_values=6, dtype=DEFAULT_NDARRAY_TYPE)
    op = oa_gen.oversized_parameter(8, 0, 4, 6)
    op_expected = np.array(
        [
            [7, 1, 1, 1],
            [7, 2, 2, 2],
            [7, 3, 3, 3],
            [7, 4, 4, 4],
            [7, 5, 5, 5],
            [7, 6, 6, 6],
            [8, 1, 1, 1],
            [8, 2, 2, 2],
            [8, 3, 3, 3],
            [8, 4, 4, 4],
            [8, 5, 5, 5],
            [8, 6, 6, 6],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(op, op_expected)


def test_oversized_parameter_3():
    oa_gen = OrthogonalArrayGenerator(num_values=7, dtype=DEFAULT_NDARRAY_TYPE)
    op = oa_gen.oversized_parameter(8, 6, 8, 6)
    op_expected = np.array(
        [
            [1, 1, 1, 1, 1, 1, 8, 1],
            [2, 2, 2, 2, 2, 2, 8, 2],
            [3, 3, 3, 3, 3, 3, 8, 3],
            [4, 4, 4, 4, 4, 4, 8, 4],
            [5, 5, 5, 5, 5, 5, 8, 5],
            [6, 6, 6, 6, 6, 6, 8, 6],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(op, op_expected)


def test_extra_parameter_block():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    epb = oa_gen.extra_parameter_block(3, 4)
    epb_expected = np.array(
        [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(epb, epb_expected)


def test_extra_parameter_block_2():
    oa_gen = OrthogonalArrayGenerator(num_values=3, dtype=DEFAULT_NDARRAY_TYPE)
    epb = oa_gen.extra_parameter_block(8, 4)
    epb_expected = np.array(
        [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ],
        dtype=DEFAULT_NDARRAY_TYPE,
    )

    assert np.array_equal(epb, epb_expected)
