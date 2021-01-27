from flask import Flask
import pytest

from tconfig.orm import ORM
from tconfig.api.service import create_app

API_PREFIX = "/tconfig/api/v1"


# pylint: disable=redefined-outer-name

@pytest.fixture
def app():
    app_fixture = create_app('testing')
    app_context = app_fixture.app_context()
    app_context.push()
    ORM.drop_all()
    ORM.create_all()
    yield app_fixture
    ORM.session.remove()
    ORM.drop_all()
    app_context.pop()


@pytest.fixture
def orm(app):
    return ORM


@pytest.fixture
def client(app: Flask):
    return app.test_client(use_cookies=True)


@pytest.fixture
def api_prefix(app):
    return API_PREFIX


@pytest.fixture
def api_client(client, api_prefix):
    setup_response = client.get(f'{api_prefix}/setup')
    if not setup_response.status_code == 200:
        raise RuntimeError(f"Setup route returned code {setup_response.status_code}")
    return client
