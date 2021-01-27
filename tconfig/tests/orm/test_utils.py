from tconfig.orm import orm_utils


def create_test_value(*args, **kwargs):
    new_value = orm_utils.create_value(*args, **kwargs)
    orm_utils.orm_commit(new_value, "add")
    return new_value


def create_test_parameter(*args, **kwargs):
    new_value = orm_utils.create_parameter(*args, **kwargs)
    orm_utils.orm_commit(new_value, "add")
    return new_value


def create_test_parameter_set(*args, **kwargs):
    new_value = orm_utils.create_parameter_set(*args, **kwargs)
    orm_utils.orm_commit(new_value, "add")
    return new_value
