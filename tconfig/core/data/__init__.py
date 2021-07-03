"""
Package containing core data classes to set up a collection of parameters
and values for generating test configurations, a generation request class,
and a collection of test configurations.
"""

import numpy as np

DEFAULT_NDARRAY_TYPE = np.uint8

# noinspection PyPep8
from .value import Value

# noinspection PyPep8
from .parameter import Parameter

# noinspection PyPep8
from .parmset import ParameterSet

# noinspection PyPep8
from .configset import ConfigurationSet

# noinspection PyPep8
from .genrequest import GenerationRequest


__all__ = [
    "Value",
    "Parameter",
    "ParameterSet",
    "ConfigurationSet",
    "GenerationRequest",
    "DEFAULT_NDARRAY_TYPE",
]
