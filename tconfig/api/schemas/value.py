import marshmallow_sqlalchemy as ma_sq
from flask_marshmallow.fields import fields
from marshmallow import validate, validates, Schema, ValidationError, post_load

from tconfig.orm import orm_utils, ValueDao

from .move import MoveSchema


class ValueSchema(ma_sq.schema.SQLAlchemySchema):
    class Meta:
        model = ValueDao
        include_relationships = True
        load_instance = True
        sqla_session = orm_utils.orm_session()

    uid = fields.Integer()
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))
    parameter = fields.Pluck('ParameterSchema', 'uid', allow_none=True)
    position = fields.Integer(allow_none=True)


class UpdateValueSchema(Schema):
    uid = fields.Integer(load_only=True)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))
    parameter = fields.Pluck('UpdateNestedParameterSchema', 'uid', allow_none=True)
    position = fields.Integer(load_only=True)

    @validates('uid')
    def validate_uid(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")

    @validates('position')
    def validate_position(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")


class NewValueSchema(Schema):
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))

    # noinspection PyUnusedLocal
    @post_load()
    def get_name(self, item, many, **kwargs):
        return item['name']


MoveValueSchema = MoveSchema
