"""
Created on Sep 26, 2017

@author: Alan Williams
"""

import numpy as np

from tconfig.core.data import DEFAULT_NDARRAY_TYPE
from tconfig.core.algorithms.recursive.field import Field
from tconfig.core.algorithms.recursive import utils


class LatinSquares(object):

    def __init__(self, square_size: int, dtype=DEFAULT_NDARRAY_TYPE):
        num_squares = 1
        if utils.is_prime_power(square_size) != 0:
            num_squares = square_size - 1
        self.squares = np.zeros((num_squares, square_size, square_size), dtype=dtype)
        if num_squares == 1:
            self.generate_single_square(square_size)
        else:
            self.generate_from_field(square_size)

    def __repr__(self) -> str:
        return f"LatinSquares(square_list={self.squares})"

    def __str__(self) -> str:
        return str(self.squares)

    def __eq__(self, other: 'LatinSquares') -> bool:
        return np.array_equal(self.squares, other.squares)

    def __hash__(self) -> int:
        return hash(self.squares)

    def generate_from_field(self, square_size: int):
        field = Field(square_size)
        num_squares = square_size - 1

        for square_num in range(0, num_squares):
            for row_index in range(0, square_size):
                row_result = field[square_num + 1] * field[row_index]
                for col_index in range(0, square_size):
                    end_result = row_result + field[col_index]
                    self.squares[square_num][row_index][col_index] = end_result.enumerate()

    def generate_single_square(self, square_size: int):
        for row_index in range(0, square_size):
            for col_index in range(0, square_size):
                self.squares[0][row_index][col_index] = (row_index + col_index) % square_size
