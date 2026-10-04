import os
import uuid

from pytest import fixture

from framework.config import Settings
from framework.services.auth import AuthApi
from framework.services.balances import BalancesApi
from framework.services.orders import OrdersApi
from framework.transport.auth import BearerAuth
from framework.transport.client import ApiClient
from framework.user import LoggedInUser


@fixture(scope="session")
def configs():
    env = os.environ.get("ENV", "docker")
    settings = Settings(_env_file=f"envs/{env}.env")

    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write(f"ENV={env}\n")
        f.write(f"BASE_URL={settings.base_url}\n")

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


@fixture
def orders_api(api_client):
    return OrdersApi(api_client)


@fixture
def make_user(configs, auth_api):
    clients = []

    def create() -> LoggedInUser:
        uid = uuid.uuid4().hex[:8]
        credentials = {"email": f"qa+{uid}@example.com", "password": f"Aa1!{uid}secret"}
        assert auth_api.register(credentials).status_code == 201
        token = auth_api.login(credentials).json()["access_token"]

        client = ApiClient(configs.base_url, configs.timeout, auth=BearerAuth(token))
        clients.append(client)
        return LoggedInUser(credentials["email"], client)

    yield create

    for client in clients:
        client.close()
