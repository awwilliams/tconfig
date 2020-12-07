"""
Created on Sep 10, 2017

@author: Alan Williams
"""

from typing import Optional
import pandas as pd
import numpy as np

from . import ParameterSet, DEFAULT_NDARRAY_TYPE


class ConfigurationSet(object):

    def __init__(self, *,
                 parameter_set: Optional[ParameterSet] = None,
                 covering_array: Optional[np.ndarray] = None,
                 data_frame: Optional[pd.DataFrame] = None):
        """
        Convert a parameter set (list of Pandas Series) and a integer-based covering
        array (NumPy array) to a Pandas DataFrame where the column indices are the
        names of the parameters, the row indices are the configuration number, the
        entries are the parameter value names, and "don't care" values are set to
        the Pandas "null" value Pandas.NA.
        """
        use_covering_array = (parameter_set and isinstance(covering_array, np.ndarray)) and data_frame is None
        if use_covering_array:
            self.configs = self.covering_array_to_dataframe(parameter_set, covering_array)
        else:
            self.configs = data_frame

    def __repr__(self) -> str:
        return f"ConfigurationSet(configs={self.configs})"

    def __str__(self) -> str:
        return str(self.configs)

    def __eq__(self, other: 'ConfigurationSet') -> bool:
        return self.configs.equals(other.configs)

    def __hash__(self) -> int:
        return hash(self.configs)

    def __iter__(self):
        return iter([pd.Series(z, index=self.configs.columns)
                     for z in self.configs.itertuples(index=False)])

    def __len__(self) -> int:
        return len(self.configs)

    def __getitem__(self, key: int):
        return self.configs.iloc[key]

    def to_dict(self):
        return {
            "configurations": [
                {key: value.name for key, value in self[index].items()}
                for index in range(len(self))
            ]
        }

    @staticmethod
    def covering_array_to_dataframe(parameter_set, covering_array):
        dataframe = pd.DataFrame(
            covering_array, columns=[parm.name for parm in parameter_set])

        # Replace the covering array integer entries for each column with the corresponding
        # values for that column's parameter.

        for parm in parameter_set:
            # Don't care values in covering array have a zero entry instead of NumPy's NaN,
            # as NaN requires using floats as the array's data type.

            replace_dict = {0: pd.NA}

            # Parameter values are indexed from zero, so be sure to match covering array
            # value N+1 with parameter value N.

            replace_dict.update({k + 1: v for k, v in enumerate(parm.values)})

            # Replace covering array entries in DataFrame using 'replace_dict' as
            # the mapping of integers to parameter values.

            dataframe[parm.name].replace(to_replace=replace_dict, inplace=True)
        return dataframe

    @staticmethod
    def dataframe_to_covering_array(dataframe, parameter_set):
        if dataframe is None or dataframe.empty:
            return np.zeros(shape=(0, len(parameter_set)))
        configs = []
        df_dict = dataframe.to_dict(orient="index")
        for index in df_dict:
            config_row = []
            for value in df_dict[index].values():
                if value is pd.NA:
                    value_index = -1
                elif hasattr(value, 'position'):
                    value_index = value.position
                else:
                    parameter, value_index = parameter_set.find_parameter_index_for_value(value)

                # At this point, value_index is -1 if the parameter is "don't care" or
                # the value doesn't match a parameter.  Covering arrays use 0 as "don't care"
                # and values indexed from 1.

                config_row.append(value_index + 1)
            configs.append(config_row)
        return np.array(configs, dtype=DEFAULT_NDARRAY_TYPE)

    def to_covering_array(self, parameter_set):
        return self.dataframe_to_covering_array(self.configs, parameter_set)
