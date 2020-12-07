import numpy as np
from typing import Optional
from . import ParameterSet
from tconfig.core.algorithms.recursive.recursive_gen import RecursiveGenerator
from tconfig.core.algorithms.ipo.ipo_gen import IpoGenerator
from tconfig.core.data import ConfigurationSet

GENERATORS = {
    "ipo": IpoGenerator,
    "recursive": RecursiveGenerator,
}


class GenerationRequest(object):
    def __init__(self, parameter_set: ParameterSet, algorithm_name="recursive",
                 coverage_degree: int = 2,
                 existing_configurations: Optional[ConfigurationSet] = None):
        self.parameter_set = parameter_set
        self.algorithm_name = algorithm_name.lower()
        self.coverage_degree = coverage_degree
        self.existing_configurations = existing_configurations
        if self.coverage_degree < 1:
            raise ValueError(f"Invalid coverage degree '{coverage_degree}'")
        if self.algorithm_name not in GENERATORS:
            raise ValueError(f"Invalid algorithm name '{algorithm_name}'")
        if self.coverage_degree > len(self.parameter_set):
            raise ValueError(
                f"Coverage degree {coverage_degree} higher than number of parameters {len(self.parameter_set)}")
        if self.algorithm_name == "recursive" and self.coverage_degree >= 3:
            raise ValueError(f"Coverage degree higher than 2 not yet implemented for recursive algorithm")

    def construct_generator(self):
        max_num_of_values = max([len(parameter) for parameter in self.parameter_set])
        dtype = np.uint8 if max_num_of_values < 256 else np.uint16
        generator_class = GENERATORS[self.algorithm_name]
        gen_covering_array = None
        if self.existing_configurations:
            gen_covering_array = self.existing_configurations.to_covering_array(self.parameter_set)
        return generator_class(parameter_set=self.parameter_set, coverage_degree=self.coverage_degree,
                               dtype=dtype, existing_configs=gen_covering_array)
