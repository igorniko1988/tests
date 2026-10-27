import pytest
from framework.transport.api_client import ApiClient
from framework.app import Api
from framework.config.settings import settings
from framework.models.order import CreateOrder
from faker import Faker

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


@pytest.fixture()
def funded_user(auth_api):
    deposit = auth_api.balances.deposit('USDT',100)
    assert deposit.status_code == 200
    return auth_api

@pytest.fixture()
def create_order(funded_user):
    def _create(**data):
        created = funded_user.orders.create(CreateOrder(**data))
        return created
    return _create

@pytest.fixture()
def make_user():
    def _make():
        faker = Faker()
        data = {
            'email': faker.email(),
            'password': faker.password(length=12)
        }
        api_client = ApiClient(settings.base_url, settings.timeout)
        api = Api(api_client)
        api.auth.register(**data)
        token = api.auth.login(**data).json()['access_token']
        api.client.set_token(token)
        return api
    yield _make

