from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.api.schemas.parameter import ParameterSchema, ParameterExclusionSchema, UpdateParameterSchema
from tconfig.api.resources import orm_utils

PARAMETER_EXCLUSION_SCHEMA = ParameterExclusionSchema()
PARAMETER_SCHEMA = ParameterSchema()
UPDATE_PARAMETER_SCHEMA = UpdateParameterSchema()


class ParameterExclusionListResource(Resource):
    def get(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        excluded_content = PARAMETER_EXCLUSION_SCHEMA.dump(parameter)
        response_content = {
            'message': f'exclusions for parameter {uid}',
            'parameter': excluded_content,
            'parameter_url': url_for('.parameter', uid=uid),
            'parameter_exclusion_url': url_for('.parameter_exclude_list', uid=uid),
        }
        return response_content

    def post(self, uid):
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
        orm_utils.perform_orm_commit_or_500(parameter, operation="update")
        parameter_info = PARAMETER_EXCLUSION_SCHEMA.dump(parameter)
        response_content = {
            'message': 'parameter exclusion created',
            "parameter": parameter_info,
            "parameter_url": url_for('.parameter', uid=uid),
        }
        return response_content, 201
