"""
Created on Oct 4, 2017

@author: Alan Williams
"""

from tconfig.core.algorithms.ipo.ie import InteractionElement

# pylint: disable=invalid-name

COMMON_HASH_VALUE = 683845631297459348


def test_ie_eq():
    tv_dict = {1: 3, 2: 4, 4: 4}

    ie1 = InteractionElement(tv_dict)
    ie2 = InteractionElement(tv_dict)

    assert ie1 == ie2
    assert ie1 is not ie2

    tv_dict_2 = {1: 3, 4: 4}

    ie3 = InteractionElement(tv_dict_2)

    assert ie1 != ie3


def test_ie_get():
    ie = InteractionElement({1: 3, 2: 4, 4: 4})

    assert ie[1] == 3
    assert ie[2] == 4
    assert ie[4] == 4
    assert 3 not in ie


def test_ie_other():
    ie = InteractionElement({1: 3, 2: 4, 4: 4})
    other_ie = ie.get_ie_excepting_parm(2)

    ie_expected = InteractionElement({1: 3, 4: 4})
    assert ie_expected == other_ie

    assert len(ie) == 3
    assert 2 in ie
    assert ie[2] == 4

    assert 2 not in other_ie


def test_ie_str():
    ie = InteractionElement({1: 3, 2: 4, 4: 4})

    assert str(ie) == "{1: 3, 2: 4, 4: 4}"


def test_ie_repr():
    ie = InteractionElement({1: 3, 2: 4, 4: 4})

    assert repr(ie) == "InteractionElement(value_dict={1: 3, 2: 4, 4: 4})"


def test_ie_hash1():
    ie1 = InteractionElement({1: 2, 3: 4, 5: 6})
    ie2 = InteractionElement({1: 2, 5: 6, 3: 4})
    ie3 = InteractionElement({3: 4, 1: 2, 5: 6})
    ie4 = InteractionElement({3: 4, 5: 6, 1: 2})
    ie5 = InteractionElement({5: 6, 1: 2, 3: 4})
    ie6 = InteractionElement({5: 6, 3: 4, 1: 2})

    h1 = hash(ie1)
    h2 = hash(ie2)
    h3 = hash(ie3)
    h4 = hash(ie4)
    h5 = hash(ie5)
    h6 = hash(ie6)

    assert h1 == COMMON_HASH_VALUE
    assert h2 == COMMON_HASH_VALUE
    assert h3 == COMMON_HASH_VALUE
    assert h4 == COMMON_HASH_VALUE
    assert h5 == COMMON_HASH_VALUE
    assert h6 == COMMON_HASH_VALUE


def test_ie_hash2():
    ie1 = InteractionElement({1: 2, 3: 4, 5: 6})
    ie2 = InteractionElement({7: 8, 9: 10, 11: 12})
    ie3 = InteractionElement({13: 14, 15: 16, 17: 18})

    set1 = {ie1, ie2, ie3}
    ie4 = InteractionElement({7: 8, 9: 10, 11: 12})
    ie5 = InteractionElement({1: 2, 3: 4, 5: 6})
    set2 = {ie4, ie5}

    set1 = set1 - set2

    assert set1 == {ie3}


def test_ie_hash3():
    ie = InteractionElement({1: 2, 3: 4})

    # noinspection PyUnusedLocal
    h1 = hash(ie)  # pylint: disable=unused-variable
    ie[5] = 6
    h2 = hash(ie)

    assert h2 == COMMON_HASH_VALUE
