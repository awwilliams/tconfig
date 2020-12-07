from typing import Optional
import numpy as np
from tconfig.core.data import ParameterSet, DEFAULT_NDARRAY_TYPE


class Generator:

    def __init__(self, parameter_set: ParameterSet, coverage_degree: int = 2, *,
                 dtype=DEFAULT_NDARRAY_TYPE, existing_configs: Optional[np.ndarray] = None):
        """
        Initialize covering array generator.

        Information used from the parameter set is the number of parameters, and the
        number of values for each parameter.

        Some generator implementation algorithms may not be able to handle coverage_degree > 2.

        Some generator implementation algorithms may not be able to upgrade an initial set of
        configurations to a coverage degree goal.
        """
        self.num_parms = len(parameter_set)
        self.num_values_per_parm = [len(parm) for parm in parameter_set]
        self.coverage_degree = coverage_degree
        self.ndarray_type = dtype
        self.existing_configs = existing_configs

    def generate_covering_array(self) -> np.ndarray:
        """
        Generate a set of configurations for the ParameterSet and coverage degree.
        """
        raise NotImplementedError(
            "Generator.generate_covering_array() must be implemented by subclasses")
