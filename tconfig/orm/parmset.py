"""
Created on Jul 4, 2020

@author: Alan Williams
"""

from sqlalchemy.ext.orderinglist import ordering_list

from tconfig.api.service import ORM
from tconfig.core.data import ParameterSet


class ParameterSetDao(ParameterSet, ORM.Model):
    __tablename__ = 'parameter_sets'

    name = ORM.Column(ORM.String(64))
    parameters = ORM.relationship(
        'ParameterDao', backref='parameter_set', order_by="ParameterDao.position",
        collection_class=ordering_list('position')
    )

    @classmethod
    def _parameter_class(cls):
        from tconfig.orm.parameter import ParameterDao
        return ParameterDao
