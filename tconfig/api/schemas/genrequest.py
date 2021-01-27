from marshmallow import fields, post_load, validates_schema, ValidationError
from flask_marshmallow import Schema
from tconfig.api.schemas import DataframeConfigsField
from tconfig.core.data import GenerationRequest, ConfigurationSet
from tconfig.core.data.genrequest import GENERATORS


# noinspection PyUnusedLocal
class GeneratorRequestSchema(Schema):
    parameter_set = fields.Nested('ParameterSetSchema')
    algorithm_name = fields.String()
    coverage_degree = fields.Integer()
    existing_configurations = DataframeConfigsField()

    @validates_schema
    def validate_schema(self, data, **kwargs):
        coverage_degree = data["coverage_degree"]
        parameter_set = data["parameter_set"]
        algorithm_name = data["algorithm_name"]
        if coverage_degree < 1:
            raise ValidationError(f"Invalid coverage degree '{coverage_degree}': must be > 1")
        if algorithm_name not in GENERATORS:
            raise ValidationError(f"Invalid algorithm name '{algorithm_name}'")
        if coverage_degree > len(parameter_set):
            raise ValidationError(
                f"Coverage degree {coverage_degree} higher than number of parameters {len(parameter_set)}")
        if algorithm_name == "recursive" and coverage_degree >= 3:
            raise ValidationError(f"Coverage degree higher than 2 not yet implemented for recursive algorithm")

    @post_load
    def make_gen_request(self, data, **kwargs):
        orig_df = data["existing_configurations"]
        if orig_df.empty:
            data["existing_configurations"] = ConfigurationSet(data_frame=orig_df)
        else:
            parameter_names = [parameter.name for parameter in data["parameter_set"]]
            data["existing_configurations"] = ConfigurationSet(data_frame=orig_df[parameter_names])
        return GenerationRequest(**data)
