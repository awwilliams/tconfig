"""
Created on Jul 4, 2020

@author: Alan Williams
"""
from tconfig.core.data import Value

from tconfig.orm import ORM


# noinspection PyTypeChecker
class ValueDao(Value, ORM.Model):
    __tablename__ = 'vals'
    name = ORM.Column(ORM.String(64), nullable=False)
    parameter_id = ORM.Column(ORM.Integer, ORM.ForeignKey('parameters.uid'))

    def __eq__(self, other: Value) -> bool:
        """
        Equality:  name and UUID (if present) must agree.
        """
        return self.name == other.name

    def __hash__(self) -> int:
        """
        Hash code:  use name and UUID (if present).
        """
        return hash(self.name)

    def __repr__(self) -> str:
        return f"ValueDao(name={self.name}, uid={self.uid})"

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "position": self.position,
        })
        return result

    @classmethod
    def from_dict(cls, cls_dict: dict) -> 'ValueDao':
        result = super().from_dict(cls_dict)
        result.position = cls_dict["position"]
        return result
