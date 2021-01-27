from flask import request, url_for
from flask_restx import Resource, abort

from tconfig.orm import orm_utils

from tconfig.api.schemas import ValueSchema, UpdateValueSchema

from tconfig.api.resources import resource_utils

VALUE_SCHEMA = ValueSchema()
UPDATE_VALUE_SCHEMA = UpdateValueSchema()


# noinspection PyMethodMayBeStatic
class ValueListResource(Resource):
    def get(self):
        value_list = orm_utils.get_value_list()
        response_content = {
            "value_list": [VALUE_SCHEMA.dump(value) for value in value_list],
            "value_List_url": url_for('.value_list'),
        }
        return response_content

    def post(self):
        post_data = request.get_json()  # @UndefinedVariable
        validation_errors = UPDATE_VALUE_SCHEMA.validate(post_data)
        if validation_errors:
            abort(400, f"Validation error(s):  {validation_errors}")
        value_info = {
            key: UPDATE_VALUE_SCHEMA.fields[key].deserialize(post_data[key])
            for key in post_data
        }
        new_value = orm_utils.create_value(**value_info)
        resource_utils.perform_orm_commit_or_500(new_value)
        new_id = new_value.uid
        response_content = {
            'message': 'new value created',
            'new_value': VALUE_SCHEMA.dump(new_value),
            'new_value_url': url_for('.value', uid=new_id),
            "value_List_url": url_for('.value_list'),
        }
        return response_content, 201
