from flask import Flask
from flask_cors import CORS

from tconfig.config import CONFIG
from tconfig.orm import ORM
from tconfig.api.views import SERVICE, API

from tconfig.api.resources import ValueResource, ValueListResource, ParameterResource, \
    ParameterListResource, ParameterValueListResource, ParameterExclusionResource, \
    ParameterExclusionListResource, ParameterSetResource, GenerateResource, PopulateResource

API_PREFIX = "/tconfig/api/v1"

CORS_OBJ = CORS(resources={r'/tconfig/api/*': {'origins': '*'}})


def create_app(config_name='development') -> Flask:
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)

    CORS_OBJ.init_app(app)
    ORM.init_app(app)
    app.register_blueprint(SERVICE, url_prefix=API_PREFIX)
    API.add_resource(ValueListResource, "/values/", endpoint='value_list')
    API.add_resource(ValueResource, "/values/<int:uid>", endpoint='value')
    API.add_resource(ParameterListResource, "/parameters/", endpoint='parameter_list')
    API.add_resource(ParameterResource, "/parameters/<int:uid>", endpoint='parameter')
    API.add_resource(
        ParameterValueListResource,
        "/parameters/<int:uid>/values/",
        endpoint='parameter_value_list')
    API.add_resource(ParameterExclusionListResource,
                     "/parameters/<int:uid>/exclusions/", endpoint='parameter_exclude_list')
    API.add_resource(ParameterExclusionResource,
                     "/parameters/<int:puid>/exclusions/<int:euid>", endpoint='parameter_exclude')
    API.add_resource(ParameterSetResource, "/parameterset/", endpoint='parameter_set')
    API.add_resource(GenerateResource, "/generate/", endpoint='generate')
    API.add_resource(PopulateResource, "/setup")

    return app


if __name__ == '__main__':
    app_main = create_app()
    # noinspection PyUnresolvedReferences
    setup_response = app_main.get(f'{API_PREFIX}/setup')  # pylint: disable=no-member
    if not setup_response.status_code == 200:
        raise RuntimeError(f"Setup route returned code {setup_response.status_code}")
    app_main.run()
