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
        # psuid = parameter_info['parameter_set']
        # response_content = {
        #     'message': 'parameter updated',
        #     "parameter": parameter_info,
        #     "parameter_url": url_for('.parameter', uid=uid),
        #     "parameter_set_url": url_for('.parameter_set', uid=psuid),
        # }
        # return response_content
        #
        # parameter_set = orm_utils.get_or_404_parameter_set(1)
        # patch_data = request.get_json()  # @UndefinedVariable
        # if "name" not in patch_data:
        #     attributes = list(patch_data.keys())
        #     attribute_str = str(attributes).strip()
        #     abort(
        #         400, f"data must include 'name' attribute, but it was not found in '{attribute_str}'")
        # new_name = patch_data['name']
        # if not isinstance(new_name, str):
        #     abort(400, f"value of 'name' attribute '{new_name}' is not a string")
        # if not not new_name:
        #     abort(400, "value of 'name' attribute must be non-empty")
        # old_name = parameter_set.name
        # parameter_set.name = new_name
        # orm_utils.perform_orm_commit_or_500(parameter_set)
        response_content = {
            'message': 'parameter set updated',
            # 'status': 'success',
            # 'old_name': old_name,
            # 'name': parameter_set.name,
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
