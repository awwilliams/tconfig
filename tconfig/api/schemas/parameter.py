import marshmallow_sqlalchemy as ma_sq
from flask_marshmallow.fields import fields
from marshmallow import Schema, ValidationError, validates, validate, post_load

from tconfig.orm import orm_utils, ParameterDao

from tconfig.api.schemas import ValueSchema
from .move import MoveSchema


class ParameterSchema(ma_sq.SQLAlchemySchema):
    class Meta:
        model = ParameterDao
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = orm_utils.orm_session()

    uid = fields.Integer()
    name = fields.String(
        required=True, allow_none=False, validate=validate.Length(min=1)
    )
    values = fields.Nested(ValueSchema, many=True)
    parameter_set = fields.Pluck("ParameterSetSchema", "uid", allow_none=True)
    position = fields.Integer(allow_none=True)
    excluded = fields.Pluck("ParameterSchema", "uid", many=True)
    excluded_by = fields.Pluck("ParameterSchema", "uid", many=True)


class UpdateNestedParameterSchema(Schema):
    uid = fields.Integer(required=True)

    # noinspection PyUnusedLocal
    @post_load()
    def get_parameter(self, item, many, **kwargs):
        parameter = ParameterDao.query.get(item["uid"])  # @UndefinedVariable
        if parameter is None:
            message = f"No parameter with uid={item['uid']} was found"
            raise ValidationError(message)
        return parameter


class NewParameterSchema(Schema):
    uid = fields.Integer(load_only=True)
    name = fields.String(
        required=True, allow_none=False, validate=validate.Length(min=1)
    )
    values = fields.List(fields.String(validate=validate.Length(min=1)))
    parameter_set = fields.Pluck("ParameterSetSchema", "uid", allow_none=True)
    position = fields.Integer(load_only=True)
    excluded = fields.Pluck("ParameterSchema", "uid", many=True)
    excluded_by = fields.Pluck("ParameterSchema", "uid", many=True)

    @validates("uid")
    def validate_uid(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")

    @validates("position")
    def validate_position(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")


MoveParameterSchema = MoveSchema


class UpdateParameterSchema(Schema):
    uid = fields.Integer(load_only=True)
    name = fields.String(
        required=True, allow_none=False, validate=validate.Length(min=1)
    )
    values = fields.Nested("ValueSchema", many=True)
    parameter_set = fields.Pluck("ParameterSetSchema", "uid", allow_none=True)
    position = fields.Integer(load_only=True)
    excluded = fields.Pluck("ParameterSchema", "uid", many=True)
    excluded_by = fields.Pluck("ParameterSchema", "uid", many=True)

    @validates("uid")
    def validate_uid(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")

    @validates("position")
    def validate_position(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")


class ParameterExclusionSchema(ma_sq.SQLAlchemySchema):
    class Meta:
        model = ParameterDao
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = orm_utils.orm_session()

    uid = fields.Integer()
    name = fields.String(required=True)
    excluded = fields.Nested(
        ParameterSchema(only=("name", "uid")), many=True, dump_only=True
    )
    excluded_by = fields.Nested(
        ParameterSchema(only=("name", "uid")), many=True, dump_only=True
    )
