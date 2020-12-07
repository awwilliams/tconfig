"""
Created on Oct 4, 2017

@author: Alan Williams
"""

from copy import deepcopy
from typing import Optional, Set
import numpy as np
from tconfig.core.data import ParameterSet, DEFAULT_NDARRAY_TYPE
from tconfig.core.algorithms.generator import Generator
from tconfig.core.algorithms.ipo.ie import InteractionElement


# pylint: disable=invalid-name


class IpoGenerator(Generator):

    def __init__(self, parameter_set: ParameterSet, coverage_degree: int = 2, *,
                 dtype=DEFAULT_NDARRAY_TYPE, existing_configs: Optional[np.ndarray] = None):
        super().__init__(parameter_set, coverage_degree,
                         dtype=dtype, existing_configs=existing_configs)
        self.test_set = None if existing_configs is None else deepcopy(
            existing_configs)

    def add_new_test(self, t_prime: np.ndarray,
                     pkw: InteractionElement,
                     piu: InteractionElement) -> np.ndarray:
        """
        Create a new test
        """
        config_width = (1 + max(max(pkw.keys()), max(piu.keys())))
        new_config = np.zeros((1, config_width), dtype=self.ndarray_type)
        for index in pkw:
            new_config[0, index] = pkw[index]
        for index in piu:
            new_config[0, index] = piu[index]
        if t_prime is None:
            return new_config
        return np.vstack([t_prime, new_config])

    @staticmethod
    def is_zero(test, pkw: InteractionElement) -> bool:
        """
        Returns True if all values in 'test' are either 0 or the same as the
        test index, and False otherwise.
        """
        return all(test[index] in [0, value] for index, value in pkw.items())

    def contains_dash_in_t(self, t_prime: Optional[np.ndarray],
                           pkw: InteractionElement,
                           piu: InteractionElement) -> int:
        """
        Looks for 0 values in a test set that can be filled in.
        """

        pi = list(piu)[0]
        u = piu[pi]

        for test_num, test in enumerate(self.test_set):
            if self.is_zero(test, pkw) and test[pi] in [0, u]:
                return test_num

        if t_prime is not None:
            for test_num, test in enumerate(t_prime):
                if self.is_zero(test, pkw) and test[pi] == u:
                    return test_num + len(self.test_set)

        return -1

    def first_parameters(self):
        strength = self.coverage_degree
        value = [1] * strength
        initial_num_rows = 1
        for index in range(0, strength):
            initial_num_rows *= self.num_values_per_parm[index]

        initial_num_columns = strength
        self.test_set = np.empty(
            (initial_num_rows,
             initial_num_columns),
            dtype=self.ndarray_type)

        for test_num in range(0, initial_num_rows):
            for col in range(0, strength):
                self.test_set[test_num][col] = value[col]
            if test_num < initial_num_rows - 1:
                incr_col = strength - 1
                value[incr_col] += 1
                while value[incr_col] > self.num_values_per_parm[incr_col]:
                    value[incr_col] = 1
                    incr_col -= 1
                    value[incr_col] += 1

    def get_hori_recur(self,
                       new_parameter_index: int,
                       cover: int, pi: Set[InteractionElement],
                       test_value_list: InteractionElement) -> Set[InteractionElement]:
        for i in range(0, new_parameter_index):
            if i in test_value_list:
                continue
            for value in range(1, 1 + self.num_values_per_parm[i]):
                ie = InteractionElement(test_value_list)
                ie[i] = value
                if cover == 1 and ie not in pi:
                    pi.add(ie)
                if cover != 1:
                    self.get_hori_recur(new_parameter_index, cover - 1, pi, ie)
        return pi

    def get_test_value_recur(self, orig_set: Set[InteractionElement],
                             config_num: int,
                             parm_num: int,
                             cover: int, result,
                             ie: InteractionElement):

        for i in range(0, parm_num):
            same_flag = i in ie.keys()
            if same_flag:
                continue
            new_ie = InteractionElement(ie)
            new_ie[i] = self.test_set[config_num][i]

            if cover == 1:
                if new_ie in orig_set and new_ie not in result:
                    result.add(new_ie)
            else:
                self.get_test_value_recur(orig_set, config_num, parm_num, cover - 1,
                                          result, new_ie)

    def pairs_covered_in(self, orig_set: Set[InteractionElement],
                         config_num: int,
                         parm_num: int,
                         new_value: int) -> Set[InteractionElement]:
        result: Set[InteractionElement] = set()
        for parm_index in range(0, parm_num):
            ie = InteractionElement(
                {parm_num: new_value, parm_index: self.test_set[config_num][parm_index]})
            if self.coverage_degree > 2:
                self.get_test_value_recur(
                    orig_set, config_num, parm_num, self.coverage_degree - 2, result, ie)
            else:
                if ie in orig_set:
                    result.add(ie)
        return result

    def do_horizontal_growth(
            self, new_parameter_index: int) -> Set[InteractionElement]:
        """
        Add one more parameter, and determine which values to fill in
        to the existing configuration set that cover the most interaction
        elements for the new parameter.
        """
        self.test_set = np.insert(
            self.test_set, self.test_set.shape[1], 0, axis=1)

        pi = set()
        num_new_values = self.num_values_per_parm[new_parameter_index]
        for nv_index in range(1, num_new_values + 1):
            for parm_index in range(0, new_parameter_index):
                for value_index in range(
                        1, self.num_values_per_parm[parm_index] + 1):
                    ie = InteractionElement(
                        {new_parameter_index: nv_index, parm_index: value_index})
                    if self.coverage_degree > 2:
                        pi = self.get_hori_recur(
                            new_parameter_index, self.coverage_degree - 2, pi, ie)
                    else:
                        pi.add(ie)

        s = min(num_new_values, len(self.test_set))

        for j in range(0, s):
            self.test_set[j][new_parameter_index] = j + 1
            covered = self.pairs_covered_in(pi, j, new_parameter_index, j + 1)
            pi = pi - covered

        if s == len(self.test_set):
            return pi

        for j in range(s, len(self.test_set)):
            pi_prime = set()
            v_prime = 0
            for nv_index in range(1, num_new_values + 1):
                pi_double_prime = self.pairs_covered_in(
                    pi, j, new_parameter_index, nv_index)
                if len(pi_double_prime) > len(pi_prime):
                    pi_prime = pi_double_prime
                    v_prime = nv_index
            if v_prime != 0:
                self.test_set[j][new_parameter_index] = v_prime
            pi = pi - pi_prime

        return pi

    def do_vertical_growth(self,
                           pi: Set[InteractionElement],
                           new_parameter_index: int) -> np.ndarray:
        """
        Determine a set of additional test configurations that are needed
        to completely cover the set of interaction elements required for
        the new parameter.
        """
        t_prime: Optional[np.ndarray] = None

        for ie in pi:
            piu = InteractionElement(
                {new_parameter_index: ie[new_parameter_index]})
            pkw = InteractionElement(ie.data)
            del pkw[new_parameter_index]

            tau = self.contains_dash_in_t(t_prime, pkw, piu)
            if tau >= 0:
                if tau >= len(self.test_set):
                    for i in pkw:
                        t_prime[tau - len(self.test_set)][i] = pkw[i]  # pylint: disable=unsubscriptable-object
                else:
                    for i in pkw:
                        self.test_set[tau][i] = pkw[i]
                    if self.test_set[tau][new_parameter_index] == 0:
                        self.test_set[tau][new_parameter_index] = piu[new_parameter_index]
            else:
                t_prime = self.add_new_test(t_prime, pkw, piu)
        return t_prime

    def generate_covering_array(self) -> np.ndarray:
        """
        Generate a set of configurations for the ParameterSet and coverage degree.
        """

        if self.test_set is None or len(
                self.test_set[0]) < self.coverage_degree:
            self.first_parameters()

        if self.num_parms > self.coverage_degree:
            for parm_index in range(self.coverage_degree, self.num_parms):
                missing_interactions = self.do_horizontal_growth(parm_index)
                new_rows = self.do_vertical_growth(
                    missing_interactions, parm_index)
                if new_rows is not None:
                    self.test_set = new_rows if self.test_set is None else np.vstack(
                        [self.test_set, new_rows])
        return self.test_set
