"""
Created on Sep 16, 2017

@author: Alan Williams
"""

from typing import Union, Optional


class IntMod(object):
    modulus = 0

    def __init__(self, value: Union[int, "IntMod"] = 0):
        self.value = value if IntMod.modulus == 0 else value % IntMod.modulus

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"IntMod(value={self.value})"

    def __eq__(self, operand: Optional["IntMod"]) -> bool:
        if operand is None:
            return False
        return self.value == operand.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __add__(self, operand: "IntMod") -> "IntMod":
        return IntMod(self.value + operand.value)

    def __sub__(self, operand: "IntMod") -> "IntMod":
        return IntMod(self.value - operand.value)

    def __mul__(self, operand: "IntMod") -> "IntMod":
        return IntMod(self.value * operand.value)

    def __floordiv__(self, operand: Union[int, "IntMod"]) -> "IntMod":
        if isinstance(operand, int):
            op_value = operand
        else:
            op_value = operand.value
        if op_value == 0:
            raise ZeroDivisionError
        if IntMod.modulus == 0:
            return IntMod(self.value // op_value)

        # The next section figures out if the modular division can be
        # performed.  To find ( l mod m ) / ( r mod m ), we need to find
        # what value of k gives a zero remainder for ( l + km ) / r, where
        # 0 <= k < m.  However, when m is not prime, not all values of r
        # will have inverses.  This will be detected if all possible values
        # of k leave remainders.

        # The algorithm below keeps adding 'm' to 'l', and repeats up to 'k'
        # times, which has the effect of trying each value of k.

        result_value = self.value  # holds current value of 'l + km'
        k = 0  # corresponds to 'k' above

        # Check for zero remainder, and k has not exceeded maximum

        while (result_value % op_value != 0) and (k < IntMod.modulus):
            result_value += IntMod.modulus  # add another 'm'
            k += 1

        # If no zero remainder for any value of k, then no inverse exists.

        if k >= IntMod.modulus:
            raise ArithmeticError(
                f"No inverse for {self.value} with modulus {IntMod.modulus}"
            )

        # We tested for no remainder above, so integer division with increased
        # value yields the result.

        return IntMod(result_value // op_value)

    def __iadd__(self, operand: Union[int, "IntMod"]) -> "IntMod":
        add_value = operand.value if isinstance(operand, IntMod) else operand
        if IntMod.modulus > 0:
            self.value = (self.value + add_value) % IntMod.modulus
        else:
            self.value += add_value
        return self
