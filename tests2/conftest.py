import pytest

from framework2.api.auth import AuthApi
from framework2.client import ApiClient
from framework2.config import Config, load_config
from framework2.session import UserSession, register_user


@pytest.fixture(scope="session")
def config() -> Config:
    return load_config()


@pytest.fixture(scope="session")
def client(config):
    """Клиент без токена — для публичных запросов (регистрация, логин, проверки 401)."""
    with ApiClient(config.base_url, config.timeout) as client:
        yield client


@pytest.fixture(scope="session")
def auth_api(client) -> AuthApi:
    return AuthApi(client)


@pytest.fixture
def make_user(config):
    """Фабрика: каждый вызов — новый залогиненный пользователь. После теста сессии закрываются."""
    users: list[UserSession] = []

    def create() -> UserSession:
        user = register_user(config)
        users.append(user)
        return user

    yield create

    for user in users:
        user.close()


@pytest.fixture
def user(make_user) -> UserSession:
    """Один залогиненный пользователь — самый частый случай."""
    return make_user()


@pytest.fixture
def rich_user(make_user) -> UserSession:
    """Пользователь, у которого уже есть 100 USDT."""
    user = make_user()
    user.balances.deposit("USDT", "100").raise_for_status()
    return user
