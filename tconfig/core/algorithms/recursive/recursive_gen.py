"""
Created on Sep 30, 2017

@author: Alan Williams
"""

import math
from typing import Optional
import numpy as np

from tconfig.core.data.parmset import ParameterSet
from tconfig.core.algorithms.generator import Generator, DEFAULT_NDARRAY_TYPE

from tconfig.core.algorithms.recursive.orthog import OrthogonalArrayGenerator
from tconfig.core.algorithms.recursive import utils


class RecursiveGenerator(Generator):

    def __init__(self, parameter_set: ParameterSet, coverage_degree: int = 2, *,
                 dtype=DEFAULT_NDARRAY_TYPE, existing_configs: Optional[np.ndarray] = None):
        super().__init__(parameter_set, coverage_degree,
                         dtype=dtype, existing_configs=existing_configs)

        assert self.num_parms >= 2

        self.square_size = 0
        self.num_rounds = 0
        self.round_group_size = []
        self.group_repeat_factor = []
        self.num_configs_per_round = []
        self.extra_parms_per_round = []
        self.extra_parms_repeat_factor = []

        self.max_num_values = max(self.num_values_per_parm)
        self.max_index = self.num_values_per_parm.index(self.max_num_values)
        self.second_max_num_values = sorted(self.num_values_per_parm)[-2]

    def generate_covering_array(self) -> np.ndarray:
        self.determine_square_setup()
        self.determine_round_groupings()
        return self.build_configurations()

    def determine_square_setup(self):
        if self.num_parms <= 3:
            self.num_rounds = 1
            self.square_size = self.second_max_num_values
        else:
            self.square_size = utils.find_next_prime_power(
                self.second_max_num_values)
            max_parms = self.square_size + 1
            self.num_rounds = math.ceil(
                math.log(self.num_parms, max_parms))
            if self.num_rounds == 2:
                if self.num_parms > max_parms * (max_parms - 1):
                    num_configs_v1 = 2 * self.square_size ** self.coverage_degree - 1
                else:
                    num_configs_v1 = 2 * self.square_size ** self.coverage_degree - 1 - self.square_size
                square_size_v2 = utils.find_next_prime_power(self.num_parms - 1)
                num_configs_v2 = square_size_v2 ** self.coverage_degree
                if num_configs_v2 < num_configs_v1:
                    self.square_size = square_size_v2
                    self.num_rounds = 1

    def find_capacity(self) -> int:
        capacity = self.round_group_size[0]

        for round_index in range(1, self.num_rounds):
            capacity *= self.round_group_size[round_index]
            if self.round_group_size[round_index] == self.square_size:
                capacity += 1
        return capacity

    def determine_round_groupings(self):
        if self.num_rounds > 0:
            max_parms = self.square_size + 1
            self.num_configs_per_round = []
            self.round_group_size = []
            self.group_repeat_factor = []

            self.extra_parms_repeat_factor = [
                                                 [0] * self.num_rounds] * self.num_rounds

            self.num_configs_per_round.append(
                self.square_size ** self.coverage_degree)
            self.round_group_size.append(max_parms)
            self.group_repeat_factor.append(1)

            for _ in range(1, self.num_rounds):
                self.round_group_size.append(self.square_size)
                self.num_configs_per_round.append(
                    self.square_size ** self.coverage_degree - self.square_size)

            capacity = self.find_capacity()
            current_round = 1
            while capacity < self.num_parms:
                self.round_group_size[current_round] = max_parms
                self.num_configs_per_round[current_round] = self.square_size ** self.coverage_degree - 1
                current_round += 1
                capacity = self.find_capacity()

            num_configs = self.num_configs_per_round[0]
            for round_index in range(1, self.num_rounds):
                self.group_repeat_factor.append(
                    self.round_group_size[round_index - 1] *
                    self.group_repeat_factor[round_index - 1])
                num_configs += self.num_configs_per_round[round_index]

            if self.square_size < self.max_num_values:
                num_configs += (self.max_num_values -
                                self.square_size) * self.second_max_num_values

        basic_capacity = self.group_repeat_factor[self.num_rounds -
                                                  1] * self.round_group_size[self.num_rounds - 1]
        self.extra_parms_per_round.append(0)
        for round_index in range(1, self.num_rounds):
            if self.round_group_size[round_index] == self.square_size + 1:
                self.extra_parms_per_round.append(0)
            else:
                self.extra_parms_per_round.append(
                    basic_capacity // (
                            self.group_repeat_factor[round_index] * self.round_group_size[round_index]))
            if round_index + 1 < self.num_rounds:
                self.extra_parms_repeat_factor[round_index][round_index + 1] = 1
                for sub_seq_index in range(round_index + 2, self.num_rounds):
                    self.extra_parms_repeat_factor[round_index][sub_seq_index] = \
                        self.extra_parms_repeat_factor[round_index][sub_seq_index -
                                                                    1] * self.round_group_size[sub_seq_index]

    def adjust_values(self, grid, new_low_value: int):
        if self.max_num_values == self.second_max_num_values:
            difference = new_low_value - 1
        else:
            difference = 0
            new_low_value = -1

        if difference > 0:
            grid = np.delete(grid, [0, new_low_value - 2], axis=0)

        grid = np.where(grid < new_low_value, 0, grid - difference)

        for col_index in range(self.num_parms):
            max_parm_value = self.num_values_per_parm[col_index]
            grid[:, col_index][grid[:, col_index] > max_parm_value] = 0

        return grid

    def build_configurations(self) -> np.ndarray:
        oa_gen = OrthogonalArrayGenerator(
            num_values=self.square_size,
            degree=self.coverage_degree,
            dtype=self.ndarray_type)
        final_grid = None
        basic_capacity = self.group_repeat_factor[self.num_rounds - 1] \
            * self.round_group_size[self.num_rounds - 1]
        for round_num in range(0, self.num_rounds):
            extra_parameters_grid = None
            repeat_factor = basic_capacity // (self.group_repeat_factor[round_num] *
                                               self.round_group_size[round_num])
            if round_num == 0:
                add_grid = oa_gen.generate_oa()
            elif self.round_group_size[round_num] == self.square_size:
                add_grid = oa_gen.reduced_array(self.group_repeat_factor[round_num])
                extra_parameters_grid = oa_gen.extra_parameter_block(
                    len(final_grid),
                    self.extra_parms_per_round[round_num])
            elif self.round_group_size[round_num] == self.square_size + 1:
                add_grid = oa_gen.basic_array(self.group_repeat_factor[round_num])
            else:
                raise ValueError("Error in internal construction")

            if final_grid is not None:
                if extra_parameters_grid is not None:
                    final_grid = np.hstack([final_grid, extra_parameters_grid])
            else:
                final_grid = extra_parameters_grid

            round_grid = np.tile(add_grid, reps=repeat_factor)

            for prior_round in range(1, round_num):
                num_groups = self.extra_parms_per_round[prior_round] // (
                        self.extra_parms_repeat_factor[prior_round][round_num] * self.round_group_size[prior_round])
                add_grid = oa_gen.reduced_array(self.extra_parms_repeat_factor[prior_round][prior_round])
                round_grid = np.hstack(
                    [round_grid, np.tile(add_grid, reps=num_groups)])

            two_to_n_block = oa_gen.two_to_n_block(self.extra_parms_per_round[round_num])
            if two_to_n_block is not None:
                round_grid = np.hstack([round_grid, two_to_n_block])

            if final_grid is not None:
                final_grid = np.vstack([final_grid, round_grid])
            else:
                final_grid = round_grid

        offset = len(final_grid[0]) - self.num_parms

        over_sized_grid = \
            oa_gen.oversized_parameter(
                self.max_num_values,
                self.max_index + offset,
                len(final_grid[0]),
                self.second_max_num_values)
        if over_sized_grid is not None:
            final_grid = np.vstack([final_grid, over_sized_grid])

        config_grid = self.adjust_values(
            final_grid[:, offset:],
            self.square_size - self.second_max_num_values + 1
        )

        return config_grid
