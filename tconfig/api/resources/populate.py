from flask_restx import Resource
from flask import url_for

from tconfig.api.service import ORM

from tconfig.api.resources.orm_utils import get_or_404_parameter_set, create_new_value, \
    create_new_parameter, create_new_parameter_set
from tconfig.api.schemas import ParameterSetSchema

PARAMETER_SET_SCHEMA = ParameterSetSchema()


# noinspection PyPep8Naming
class PopulateResource(Resource):
    def get(self):
        ORM.drop_all()
        ORM.create_all()
        RED = create_new_value("Red")
        GREEN = create_new_value("Green")

        BIRD = create_new_value("Bird")
        CAT = create_new_value("Cat")
        DOG = create_new_value("Dog")
        FISH = create_new_value("Fish")

        FAST = create_new_value("Fast")
        SLOW = create_new_value("Slow")

        EIGHTIES = create_new_value("80s")
        TWENTIES = create_new_value("20s")

        p1 = create_new_parameter("Colour", [RED, GREEN])
        p2 = create_new_parameter("Pet", [BIRD, CAT, DOG, FISH])
        p3 = create_new_parameter("Speed", [FAST, SLOW])
        p4 = create_new_parameter("Music", [EIGHTIES, TWENTIES])

        create_new_parameter_set(parameters=[p1, p2, p3, p4])

        parameter_set = get_or_404_parameter_set()
        response_content = {
            "parameter_set": PARAMETER_SET_SCHEMA.dump(parameter_set),
            "parameter_set_url": url_for('.parameter_set'),
        }
        return response_content
