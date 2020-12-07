from flask_marshmallow.fields import fields
from marshmallow import validate, Schema, ValidationError, validates_schema


class MoveSchema(Schema):
    numItems = fields.Integer(required=True)
    oldIndex = fields.Integer(required=True, validate=validate.Range(min=0))
    newIndex = fields.Integer(required=True, validate=validate.Range(min=0))

    # noinspection PyUnusedLocal
    @validates_schema()
    def validate_indices_with_items(self, data, **kwargs):
        number_of_values = data.pop('numItems')
        errors = {}
        limit_message = f"Must be less than or equal to {number_of_values}."
        for index_name, index_value in data.items():
            if index_value >= number_of_values:
                errors[index_name] = [limit_message, ]
        if errors:
            raise ValidationError(errors)
