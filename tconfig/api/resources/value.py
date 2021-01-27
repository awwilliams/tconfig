from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.orm import orm_utils

from tconfig.api.schemas import ValueSchema, UpdateValueSchema

from tconfig.api.resources import resource_utils

VALUE_SCHEMA = ValueSchema()
UPDATE_VALUE_SCHEMA = UpdateValueSchema()


# noinspection PyMethodMayBeStatic
class ValueResource(Resource):
    def get(self, uid):
        value = orm_utils.get_or_404_value_with_uid(uid)
        value_info = VALUE_SCHEMA.dump(value)
        puid = value_info['parameter']
        response_content = {
            'message': 'value found',
            "value": value_info,
            "value_url": url_for('.value', uid=uid),
            "parameter_url": url_for('.parameter', uid=puid),
        }
        return response_content

    def patch(self, uid):
        value = orm_utils.get_or_404_value_with_uid(uid)
        edit_value_info = UPDATE_VALUE_SCHEMA.dump(value)
        patch_data = request.get_json()  # @UndefinedVariable
        if not patch_data:
            abort(400, "No updates provided with request")
        edit_value_info.update(patch_data)
        validation_errors = UPDATE_VALUE_SCHEMA.validate(edit_value_info)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        for key in patch_data:
            new_value = VALUE_SCHEMA.fields[key].deserialize(edit_value_info[key])
            setattr(value, key, new_value)
        resource_utils.perform_orm_commit_or_500(value, operation="update")
        value_info = VALUE_SCHEMA.dump(value)
        puid = value_info['parameter']
        response_content = {
            'message': 'value updated',
            "value": value_info,
            "value_url": url_for('.value', uid=uid),
            "parameter_url": url_for('.parameter', uid=puid),
        }
        return response_content

    def delete(self, uid):
        value = orm_utils.get_or_404_value_with_uid(uid)
        deleted_value = VALUE_SCHEMA.dump(value)
        puid = value.parameter.uid
        resource_utils.perform_orm_commit_or_500(value, "delete")
        response_content = {
            'message': f'value {uid} deleted',
            'deleted_value': deleted_value,
            "parameter_url": url_for('.parameter', uid=puid),
        }
        return response_content
