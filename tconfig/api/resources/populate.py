from flask_restx import Resource
from flask import url_for

from tconfig.orm import orm_utils, ORM

from tconfig.api.schemas import ParameterSetSchema

PARAMETER_SET_SCHEMA = ParameterSetSchema()


# noinspection PyPep8Naming
class PopulateResource(Resource):
    def get(self):
        ORM.drop_all()
        ORM.create_all()
        RED = orm_utils.create_value("Red")
        GREEN = orm_utils.create_value("Green")

        BIRD = orm_utils.create_value("Bird")
        CAT = orm_utils.create_value("Cat")
        DOG = orm_utils.create_value("Dog")
        FISH = orm_utils.create_value("Fish")

        FAST = orm_utils.create_value("Fast")
        SLOW = orm_utils.create_value("Slow")

        EIGHTIES = orm_utils.create_value("80s")
        TWENTIES = orm_utils.create_value("20s")

        orm_utils.orm_commit(
            [RED, GREEN, BIRD, CAT, DOG, FISH, FAST, SLOW, EIGHTIES, TWENTIES], "add")

        p1 = orm_utils.create_parameter("Colour", [RED, GREEN])
        p2 = orm_utils.create_parameter("Pet", [BIRD, CAT, DOG, FISH])
        p3 = orm_utils.create_parameter("Speed", [FAST, SLOW])
        p4 = orm_utils.create_parameter("Music", [EIGHTIES, TWENTIES])

        orm_utils.orm_commit([p1, p2, p3, p4], "add")

        parm_set = orm_utils.create_parameter_set(parameters=[p1, p2, p3, p4])
        orm_utils.orm_commit(parm_set, "add")

        parameter_set = orm_utils.get_or_404_parameter_set()
        response_content = {
            "parameter_set": PARAMETER_SET_SCHEMA.dump(parameter_set),
            "parameter_set_url": url_for('.parameter_set'),
        }
        return response_content
