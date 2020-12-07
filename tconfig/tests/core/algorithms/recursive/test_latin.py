"""
Created on Sep 26, 2017

@author: Alan Williams
"""

import numpy as np
from tconfig.core.algorithms.generator import DEFAULT_NDARRAY_TYPE
from tconfig.core.algorithms.recursive.latin import LatinSquares


# pylint: disable=invalid-name

def test_prime_order():
    sq = LatinSquares(5).squares
    sq_expected = np.empty((4, 5, 5), dtype=DEFAULT_NDARRAY_TYPE)
    sq_expected[0] = [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 0],
        [2, 3, 4, 0, 1],
        [3, 4, 0, 1, 2],
        [4, 0, 1, 2, 3],
    ]
    sq_expected[1] = [
        [0, 1, 2, 3, 4],
        [2, 3, 4, 0, 1],
        [4, 0, 1, 2, 3],
        [1, 2, 3, 4, 0],
        [3, 4, 0, 1, 2],
    ]
    sq_expected[2] = [
        [0, 1, 2, 3, 4],
        [3, 4, 0, 1, 2],
        [1, 2, 3, 4, 0],
        [4, 0, 1, 2, 3],
        [2, 3, 4, 0, 1],
    ]
    sq_expected[3] = [
        [0, 1, 2, 3, 4],
        [4, 0, 1, 2, 3],
        [3, 4, 0, 1, 2],
        [2, 3, 4, 0, 1],
        [1, 2, 3, 4, 0],
    ]

    assert np.array_equal(sq, sq_expected)


def test_prime_power_order():
    sq = LatinSquares(4).squares
    sq_expected = np.empty((3, 4, 4), dtype=DEFAULT_NDARRAY_TYPE)
    sq_expected[0] = [
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
        [3, 2, 1, 0],
    ]
    sq_expected[1] = [
        [0, 1, 2, 3],
        [2, 3, 0, 1],
        [3, 2, 1, 0],
        [1, 0, 3, 2],
    ]
    sq_expected[2] = [
        [0, 1, 2, 3],
        [3, 2, 1, 0],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
    ]

    assert np.array_equal(sq, sq_expected)


def test_other_order():
    sq = LatinSquares(6).squares
    sq_expected = np.empty((1, 6, 6), dtype=DEFAULT_NDARRAY_TYPE)
    sq_expected[0] = [
        [0, 1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 0],
        [2, 3, 4, 5, 0, 1],
        [3, 4, 5, 0, 1, 2],
        [4, 5, 0, 1, 2, 3],
        [5, 0, 1, 2, 3, 4],
    ]
    assert np.array_equal(sq, sq_expected)
