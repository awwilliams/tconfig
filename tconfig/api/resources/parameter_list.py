from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.orm import orm_utils

from tconfig.api.schemas import ParameterSchema, NewParameterSchema, MoveParameterSchema

from tconfig.api.resources import resource_utils

PARAMETER_SCHEMA = ParameterSchema()
NEW_PARAMETER_SCHEMA = NewParameterSchema()
MOVE_PARAMETER_SCHEMA = MoveParameterSchema()


# noinspection PyMethodMayBeStatic
class ParameterListResource(Resource):
    def get(self):
        parameter_list = orm_utils.get_parameter_list()
        response_content = {
            "parameter_list": [
                PARAMETER_SCHEMA.dump(parameter) for parameter in parameter_list
            ],
            "parameter_List_url": url_for(".parameter_list"),
        }
        return response_content

    def put(self):
        parameter_set = orm_utils.get_or_404_parameter_set()
        put_data = request.get_json()  # @UndefinedVariable
        put_data.update({"numItems": len(parameter_set)})
        validation_errors = MOVE_PARAMETER_SCHEMA.validate(put_data)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        old_index = put_data["oldIndex"]
        new_index = put_data["newIndex"]
        moved_parameter = parameter_set.pop(old_index)
        parameter_set.insert(new_index, moved_parameter)
        resource_utils.perform_orm_commit_or_500(parameter_set, operation="update")
        response_content = {
            "message": "parameter moved within list",
            "old_index": old_index,
            "new_index": new_index,
            "moved_parameter_url": url_for(".parameter", uid=moved_parameter.uid),
            "parameter_List_url": url_for(".parameter_list"),
        }
        return response_content

    def post(self):
        parameter_set = orm_utils.get_or_404_parameter_set()
        post_data = request.get_json()  # @UndefinedVariable
        validation_errors = NEW_PARAMETER_SCHEMA.validate(post_data)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        value_info = {
            key: NEW_PARAMETER_SCHEMA.fields[key].deserialize(post_data[key])
            for key in post_data
        }
        new_parameter = orm_utils.create_parameter(**value_info)
        parameter_set.append(new_parameter)
        resource_utils.perform_orm_commit_or_500(parameter_set)
        new_id = new_parameter.uid
        response_content = {
            "message": "new parameter created",
            "new_parameter": PARAMETER_SCHEMA.dump(new_parameter),
            "new_parameter_url": url_for(".parameter", uid=new_id),
            "parameter_list_url": url_for(".parameter_list"),
            "parameter_set_url": url_for(".parameter_set"),
        }
        return response_content, 201
