"""
Created on Sep 20, 2017

@author: Alan Williams
"""

import bisect
import math

# Array of prime numbers 1 <= p <= 101. Used for quick reference to avoid
# repeatedly finding prime numbers.
PRIME_ARRAY = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
]


# Array of prime powers numbers 1 <= p <= 101. Used for quick reference to
# avoid repeatedly finding prime powers.
PRIME_POWER_ARRAY = [
    2,
    3,
    4,
    5,
    7,
    8,
    9,
    11,
    13,
    16,
    17,
    19,
    23,
    25,
    27,
    29,
    31,
    32,
    37,
    41,
    43,
    47,
    49,
    53,
    59,
    61,
    64,
    67,
    71,
    73,
    79,
    81,
    83,
    89,
    97,
    101,
]

# Largest prime power that these utility methods can handle (i.e. N < 103^2).

LARGEST_PRIME_POWER = 10609

#   Returns true if the parameter is an integer power of a prime factor.


def is_prime_power(number):
    if number >= LARGEST_PRIME_POWER:
        raise ValueError(
            f"is_prime_power() cannot handle the value {number} "
            f"which is greater or equal to maximum value {LARGEST_PRIME_POWER}"
        )

    # Using table of prime numbers, check to see if our
    # original number is a prime, or prime power.

    if number in PRIME_ARRAY:
        return 1  # small prime

    for prime in PRIME_ARRAY:
        if number % prime == 0:
            # not prime
            log_value = math.log(number, prime)
            if abs(log_value - round(log_value)) < 0.000001:
                return prime  # prime power
            return 0  # composite

    return 1  # big prime


# Returns the next highest prime power >= number.


def find_next_prime_power(number):
    if number >= LARGEST_PRIME_POWER:
        raise ValueError(
            f"find_next_prime_power() cannot handle the value {number} "
            f"which is larger than {LARGEST_PRIME_POWER}"
        )

    # Do quick check when number <= 101

    if number <= 101:
        index = bisect.bisect_left(PRIME_POWER_ARRAY, number)
        if index != len(PRIME_POWER_ARRAY):
            return PRIME_POWER_ARRAY[index]
    raise ValueError("Out of range")
