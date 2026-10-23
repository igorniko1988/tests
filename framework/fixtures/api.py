import pytest
from framework.transport.api_client import ApiClient
from framework.app import Api
from framework.config.settings import settings


@pytest.fixture()
def api():
    api_client = ApiClient(settings.base_url, settings.timeout)
    yield Api(api_client)
    api_client.session.close()


@pytest.fixture()
def auth_api(api, credentials):
    api.auth.register(**credentials)
    login = api.auth.login(**credentials)
    assert login.status_code == 200
    api.client.set_token(login.json()['access_token'])
    return api