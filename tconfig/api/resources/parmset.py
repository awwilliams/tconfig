from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.api.resources import orm_utils

from tconfig.api.schemas import ParameterSetSchema, UpdateParameterSetSchema

PARAMETER_SET_SCHEMA = ParameterSetSchema()
UPDATE_PARAMETER_SET_SCHEMA = UpdateParameterSetSchema()


class ParameterSetResource(Resource):
    def get(self):
        parameter_set = orm_utils.get_or_404_parameter_set()
        response_content = {
            "parameter_set": PARAMETER_SET_SCHEMA.dump(parameter_set),
            "parameter_set_url": url_for('.parameter_set'),
            "parameter_list_url": url_for('.parameter_list'),
        }
        return response_content, 200, {"Access-Control-Allow-Origin": "*"}

    def patch(self):
        parameter_set = orm_utils.get_or_404_parameter_set(1)
        edit_parameter_set_info = UPDATE_PARAMETER_SET_SCHEMA.dump(parameter_set)
        patch_data = request.get_json()  # @UndefinedVariable
        if not patch_data:
            abort(400, "No updates provided with request")
        edit_parameter_set_info.update(patch_data)
        validation_errors = UPDATE_PARAMETER_SET_SCHEMA.validate(edit_parameter_set_info)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        for key in patch_data:
            new_value = PARAMETER_SET_SCHEMA.fields[key].deserialize(edit_parameter_set_info[key])
            setattr(parameter_set, key, new_value)
        orm_utils.perform_orm_commit_or_500(parameter_set, operation="update")
        parameter_set_info = PARAMETER_SET_SCHEMA.dump(parameter_set)
        response_content = {
            'message': 'parameter set updated',
            "parameter_set": parameter_set_info,
            "parameter_set_url": url_for('.parameter_set'),
            "parameter_list_url": url_for('.parameter_list'),
        }
        return response_content

    def delete(self):
        parameter = orm_utils.get_or_404_parameter_with_uid(1)
        orm_utils.perform_orm_commit_or_500(parameter, "delete")
        response_content = {
            'message': 'parameter set deleted',
        }
        return response_content
