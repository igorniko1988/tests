import pytest
from framework.transport.api_client import ApiClient
from framework.config.settings import settings
from faker import Faker



@pytest.fixture()
def api():
    api_client = ApiClient(settings.base_url, settings.timeout)
    yield api_client
    api_client.session.close()


@pytest.fixture()
def auth_api(api):
    faker = Faker()

    data = {
        'email': faker.email(),
        'password': faker.password()
    }

    register = api.post('/auth/register', json=data)
    login = api.post('/auth/login', json=data)
    token = login.json()['access_token']
    api.set_token(token)

    return api