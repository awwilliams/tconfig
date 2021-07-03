from flask_restx import abort
from sqlalchemy.exc import SQLAlchemyError

from tconfig.orm import orm_utils


def exception_500(exception):
    message = str(exception)
    abort_args = {"error": "internal server error", "message": message}
    abort(500, **abort_args)


def perform_orm_commit_or_500(items, operation="add"):
    try:
        orm_utils.orm_commit(items, operation)
    except SQLAlchemyError as orm_err:
        exception_500(orm_err)
