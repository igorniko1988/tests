import uuid

from pytest import fixture

from framework.config import Settings
from framework.http.auth import BearerAuth
from framework.http.client import ApiClient
from framework.services.auth import AuthApi
from framework.services.balances import BalancesApi


@fixture(scope="session")
def configs():
    settings = Settings()
    return settings


@fixture
def api_client(configs):
    with ApiClient(base_url=configs.base_url, timeout=configs.timeout) as client:
        yield client


@fixture
def user_credential():
    uid = uuid.uuid4().hex[:8]
    return {
        "email": f"qa+{uid}@example.com",
        "password": f"Aa1!{uuid.uuid4().hex[:12]}",
    }


@fixture
def auth_token(auth_api, user_credential):
    response = auth_api.register(user_credential)

    assert response.status_code == 201

    authorised_user = auth_api.login(user_credential)

    assert authorised_user.status_code == 200
    assert "access_token" in authorised_user.json()
    token = authorised_user.json()["access_token"]
    return token


@fixture
def bearer_token(auth_token):
    return BearerAuth(auth_token)


@fixture
def auth_api(api_client):
    return AuthApi(api_client)


@fixture
def balance_api(api_client):
    return BalancesApi(api_client)
