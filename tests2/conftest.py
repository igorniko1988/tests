import pytest
from framework2.core.http_client import HttpClient
from framework2.core.auth import TokenApi
from framework2.core.services.auth import AuthApi
from faker import Faker



@pytest.fixture
def token(auth_api):
    user_data = {
        'email' : Faker().email(),
        'password': Faker().password()
    }

    auth_api.register(**user_data)
    response = auth_api.login(**user_data)
    token = response.json()['access_token']
    return TokenApi(token)

@pytest.fixture(scope='session')
def api_client():
    client = HttpClient(base_url='http://localhost:8080')
    return client

@pytest.fixture
def authorized_api_client(token):
    client = HttpClient(base_url='http://localhost:8080', auth=token)
    return client

@pytest.fixture
def auth_api(api_client):
    auth_api = AuthApi(api_client)
    return auth_api

@pytest.fixture
def authorized_api(authorized_api_client):
    client = AuthApi(authorized_api_client)
    return client




