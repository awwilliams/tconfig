from flask_restx import Resource, abort
from flask import url_for

from tconfig.api.schemas.parameter import ParameterExclusionSchema
from tconfig.api.resources import orm_utils

PARAMETER_EXCLUSION_SCHEMA = ParameterExclusionSchema()


class ParameterExclusionResource(Resource):
    def delete(self, puid, euid):
        parameter = orm_utils.get_or_404_parameter_with_uid(puid)
        excluded_parameter = orm_utils.get_or_404_parameter_with_uid(euid)
        if excluded_parameter not in parameter.excluded:
            abort(400, f"Parameter with uid={euid} is not in the exclusion list of parameter with uid={puid}")
        parameter.restore_interaction_with(excluded_parameter)
        orm_utils.perform_orm_commit_or_500([parameter, excluded_parameter])
        excluded_content = PARAMETER_EXCLUSION_SCHEMA.dump(parameter)
        excluded_by_content = PARAMETER_EXCLUSION_SCHEMA.dump(excluded_parameter)
        response_content = {
            'message': 'parameter exclusion deleted',
            'parameter_excludes': excluded_content,
            'parameter_excluded_by': excluded_by_content,
            'parameter_url': url_for('.parameter', uid=puid),
            'excluded_parameter_url': url_for('.parameter', uid=euid),
        }
        return response_content, 200
