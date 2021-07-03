from sqlalchemy.ext.orderinglist import ordering_list

from .base import ORM
from .value import ValueDao
from .parmset import ParameterSetDao
from .parameter import ParameterDao


ParameterSetDao.parameter_class = ParameterDao

ParameterDao.value_class = ValueDao

exclusions = ORM.Table(
    "exclusions",
    ORM.Column("excluder_id", ORM.Integer, ORM.ForeignKey("parameters.uid")),
    ORM.Column("excluded_id", ORM.Integer, ORM.ForeignKey("parameters.uid")),
)

ParameterDao.values = ORM.relationship(
    "ValueDao",
    backref="parameter",
    order_by="ValueDao.position",
    collection_class=ordering_list("position"),
)

ParameterDao.excluded = ORM.relationship(
    "ParameterDao",
    secondary=exclusions,
    primaryjoin="exclusions.c.excluder_id == ParameterDao.uid",
    secondaryjoin="exclusions.c.excluded_id == ParameterDao.uid",
    order_by="ParameterDao.uid",
    backref=ORM.backref("excluded_by", order_by="ParameterDao.uid", lazy="dynamic"),
    lazy="dynamic",
)

ParameterSetDao.parameters = ORM.relationship(
    "ParameterDao",
    backref="parameter_set",
    order_by="ParameterDao.position",
    collection_class=ordering_list("position"),
)
