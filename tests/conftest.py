import os

import pytest
from pytest import fixture

from framework.config import Settings
from framework.db.client import Database
from framework.factories.users import create_user, random_credentials
from framework.services.auth import AuthApi
from framework.services.balances import BalancesApi
from framework.services.orders import OrdersApi
from framework.transport.auth import BearerAuth
from framework.transport.client import ApiClient


@fixture(scope="session")
def configs():
    env = os.environ.get("ENV", "docker")
    settings = Settings(_env_file=f"envs/{env}.env")

    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write(f"ENV={env}\n")
        f.write(f"BASE_URL={settings.base_url}\n")

    return settings


@fixture(scope="session")
def api_client(configs):
    with ApiClient(base_url=configs.base_url, timeout=configs.timeout) as client:
        yield client


@fixture
def user_credential():
    return random_credentials()


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


@fixture(scope="session")
def auth_api(api_client):
    return AuthApi(api_client)


@fixture(scope="session")
def balance_api(api_client):
    return BalancesApi(api_client)


@fixture(scope="session")
def orders_api(api_client):
    return OrdersApi(api_client)


@fixture
def make_user(configs):
    users = []

    def create():
        user = create_user(configs.base_url, configs.timeout)
        users.append(user)
        return user

    yield create

    for user in users:
        user.client.close()


@fixture
def funded_user(make_user):
    """Пользователь, у которого уже есть 100 USDT."""
    user = make_user()
    user.balances.deposit("USDT", "100").raise_for_status()
    return user


@fixture(scope="session")
def db(configs):
    if configs.db_url is None:
        pytest.skip("на этом окружении нет доступа к базе")
    return Database(configs.db_url)
