"""
Created on Oct. 3, 2020

@author: Alan Williams
"""
from tconfig.orm.value import ValueDao
from tconfig.orm.parameter import ParameterDao
from tconfig.orm.parmset import ParameterSetDao


def create_test_value(*args, **kwargs):
    return ValueDao.create_new(*args, **kwargs)  # @UndefinedVariable


def create_test_parameter(*args, **kwargs):
    return ParameterDao.create_new(*args, **kwargs)  # @UndefinedVariable


def create_test_parameter_set(*args, **kwargs):
    return ParameterSetDao.create_new(*args, **kwargs)  # @UndefinedVariable
