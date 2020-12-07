import typing
import pandas as pd

from marshmallow import post_load
from flask_marshmallow import Schema
from flask_marshmallow.fields import fields

from tconfig.core.data.configset import ConfigurationSet
from tconfig.api.schemas.value import ValueSchema
from tconfig.api.service import ORM

VALUE_SCHEMA = ValueSchema(only=("name", "uid"))


class DataframeConfigsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        # noinspection PyUnresolvedReferences
        df_dict = value.to_dict(orient="index")
        return [{parm_name: VALUE_SCHEMA.dump(value) for parm_name, value in df_dict[index].items()} for index in
                df_dict]

    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        frame_dict = []
        for config in value:
            config_entry = {}
            for parameter_name, value_entry in config.items():
                value_obj = VALUE_SCHEMA.load(value_entry, session=ORM.session)
                config_entry[parameter_name] = value_obj
            frame_dict.append(config_entry)
        result = pd.DataFrame(frame_dict)
        return result


class DataframeParameterNamesField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return []
        return value.columns.tolist()


class ConfigSetSchema(Schema):
    configs = DataframeConfigsField(data_key='configurations')
    parameter_names = DataframeParameterNamesField(dump_only=True, attribute='configs')

    # noinspection PyUnusedLocal
    @post_load
    def make_config_set(self, data, **kwargs):
        orig_df = data["configs"]
        ordered_df = orig_df[data["parameter_names"]]
        return ConfigurationSet(data_frame=ordered_df)
