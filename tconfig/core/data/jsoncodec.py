import json
from typing import Any
from .parmset import ParameterSet


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        # Calling custom encode function:
        json_string = obj
        if callable(getattr(obj, "to_json")):
            json_string = obj.to_json()
        if json_string != obj:  # Encode function has done something
            return json_string  # Return that
        # else let the base class do the work
        return json.JSONEncoder.default(self, obj)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.orig_obj_hook = kwargs.pop("object_hook", None)
        super(CustomJSONDecoder, self).__init__(*args,
                                                object_hook=self.custom_obj_hook, **kwargs)

    def custom_obj_hook(self, dct):
        # Calling custom decode function:
        if 'parm_set' in dct:
            dct['parm_set'] = ParameterSet.from_json(dct['parm_set'])

        if self.orig_obj_hook:  # Do we have another hook to call?
            return self.orig_obj_hook(dct)  # Yes: then do it
        return dct  # No: just return the decoded dict
