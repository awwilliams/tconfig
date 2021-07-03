from typing import Optional

import numpy as np

from tconfig.core.algorithms.recursive import RecursiveGenerator
from tconfig.core.algorithms.ipo import IpoGenerator
from tconfig.core.data import ConfigurationSet

from . import ParameterSet

GENERATORS = {
    "ipo": IpoGenerator,
    "recursive": RecursiveGenerator,
}

# pylint: disable=unsubscriptable-object


class GenerationRequest(object):
    """
    Instance of a request to generate a covering array for a parameter set.  Intended
    for use from REST API.
    """

    def __init__(
        self,
        parameter_set: ParameterSet,
        algorithm_name: str = "recursive",
        coverage_degree: int = 2,
        existing_configurations: Optional[ConfigurationSet] = None,
    ):
        """
        Initalize a generation request.

        :param parameter_set: Collection of parameters and values for which test
            configurations are to be generated.
        :type parameter_set: ~tconfig.core.data.parmset.ParameterSet

        :param algorithm_name:  Covering array generation algorithm to be used.
            Must be one of "recursive" or "ipo" to select the "recursive block"
            method or the "in-parameter order" (IPO) method.
        :type algorithm_name: str

        :param coverage_degree:  Degree of interaction coverage for the covering
            array.  Must be 2 for the recursive block method, and can be 2 or
            larger for the IPO method.

        :param existing_configurations: (optional) If provided, the IPO method
            can be set to start with a set of already existing configurations
            which can be extended to a covering array.
        :type existing_configurations: Optional[~tconfig.core.data.configset.ConfigurationSet]

        """
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
                f"Coverage degree {coverage_degree} higher than number of parameters {len(self.parameter_set)}"
            )
        if self.algorithm_name == "recursive" and self.coverage_degree >= 3:
            raise ValueError(
                "Coverage degree higher than 2 not yet implemented for recursive algorithm"
            )

    def construct_generator(self):
        """
        Create a covering array generator that can handle the generation request.

        :return An instance of a covering array generator appropriate for the
            selected generation algorithm.
        :rtype: ~tconfig.core.algorithms.Generator
        """
        max_num_of_values = max([len(parameter) for parameter in self.parameter_set])
        dtype = np.uint8 if max_num_of_values < 256 else np.uint16
        generator_class = GENERATORS[self.algorithm_name]
        gen_covering_array = None
        if self.existing_configurations:
            gen_covering_array = self.existing_configurations.to_covering_array(
                self.parameter_set
            )
        return generator_class(
            parameter_set=self.parameter_set,
            coverage_degree=self.coverage_degree,
            dtype=dtype,
            existing_configs=gen_covering_array,
        )
