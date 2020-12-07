"""
Created on Jun. 14, 2020

@author: Alan Williams
"""
import re
import pytest

from tconfig.core.algorithms.recursive.utils import is_prime_power, find_next_prime_power


def test_is_prime_power_small_prime():
    value = 29
    assert is_prime_power(value) == 1


def test_is_prime_power_big_prime():
    value = 197
    assert is_prime_power(value) == 1


def test_is_prime_power_bigger_prime():
    value = 10243
    assert is_prime_power(value) == 1


def test_is_prime_power_really_big_prime():
    value = 11113
    error_message = re.escape(" ".join([
        "is_prime_power() cannot handle the value 11113",
        "which is greater or equal to maximum value 10609"
    ]))
    with pytest.raises(ValueError, match=error_message):
        is_prime_power(value)


def test_find_next_prime_power_small_prime():
    value = 28
    assert find_next_prime_power(value) == 29


def test_find_next_prime_power_big_prime():
    value = 100
    assert find_next_prime_power(value) == 101


def test_find_next_prime_power_biggest_prime():
    value = 101
    assert find_next_prime_power(value) == 101


def test_find_next_prime_power_too_big_prime():
    value = 102
    with pytest.raises(ValueError, match="Out of range"):
        find_next_prime_power(value)
