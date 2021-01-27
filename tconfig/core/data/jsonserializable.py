"""
Mixin to allow a class to be serialized as a JSON string.
"""

import json

from uuid import uuid4, UUID
from typing import Dict, Optional, Union, TypeVar

# pylint: disable=unsubscriptable-object

T = TypeVar('T')
UidType = Optional[Union[UUID, str, int]]


class JsonSerializable(object):

    def __init__(self, uid: UidType = None):
        """
        Assign a unique identifier to the instance.

        For testing purposes only:  if keyword argument 'uid' is provided,
        use that value instead.
        """
        super().__init__()
        if hasattr(self, "metadata"):
            return
        if isinstance(uid, UUID):
            self.uid = uid
        elif isinstance(uid, str):
            self.uid = UUID(uid)
        else:
            self.uid: UUID = uuid4()

    def __repr(self):
        return f"JsonSerializable(uid={self.uid})"
    
    def to_dict(self) -> Dict:
        """
        Returns a representation of the instance as a dictionary with
        values that are numeric / booleans / strings / lists.
        """
        return {
            "uid": str(self.uid) if isinstance(self.uid, UUID) else self.uid
        }

    def to_json(self) -> str:
        """
        Returns a JSON string representation of the instance.

        Converts the ``to_dict()`` representation to a string.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls: T, cls_dict: Dict) -> T:
        """
        Create a new object instance from a dictionary of attribute
        values.
        """
        raise NotImplementedError("Subclasses should implement method 'from_dict()'")

    @classmethod
    def from_json(cls: T, cls_json) -> T:
        """
        Create an object instance from a JSON representation.

        Load the JSON string into a Python dictionary, and
        then call ``from_dict`` to create the object instance.
        """
        return cls.from_dict(json.loads(cls_json))
