"""
Created on Sep 27, 2017

@author: Alan Williams
"""

from typing import Optional
import numpy as np

from tconfig.core.data import DEFAULT_NDARRAY_TYPE
from tconfig.core.algorithms.recursive import utils
from tconfig.core.algorithms.recursive.latin import LatinSquares


class OrthogonalArrayGenerator(object):

    def __init__(self, num_values, degree: int = 2, dtype=DEFAULT_NDARRAY_TYPE):
        self.num_values = num_values
        self.degree = degree
        self.ndarray_type = dtype

    def generate_oa(self) -> np.ndarray:
        squares = LatinSquares(self.num_values, dtype=self.ndarray_type).squares
        num_parms = self.num_values + 1 if utils.is_prime_power(self.num_values) else 3
        num_configs = self.num_values ** self.degree
        result = np.empty((num_configs, num_parms), dtype=self.ndarray_type)
        for config_index in range(0, num_configs):
            matrix_row = config_index // self.num_values
            matrix_col = config_index % self.num_values
            result[config_index][0] = matrix_row + 1
            result[config_index][1] = matrix_col + 1
            for parm_index in range(2, num_parms):
                result[config_index][parm_index] = 1 + \
                                                   squares[parm_index - 2][matrix_row][matrix_col]
        return result

    def basic_array(self, repeat_factor: int) -> np.ndarray:
        orthogonal_array = self.generate_oa()
        return orthogonal_array[1:, :].repeat(repeat_factor, axis=1)

    def reduced_array(self, repeat_factor: int) -> np.ndarray:
        orthogonal_array = self.generate_oa()
        return orthogonal_array[self.num_values:, 1:].repeat(repeat_factor, axis=1)

    def two_to_n_block(self, repeat_factor: int = 0) -> Optional[np.ndarray]:
        if repeat_factor < 1:
            return None
        block_size = self.num_values ** (self.degree - 1)
        return np.vstack([np.full((block_size, repeat_factor), value, dtype=self.ndarray_type)
                          for value in range(2, self.num_values + 1)])

    def oversized_parameter(self,
                            max_values: int, parm_index: int, num_parms: int,
                            second_max: int) -> Optional[np.ndarray]:
        if max_values <= self.num_values:
            return None

        result = np.vstack([
            np.insert(
                np.arange(1, second_max + 1).reshape((second_max, 1)).repeat(num_parms - 1, axis=1),
                parm_index,
                oversize_value,
                axis=1)
            for oversize_value in range(self.num_values + 1, max_values + 1)
        ])
        return result

    def extra_parameter_block(self, num_configs: int, num_parms: int) -> np.ndarray:
        start_ones_block = np.ones((self.num_values, num_parms), dtype=self.ndarray_type)

        ones_row = np.ones((1, num_parms), dtype=self.ndarray_type)
        zeros_block = np.zeros((self.num_values - 1, num_parms), dtype=self.ndarray_type)
        block = np.concatenate((ones_row, zeros_block))

        result = start_ones_block
        while result.shape[0] < num_configs:
            result = np.concatenate((result, block))
        return result[:num_configs]
