from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr


# pylint: disable=no-self-argument, no-member


# noinspection PyMethodParameters,PyUnresolvedReferences
class OrmResource(Model):
    @declared_attr
    def uid(cls):  # @NoSelf
        for base in cls.__mro__[1:-1]:
            if getattr(base, "__table__", None) is not None:
                uid_type = sa.ForeignKey(base.uid)
                break
        else:
            uid_type = sa.Integer

        return sa.Column(uid_type, primary_key=True)

    @declared_attr
    def position(cls):  # @NoSelf
        for base in cls.__mro__[1:-1]:
            if getattr(base, "__table__", None) is not None:
                position_type = sa.ForeignKey(base.position)
                break
        else:
            position_type = sa.Integer

        return sa.Column(position_type)


ORM = SQLAlchemy(model_class=OrmResource)
