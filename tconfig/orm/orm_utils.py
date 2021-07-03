from flask_restx import abort
from sqlalchemy.exc import SQLAlchemyError

from tconfig.orm import ORM
from tconfig.orm.value import ValueDao
from tconfig.orm.parameter import ParameterDao
from tconfig.orm.parmset import ParameterSetDao


def orm_session():
    return ORM.session


def orm_commit(items, operation="add"):
    if operation == "add":
        if isinstance(items, list):
            ORM.session.add_all(items)  # @UndefinedVariable
        else:
            ORM.session.add(items)  # @UndefinedVariable
    elif operation == "delete":
        if isinstance(items, list):
            for item in items:
                ORM.session.delete(item)  # @UndefinedVariable
        else:
            ORM.session.delete(items)  # @UndefinedVariable
    ORM.session.commit()  # @UndefinedVariable


def get_or_404_parameter_set(uid=1):
    error_message = f"No parameter set with uid '{uid}' was found"
    return ParameterSetDao.query.get_or_404(
        uid, description=error_message
    )  # @UndefinedVariable


def get_or_404_parameter_with_uid(uid):
    error_message = f"No parameter with uid '{uid}' was found in the parameter set"
    return ParameterDao.query.get_or_404(
        uid, description=error_message
    )  # @UndefinedVariable


def get_or_400_parameter_with_uid(uid):
    error_message = f"No parameter with uid '{uid}' was found in the parameter set"
    try:
        return ParameterDao.query.get(uid)  # @UndefinedVariable
    except SQLAlchemyError:
        abort(400, error_message)


def get_or_404_value_with_uid(uid):
    error_message = f"No value with uid '{uid}' was found in the parameter set"
    return ValueDao.query.get_or_404(
        uid, description=error_message
    )  # @UndefinedVariable


def get_or_404_parameter_value_with_uid(parm, uid_value):
    error_message = (
        f"No value with name '{uid_value}' was found in parameter with uid '{parm.uid}'"
    )
    try:
        uid_int = int(uid_value)
        return ValueDao.query.get_or_404(
            uid_int, description=error_message
        )  # @UndefinedVariable
    except ValueError:
        value_match = [val for val in parm.values if str(val.uid) == str(uid_value)]
        if value_match:
            return value_match
    abort(404, error_message)


def get_value_list():
    return ValueDao.query.all()  # @UndefinedVariable


def get_parameter_list():
    return ParameterDao.query.all()  # @UndefinedVariable


def create_value(name, uid=None):
    return ValueDao(name, uid=uid)


def create_parameter(name, values=None, uid=None):
    return ParameterDao(name, values=values, uid=uid)


def create_parameter_set(parameters=None, uid=None):
    return ParameterSetDao(parameters, uid=uid)
