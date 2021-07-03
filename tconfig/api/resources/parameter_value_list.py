from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.orm import orm_utils

from tconfig.api.schemas import (
    ParameterSchema,
    ValueSchema,
    UpdateValueSchema,
    MoveValueSchema,
)
from tconfig.api.resources import resource_utils

PARAMETER_SCHEMA = ParameterSchema()
VALUE_SCHEMA = ValueSchema()
UPDATE_VALUE_SCHEMA = UpdateValueSchema()
MOVE_VALUE_SCHEMA = MoveValueSchema()


# noinspection PyMethodMayBeStatic
class ParameterValueListResource(Resource):
    def get(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        response_content = {
            "message": f"value list for parameter {uid}",
            "values": PARAMETER_SCHEMA.dump(parameter)["values"],
            "parameter_url": url_for(".parameter", uid=uid),
            "parameter_value_list_url": url_for(".parameter_value_list", uid=uid),
        }
        return response_content

    def post(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        post_data = request.get_json()  # @UndefinedVariable
        validation_errors = UPDATE_VALUE_SCHEMA.validate(post_data)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        value_info = {
            key: UPDATE_VALUE_SCHEMA.fields[key].deserialize(post_data[key])
            for key in post_data
        }
        new_value = orm_utils.create_value(**value_info)
        parameter.append(new_value)
        resource_utils.perform_orm_commit_or_500(parameter, operation="update")
        new_id = new_value.uid
        response_content = {
            "message": "new value created",
            "new_value": VALUE_SCHEMA.dump(new_value),
            "new_value_url": url_for(".value", uid=new_id),
            "parameter_url": url_for(".parameter", uid=uid),
            "parameter_value_list_url": url_for(".parameter_value_list", uid=uid),
        }
        return response_content, 201

    def put(self, uid):
        parameter = orm_utils.get_or_404_parameter_with_uid(uid)
        put_data = request.get_json()  # @UndefinedVariable
        put_data.update({"numItems": len(parameter)})
        validation_errors = MOVE_VALUE_SCHEMA.validate(put_data)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        old_index = put_data["oldIndex"]
        new_index = put_data["newIndex"]
        moved_value = parameter.pop(old_index)
        parameter.insert(new_index, moved_value)
        resource_utils.perform_orm_commit_or_500(parameter, operation="update")
        response_content = {
            "message": "value moved within list",
            "old_index": old_index,
            "new_index": new_index,
            "moved_value_uri": url_for(".value", uid=moved_value.uid),
        }
        return response_content
