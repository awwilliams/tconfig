"""
Module for named value that a parameter can take.
"""

from .jsonserializable import JsonSerializable, UidType


class Value(JsonSerializable):
    """
    Class representing a parameter value in a test configuration.

    Value can be serialized to be passed from a web interface to
    server API.
    """

    # noinspection PyUnusedLocal
    def __init__(self, name: str = "", uid: UidType = None, **kwargs):  # pylint: disable=unused-argument
        """
        Initialization:  arguments passed through to superclasses/mixins.
        """
        super().__init__(uid=uid)
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}", uid="{self.uid}")'

    def __eq__(self, other: 'Value') -> bool:
        """
        Equality:  name and UUID (if present) must agree.
        """
        return all(getattr(self, attr) == getattr(other, attr) for attr in ["uid", "name"])

    def __hash__(self) -> int:
        """
        Hash code:  use name and UUID (if present).
        """
        return hash((self.name, getattr(self, 'uid')))

    def to_dict(self) -> dict:
        """
        Return a dictionary
        """
        result = super().to_dict()
        result.update({
            "name": self.name,
        })
        return result

    @classmethod
    def from_dict(cls, cls_dict: dict) -> 'Value':
        return cls(name=cls_dict["name"], uid=cls_dict["uid"])
