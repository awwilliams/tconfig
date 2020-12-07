"""
Created on Jul 4, 2020

@author: Alan Williams
"""
from sqlalchemy.ext.orderinglist import ordering_list

from tconfig.orm import ORM
from tconfig.core.data import Parameter

exclusions = ORM.Table('exclusions',
                       ORM.Column(
                           'excluder_id',
                           ORM.Integer,
                           ORM.ForeignKey('parameters.uid')),
                       ORM.Column(
                           'excluded_id',
                           ORM.Integer,
                           ORM.ForeignKey('parameters.uid'))
                       )


class ParameterDao(Parameter, ORM.Model):
    __tablename__ = 'parameters'

    name = ORM.Column(ORM.String(64))
    values = ORM.relationship('ValueDao', backref='parameter', order_by="ValueDao.position",
                              collection_class=ordering_list('position'))
    parameter_set_id = ORM.Column(
        ORM.Integer, ORM.ForeignKey('parameter_sets.uid'))
    excluded = ORM.relationship(
        'ParameterDao',
        secondary=exclusions,
        primaryjoin='exclusions.c.excluder_id == ParameterDao.uid',
        secondaryjoin='exclusions.c.excluded_id == ParameterDao.uid',
        order_by='ParameterDao.uid',
        backref=ORM.backref('excluded_by', order_by='ParameterDao.uid', lazy='dynamic'),
        lazy='dynamic'
    )

    def __eq__(self, other: "Parameter") -> bool:
        return self.name == other.name and self.values == other.values

    def __hash__(self) -> int:
        return hash((self.name, self.values))

    @classmethod
    def _value_class(cls) -> 'ValueDao':
        from tconfig.orm.value import ValueDao
        return ValueDao

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "position": self.position,
        })
        return result

    @classmethod
    def from_dict(cls, cls_dict) -> 'ParameterDao':
        result = super().from_dict(cls_dict)
        result.position = cls_dict["position"]
        return result

    def exclude_interaction_with(self, other_parm):
        if self.interacts_with(other_parm):
            self.excluded.append(other_parm)
            ORM.session.commit()  # @UndefinedVariable

    def restore_interaction_with(self, other_parm):
        if self.is_excluding(other_parm):
            self.excluded.remove(other_parm)
            ORM.session.commit()  # @UndefinedVariable
        if self.is_excluded_by(other_parm):
            self.excluded_by.remove(other_parm)
            ORM.session.commit()  # @UndefinedVariable

    def is_excluding(self, other_parm):
        return other_parm in self.excluded.all()

    def is_excluded_by(self, other_parm):
        return other_parm in self.excluded_by.all()

    def interacts_with(self, other_parm):
        return not self.is_excluding(
            other_parm) and not self.is_excluded_by(other_parm)
