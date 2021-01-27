from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.orm import orm_utils

from tconfig.api.schemas import ParameterSchema, UpdateParameterSchema

from tconfig.api.resources import resource_utils

PARAMETER_SCHEMA = ParameterSchema()
UPDATE_PARAMETER_SCHEMA = UpdateParameterSchema()


# noinspection PyMethodMayBeStatic
class ParameterResource(Resource):
    def get(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        response_content = {
            "parameter": PARAMETER_SCHEMA.dump(parameter),
            "parameter_url": url_for('.parameter', uid=uid),
            "parameter_set_url": url_for('.parameter_set'),
        }
        return response_content

    def patch(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        edit_parameter_info = UPDATE_PARAMETER_SCHEMA.dump(parameter)
        patch_data = request.get_json()  # @UndefinedVariable
        if not patch_data:
            abort(400, "No updates provided with request")
        edit_parameter_info.update(patch_data)
        validation_errors = UPDATE_PARAMETER_SCHEMA.validate(edit_parameter_info)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        for key in patch_data:
            new_value = PARAMETER_SCHEMA.fields[key].deserialize(edit_parameter_info[key])
            setattr(parameter, key, new_value)
        resource_utils.perform_orm_commit_or_500(parameter, operation="update")
        parameter_info = PARAMETER_SCHEMA.dump(parameter)
        response_content = {
            'message': 'parameter updated',
            "parameter": parameter_info,
            "parameter_url": url_for('.parameter', uid=uid),
            "parameter_set_url": url_for('.parameter_set'),
        }
        return response_content

    def delete(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        deleted_name = parameter.name
        resource_utils.perform_orm_commit_or_500(parameter, "delete")
        response_content = {
            'message': f'parameter {uid} deleted',
            'deleted_parameter_name': deleted_name,
            "parameter_set_url": url_for('.parameter_set'),
        }
        return response_content
