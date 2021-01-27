import marshmallow_sqlalchemy as ma_sq
from flask_marshmallow.fields import fields
from marshmallow import Schema, ValidationError, validates, validate

from tconfig.orm import orm_utils, ParameterSetDao

from tconfig.api.schemas import ParameterSchema


class ParameterSetSchema(ma_sq.SQLAlchemyAutoSchema):
    class Meta:
        model = ParameterSetDao
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = orm_utils.orm_session()

    uid = fields.Integer()
    name = fields.String(allow_none=True)
    parameters = fields.Nested(ParameterSchema, many=True)


class UpdateParameterSetSchema(Schema):
    uid = fields.Integer(load_only=True)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))
    parameters = fields.Nested('ParameterSchema', many=True)

    @validates('uid')
    def validate_uid(self, data, **kwargs):
        raise ValidationError("Cannot modify read-only field")
