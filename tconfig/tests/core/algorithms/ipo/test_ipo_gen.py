"""
Created on Oct 7, 2017

@author: Alan Williams
"""

import numpy as np

from tconfig.core.data import ParameterSet
from tconfig.core.data import DEFAULT_NDARRAY_TYPE
from tconfig.core.algorithms.ipo import InteractionElement
from tconfig.core.algorithms.ipo import IpoGenerator


# pylint: disable=invalid-name, missing-function-docstring

def test_add_new_test():
    cs = np.array([1, 2, 3, 4], dtype=DEFAULT_NDARRAY_TYPE)

    pkw = InteractionElement({0: 2, 1: 3, 2: 4})

    piu = InteractionElement({3: 5})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)

    cs_new = g.add_new_test(cs, pkw, piu)

    cs_expected = np.array([[1, 2, 3, 4], [2, 3, 4, 5]], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(cs_new, cs_expected)


def test_is_zero_1():
    cs = np.array([[1, 0, 3, 0]], dtype=DEFAULT_NDARRAY_TYPE)

    pkw = InteractionElement({1: 2, 3: 4})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)

    assert g.is_zero(cs[0], pkw)


def test_is_zero_2():
    cs = np.array([[1, 2, 3, 4]], dtype=DEFAULT_NDARRAY_TYPE)

    pkw = InteractionElement({1: 2, 3: 4})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)

    assert g.is_zero(cs[0], pkw)


def test_is_zero_3():
    cs = np.array([[1, 2, 3, 4]], dtype=DEFAULT_NDARRAY_TYPE)

    pkw = InteractionElement({1: 2, 3: 5})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)

    assert not g.is_zero(cs[0], pkw)


def test_contains_dash_in_t_1():
    cs1 = np.array([[1, 0, 3, 0], [2, 0, 4, 2]], dtype=DEFAULT_NDARRAY_TYPE)
    cs2 = None

    pkw = InteractionElement({0: 1, 1: 2})
    piu = InteractionElement({3: 2})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)
    g.test_set = cs1

    assert g.contains_dash_in_t(cs2, pkw, piu) == 0


def test_contains_dash_in_t_2():
    cs1 = np.array([[2, 0, 4, 2]], dtype=DEFAULT_NDARRAY_TYPE)
    cs2 = np.array([[1, 0, 3, 2]], dtype=DEFAULT_NDARRAY_TYPE)

    pkw = InteractionElement({0: 1, 1: 2})
    piu = InteractionElement({3: 2})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)
    g.test_set = cs1

    assert g.contains_dash_in_t(cs2, pkw, piu) == 1


def test_contains_dash_in_t_3():
    cs1 = np.array([[4, 4, 4, 4], [3, 3, 3, 3]], dtype=DEFAULT_NDARRAY_TYPE)
    cs2 = None

    pkw = InteractionElement({0: 1, 1: 2})
    piu = InteractionElement({3: 2})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)
    g.test_set = cs1

    assert g.contains_dash_in_t(cs2, pkw, piu) == -1


def test_contains_dash_in_t_4():
    cs1 = np.array([[4, 4, 4, 4]], dtype=DEFAULT_NDARRAY_TYPE)
    cs2 = np.array([[3, 3, 3, 3]], dtype=DEFAULT_NDARRAY_TYPE)

    pkw = InteractionElement({0: 1, 1: 2})
    piu = InteractionElement({3: 2})

    ps = ParameterSet.create_from_parm_and_value_sizes(13, 4)
    g = IpoGenerator(ps, 2)
    g.test_set = cs1

    assert g.contains_dash_in_t(cs2, pkw, piu) == -1


def test_first_parameters():
    ps = ParameterSet.create_from_parm_and_value_sizes(13, 3)
    g = IpoGenerator(ps, 2)
    g.first_parameters()

    cs_expected = np.array([
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 2],
        [2, 3],
        [3, 1],
        [3, 2],
        [3, 3],
    ], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(g.test_set, cs_expected)


def test_get_hori_recur_1():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 2)
    g = IpoGenerator(ps, 3)
    g.first_parameters()

    tva = InteractionElement({2: 1, 4: 2})

    pi = set()
    g.get_hori_recur(4, 1, pi, tva)

    ie1 = InteractionElement({2: 1, 3: 2, 4: 2})
    ie2 = InteractionElement({2: 1, 3: 1, 4: 2})
    ie3 = InteractionElement({1: 2, 2: 1, 4: 2})
    ie4 = InteractionElement({1: 1, 2: 1, 4: 2})
    ie5 = InteractionElement({0: 1, 2: 1, 4: 2})
    ie6 = InteractionElement({0: 1, 2: 1, 4: 2})

    assert len(pi) == 6
    assert ie1 in pi
    assert ie2 in pi
    assert ie3 in pi
    assert ie4 in pi
    assert ie5 in pi
    assert ie6 in pi


def test_get_hori_recur_2():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 2)
    g = IpoGenerator(ps, 4)
    g.first_parameters()

    tva = InteractionElement({2: 1, 4: 2})

    pi = set()
    g.get_hori_recur(4, 2, pi, tva)

    ie1 = InteractionElement({1: 1, 2: 1, 3: 1, 4: 2})
    ie2 = InteractionElement({1: 1, 2: 1, 3: 2, 4: 2})
    ie3 = InteractionElement({1: 2, 2: 1, 3: 1, 4: 2})
    ie4 = InteractionElement({1: 2, 2: 1, 3: 2, 4: 2})
    ie5 = InteractionElement({0: 1, 1: 1, 2: 1, 4: 2})
    ie6 = InteractionElement({0: 1, 1: 2, 2: 1, 4: 2})
    ie7 = InteractionElement({0: 2, 1: 1, 2: 1, 4: 2})
    ie8 = InteractionElement({0: 2, 1: 2, 2: 1, 4: 2})
    ie9 = InteractionElement({0: 1, 2: 1, 3: 1, 4: 2})
    ie10 = InteractionElement({0: 1, 2: 1, 3: 2, 4: 2})
    ie11 = InteractionElement({0: 2, 2: 1, 3: 1, 4: 2})
    ie12 = InteractionElement({0: 2, 2: 1, 3: 2, 4: 2})

    assert len(pi) == 12
    assert ie1 in pi
    assert ie2 in pi
    assert ie3 in pi
    assert ie4 in pi
    assert ie5 in pi
    assert ie6 in pi
    assert ie7 in pi
    assert ie8 in pi
    assert ie9 in pi
    assert ie10 in pi
    assert ie11 in pi
    assert ie12 in pi


def test_pairs_covered_in_1():
    ps = ParameterSet.create_from_value_sizes([2, 2, 3, 2])
    g = IpoGenerator(ps, 2)

    cs = np.array([[1, 2, 3]], dtype=DEFAULT_NDARRAY_TYPE)
    g.test_set = cs

    ie1 = InteractionElement({0: 1, 3: 1})
    ie2 = InteractionElement({1: 2, 3: 1})
    ie3 = InteractionElement({2: 3, 3: 1})
    ie4 = InteractionElement({0: 2, 3: 1})
    ie5 = InteractionElement({1: 1, 3: 1})

    s = {ie1, ie2, ie3, ie4, ie5}

    s2 = g.pairs_covered_in(s, 0, 3, 1)

    assert len(s2) == 3
    assert ie1 in s2
    assert ie2 in s2
    assert ie3 in s2


def test_pairs_covered_in_2():
    ps = ParameterSet.create_from_value_sizes([2, 2, 3, 2])
    g = IpoGenerator(ps, 2)

    cs = np.array([[1, 2, 3]], dtype=DEFAULT_NDARRAY_TYPE)
    g.test_set = cs

    ie1 = InteractionElement({2: 3, 3: 1})
    ie2 = InteractionElement({0: 2, 3: 1})
    ie3 = InteractionElement({1: 1, 3: 1})

    s = {ie1, ie2, ie3}

    s2 = g.pairs_covered_in(s, 0, 3, 1)

    assert len(s2) == 1
    assert ie1 in s2


def test_do_horizontal_growth_1():
    ps = ParameterSet.create_from_parm_and_value_sizes(13, 3)
    g = IpoGenerator(ps, 2)
    g.first_parameters()
    actual = g.do_horizontal_growth(2)

    assert len(g.test_set[0]) == 3
    assert len(g.test_set) == 9

    assert len(actual) == 2
    ie1 = InteractionElement({1: 2, 2: 3})
    ie2 = InteractionElement({0: 2, 2: 3})
    assert ie1 in actual
    assert ie2 in actual


def test_do_horizontal_growth_2():
    ps = ParameterSet.create_from_value_sizes([2, 2, 5])
    g = IpoGenerator(ps, 2)
    g.first_parameters()
    actual = g.do_horizontal_growth(2)

    assert len(actual) == 12
    ie1 = InteractionElement({1: 1, 2: 5})
    ie2 = InteractionElement({1: 2, 2: 5})
    ie3 = InteractionElement({0: 1, 2: 5})
    ie4 = InteractionElement({0: 2, 2: 1})
    ie5 = InteractionElement({0: 2, 2: 2})
    ie6 = InteractionElement({1: 1, 2: 2})
    ie7 = InteractionElement({0: 2, 2: 5})
    ie8 = InteractionElement({1: 2, 2: 1})
    ie9 = InteractionElement({0: 1, 2: 3})
    ie10 = InteractionElement({1: 2, 2: 3})
    ie11 = InteractionElement({0: 1, 2: 4})
    ie12 = InteractionElement({1: 1, 2: 4})
    assert ie1 in actual
    assert ie2 in actual
    assert ie3 in actual
    assert ie4 in actual
    assert ie5 in actual
    assert ie6 in actual
    assert ie7 in actual
    assert ie8 in actual
    assert ie9 in actual
    assert ie10 in actual
    assert ie11 in actual
    assert ie12 in actual


def test_do_vertical_growth():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 3)
    g = IpoGenerator(ps, 2)
    g.first_parameters()
    s = g.do_horizontal_growth(2)
    cs = g.do_vertical_growth(s, 2)

    assert len(cs) == 1

    cs_expected = np.array([[2, 2, 3]], dtype=DEFAULT_NDARRAY_TYPE)
    assert np.array_equal(cs, cs_expected)


def test_get_test_value_recur_1():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 2)
    g = IpoGenerator(ps, 3)
    cs = np.array([
        [1, 1, 1, 1],
        [1, 1, 2, 0],
        [1, 2, 1, 0],
        [1, 2, 2, 0],
        [2, 1, 1, 0],
        [2, 1, 2, 0],
        [2, 2, 1, 0],
        [2, 2, 2, 0],
    ], dtype=DEFAULT_NDARRAY_TYPE)
    g.test_set = cs

    orig_set = set()
    orig_set.add(InteractionElement({0: 2, 2: 2, 3: 2}))
    orig_set.add(InteractionElement({1: 2, 2: 1, 3: 2}))
    orig_set.add(InteractionElement({0: 1, 2: 1, 3: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 3: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 3: 2}))
    orig_set.add(InteractionElement({1: 2, 2: 2, 3: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 3: 1}))
    orig_set.add(InteractionElement({1: 2, 2: 2, 3: 1}))
    orig_set.add(InteractionElement({1: 1, 2: 2, 3: 2}))
    orig_set.add(InteractionElement({1: 1, 2: 2, 3: 1}))
    orig_set.add(InteractionElement({0: 2, 2: 1, 3: 2}))
    orig_set.add(InteractionElement({0: 2, 2: 1, 3: 1}))
    orig_set.add(InteractionElement({0: 1, 2: 1, 3: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 3: 2}))
    orig_set.add(InteractionElement({0: 2, 2: 2, 3: 1}))
    orig_set.add(InteractionElement({1: 2, 2: 1, 3: 1}))
    orig_set.add(InteractionElement({0: 1, 2: 2, 3: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 3: 2}))
    orig_set.add(InteractionElement({1: 1, 2: 1, 3: 2}))
    orig_set.add(InteractionElement({0: 1, 2: 2, 3: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 3: 1}))
    orig_set.add(InteractionElement({1: 1, 2: 1, 3: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 3: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 3: 1}))

    config_num = 0
    parm_num = 3
    cover = 1
    test_value_list = InteractionElement({0: 1, 3: 1})
    actual = set()

    g.get_test_value_recur(
        orig_set, config_num, parm_num, cover, actual, test_value_list)

    expected = set()
    expected.add(InteractionElement({0: 1, 2: 1, 3: 1}))
    expected.add(InteractionElement({0: 1, 1: 1, 3: 1}))

    assert actual == expected


def test_get_test_value_recur_2():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 2)
    g = IpoGenerator(ps, 4)
    cs = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2, 0],
        [1, 1, 2, 1, 0],
        [1, 1, 2, 2, 0],
        [1, 2, 1, 1, 0],
        [1, 2, 1, 2, 0],
        [1, 2, 2, 1, 0],
        [1, 2, 2, 2, 0],
        [2, 1, 1, 1, 0],
        [2, 1, 1, 2, 0],
        [2, 1, 2, 1, 0],
        [2, 1, 2, 2, 0],
        [2, 2, 1, 1, 0],
        [2, 2, 1, 2, 0],
        [2, 2, 2, 1, 0],
        [2, 2, 2, 2, 0],
    ], dtype=DEFAULT_NDARRAY_TYPE)
    g.test_set = cs

    orig_set = set()
    orig_set.add(InteractionElement({1: 1, 2: 2, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 2: 2, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 2: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 2: 2, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 2: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 2: 2, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 2: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 2: 2, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 2: 1, 4: 2}))
    orig_set.add(InteractionElement({1: 2, 2: 1, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({1: 1, 2: 2, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({1: 1, 2: 2, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({1: 2, 2: 1, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 2: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 2: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 2: 2, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 2: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 2: 1, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 2: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 2: 2, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 2: 1, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({1: 2, 2: 2, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({1: 1, 2: 2, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({1: 2, 2: 2, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 2: 1, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 2: 1, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 2: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 2: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 2: 1, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 2: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 2: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 2: 1, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({1: 1, 2: 1, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({1: 2, 2: 2, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({1: 2, 2: 2, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({1: 1, 2: 1, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 2: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 1: 1, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 1: 2, 2: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 2: 2, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({0: 1, 2: 1, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 2: 2, 4: 1}))
    orig_set.add(InteractionElement({0: 2, 2: 2, 3: 1, 4: 1}))
    orig_set.add(InteractionElement({0: 1, 2: 1, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 1, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({0: 2, 1: 2, 2: 2, 4: 2}))
    orig_set.add(InteractionElement({1: 2, 2: 1, 3: 2, 4: 2}))
    orig_set.add(InteractionElement({1: 2, 2: 1, 3: 2, 4: 1}))
    orig_set.add(InteractionElement({1: 1, 2: 1, 3: 1, 4: 2}))
    orig_set.add(InteractionElement({1: 1, 2: 1, 3: 1, 4: 1}))

    config_num = 0
    parm_num = 4
    cover = 2
    test_value_list = InteractionElement({0: 1, 4: 1})
    actual = set()

    g.get_test_value_recur(
        orig_set, config_num, parm_num, cover, actual, test_value_list)

    expected = set()
    expected.add(InteractionElement({0: 1, 1: 1, 3: 1, 4: 1}))
    expected.add(InteractionElement({0: 1, 1: 1, 2: 1, 4: 1}))
    expected.add(InteractionElement({0: 1, 2: 1, 3: 1, 4: 1}))
    assert actual == expected


def test_ipo_generate_1():
    ps = ParameterSet.create_from_parm_and_value_sizes(4, 2)
    gen = IpoGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array([
        [1, 1, 1, 1],
        [1, 2, 2, 2],
        [2, 1, 2, 1],
        [2, 2, 1, 2],
        [0, 2, 0, 1],
        [0, 1, 0, 2],
    ], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(cs, cs_expected)


def test_ipo_generate_2():
    ps = ParameterSet.create_from_parm_and_value_sizes(2, 2)
    gen = IpoGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array([
        [1, 1],
        [1, 2],
        [2, 1],
        [2, 2],
    ], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(cs, cs_expected)


def test_ipo_generate_3():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 3)
    gen = IpoGenerator(ps, 2)
    cs = gen.generate_covering_array()

    cs_expected = np.array([
        [1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2],
        [1, 3, 3, 3, 3],
        [2, 1, 2, 3, 1],
        [2, 2, 1, 1, 3],
        [2, 3, 1, 2, 2],
        [3, 1, 3, 2, 1],
        [3, 2, 1, 3, 2],
        [3, 3, 2, 1, 3],
        [2, 2, 3, 1, 2],
        [0, 1, 0, 2, 3],
        [0, 3, 0, 0, 1],
        [0, 2, 0, 0, 1],
        [0, 1, 0, 0, 2],
    ], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(cs, cs_expected)


'''
    @Test
    public void testDoHorizontalGrowth3( )
    {
        Parameter p1 = new ParameterImpl( "P1", 3 );
        Parameter p2 = new ParameterImpl( "P2", 3 );
        Parameter p3 = new ParameterImpl( "P3", 3 );
        ParameterSetX ps = new ParameterSetImpl( );
        ps.addParameter( p1 );
        ps.addParameter( p2 );
        ps.addParameter( p3 );

        ps.setAdjacent( 0, 1, false );

        IPOGenerator g = new IPOGenerator( ps, 2 );
        g.firstParameters( );

        Set<InteractionElement> result = g.doHorizontalGrowth( 2 );

        int szExpected = 0;
        int szActual = result.size( );
        Assert.assertEquals( szExpected, szActual );
    }
'''


def test_ipo_generate_4():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 2)
    gen = IpoGenerator(ps, 3)
    cs = gen.generate_covering_array()

    cs_expected = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 2, 2, 2],
        [1, 2, 1, 2, 1],
        [1, 2, 2, 1, 2],
        [2, 1, 1, 2, 2],
        [2, 1, 2, 1, 1],
        [2, 2, 1, 1, 2],
        [2, 2, 2, 2, 1],
        [1, 1, 1, 1, 2],
        [1, 2, 2, 1, 1],
        [2, 2, 2, 2, 2],
        [2, 1, 1, 2, 1],
    ], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(cs, cs_expected)


def test_ipo_generate_5():
    ps = ParameterSet.create_from_parm_and_value_sizes(5, 2)
    gen = IpoGenerator(ps, 4)
    cs = gen.generate_covering_array()

    cs_expected = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2, 2],
        [1, 1, 2, 1, 2],
        [1, 1, 2, 2, 1],
        [1, 2, 1, 1, 2],
        [1, 2, 1, 2, 1],
        [1, 2, 2, 1, 1],
        [1, 2, 2, 2, 2],
        [2, 1, 1, 1, 2],
        [2, 1, 1, 2, 1],
        [2, 1, 2, 1, 1],
        [2, 1, 2, 2, 2],
        [2, 2, 1, 1, 1],
        [2, 2, 1, 2, 2],
        [2, 2, 2, 1, 2],
        [2, 2, 2, 2, 1],
    ], dtype=DEFAULT_NDARRAY_TYPE)

    assert np.array_equal(cs, cs_expected)
