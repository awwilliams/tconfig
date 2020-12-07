from flask import Blueprint
from flask_restx import Api

SERVICE = Blueprint('service', __name__)
API = Api(SERVICE)

