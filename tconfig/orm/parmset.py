"""
Created on Jul 4, 2020

@author: Alan Williams
"""

from tconfig.core.data import ParameterSet
from tconfig.orm import ORM


class ParameterSetDao(ParameterSet, ORM.Model):
    __tablename__ = "parameter_sets"

    name = ORM.Column(ORM.String(64))

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update(
            {
                "position": self.position,
            }
        )
        return result

    @classmethod
    def from_dict(cls, cls_dict) -> "ParameterSetDao":
        result = super().from_dict(cls_dict)
        result.position = cls_dict["position"]
        return result
