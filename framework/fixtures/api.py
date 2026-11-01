"""Фикстуры API-слоя: готовят клиента и состояние, проверки делает тест."""

from collections.abc import Callable, Iterator

import pytest

from framework.api.app import Api
from framework.api.client import ApiClient
from framework.api.models.order import CreateOrder
from framework.config.settings import Settings
from framework.data.generators import credentials as generate_credentials


def new_api(settings: Settings) -> Api:
    return Api(ApiClient(settings.base_url, settings.timeout))


def sign_in(api: Api, credentials: dict[str, str]) -> Api:
    """Зарегистрировать и залогинить пользователя, токен положить в сессию клиента."""
    api.auth.register(**credentials)
    login = api.auth.login(**credentials)
    assert login.status_code == 200, f"подготовка: логин не удался {login.status_code} {login.text}"
    api.client.set_token(login.json()["access_token"])
    return api


def cancel_open_orders(api: Api) -> None:
    # Стакан общий: открытые ордера одного теста ломают сделки в другом
    response = api.orders.list()
    if response.status_code != 200:
        return
    for order in response.json():
        if order["status"] in ("NEW", "PARTIALLY_FILLED"):
            api.orders.cancel(order["id"])


@pytest.fixture
def api(settings: Settings) -> Iterator[Api]:
    """Клиент без токена — для регистрации, логина и негативных тестов авторизации."""
    api = new_api(settings)
    yield api
    api.client.close()


@pytest.fixture
def auth_api(api: Api, credentials: dict[str, str]) -> Iterator[Api]:
    """Залогиненный пользователь; после теста — отмена его открытых ордеров."""
    yield sign_in(api, credentials)
    cancel_open_orders(api)


@pytest.fixture
def funded_user(auth_api: Api) -> Api:
    deposit = auth_api.balances.deposit("USDT", "100")
    assert deposit.status_code == 200, f"подготовка: депозит не прошёл {deposit.text}"
    return auth_api


@pytest.fixture
def create_order(funded_user: Api) -> Callable:
    def _create(**data):
        return funded_user.orders.create(CreateOrder(**data))

    return _create


@pytest.fixture
def make_user(settings: Settings) -> Iterator[Callable[[], Api]]:
    """Фабрика: сколько угодно отдельных пользователей в одном тесте, уборка за всеми."""
    users: list[Api] = []

    def _make() -> Api:
        api = sign_in(new_api(settings), generate_credentials())
        users.append(api)
        return api

    yield _make
    for api in users:
        cancel_open_orders(api)
        api.client.close()
