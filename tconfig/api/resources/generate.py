from flask import request, url_for
from flask_restx import Resource

from tconfig.api.schemas import ConfigSetSchema, GeneratorRequestSchema
from tconfig.core.data import ConfigurationSet

GENERATE_REQUEST_SCHEMA = GeneratorRequestSchema()
CONFIGURATIONS_SCHEMA = ConfigSetSchema()


# noinspection PyMethodMayBeStatic
class GenerateResource(Resource):
    def post(self):
        post_data = request.get_json()  # @UndefinedVariable
        gen_req = GENERATE_REQUEST_SCHEMA.load(post_data)
        generator = gen_req.construct_generator()
        covering_array = generator.generate_covering_array()
        configurations = ConfigurationSet(
            parameter_set=gen_req.parameter_set, covering_array=covering_array
        )
        response_content = {
            "message": "test configurations generated",
            "configuration_set": CONFIGURATIONS_SCHEMA.dump(configurations),
            "parameter_set_url": url_for(".parameter_set"),
        }
        return response_content
