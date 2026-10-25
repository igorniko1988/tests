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
    yield api

    for order in api.orders.list().json():
        if order['status'] in ['NEW', 'PARTIALLY_FILLED']:
            api.orders.cancel(order['id'])