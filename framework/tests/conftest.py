import pytest
from framework.transport.api_client import ApiClient
from framework.services.auth_service import Auth
from framework.app import Api
from framework.config.settings import settings
from faker import Faker



@pytest.fixture()
def api_client():
    api_client = ApiClient(settings.base_url, settings.timeout)
    yield api_client
    api_client.session.close()

@pytest.fixture()
def api(api_client):
    application = Api(api_client)
    return application

@pytest.fixture()
def credentials():
    faker = Faker()
    data = {
        'email': faker.email(),
        'password': faker.password(length=12)
    }
    return data

@pytest.fixture()
def auth_api(api_client, credentials):
    auth = Auth(api_client)

    auth.register(**credentials)
    login = auth.login(**credentials)
    token = login.json()['access_token']
    api_client.set_token(token)
    return auth