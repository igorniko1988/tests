"""Фикстуры UI-слоя: браузерные страницы через фасад Application. Фикстуры только готовят состояние."""

from collections.abc import Callable, Iterator

import pytest
from playwright.sync_api import Page

from framework.api.app import Api
from framework.config.settings import Settings
from framework.data.generators import credentials as generate_credentials
from framework.ui.application import Application


def open_app(page: Page, settings: Settings) -> Application:
    # Таймаут действий (click, fill) — из настроек, одинаковый для всех страниц теста
    page.set_default_timeout(settings.action_timeout_ms)
    return Application(page)


def register_in_browser(app: Application, credentials: dict[str, str]) -> Application:
    app.auth_page.open().fill_credentials(credentials["email"], credentials["password"]).click_register()
    app.dashboard_page.wait_loaded()
    return app


@pytest.fixture
def app(page: Page, settings: Settings) -> Application:
    return open_app(page, settings)


@pytest.fixture
def logged_user(request: pytest.FixtureRequest, app: Application, credentials: dict[str, str]) -> Application:
    """Зарегистрирован через UI. Маркер @pytest.mark.balance(USDT="100") — пополнить перед тестом."""
    register_in_browser(app, credentials)
    marker = request.node.get_closest_marker("balance")
    if marker:
        for asset, amount in marker.kwargs.items():
            app.dashboard_page.deposit_form.deposit(asset, amount)
    return app


@pytest.fixture
def new_app(new_context, settings: Settings) -> Callable[[], Application]:
    """Фабрика: второй, третий пользователь — каждый в своём контексте браузера."""

    def create_app() -> Application:
        app = open_app(new_context().new_page(), settings)
        return register_in_browser(app, generate_credentials())

    return create_app


@pytest.fixture
def order_factory(logged_user: Application) -> Iterator[Callable]:
    orders = []
    dashboard = logged_user.dashboard_page

    def create(side, price, quantity):
        response = dashboard.order_form.place(side, price, quantity)
        orders.append(response.json()["id"])
        return response

    yield create

    for order_id in orders:
        row = dashboard.orders.row(order_id)
        if row.cancel_button.count():
            row.cancel()


@pytest.fixture
def login_in_browser(new_context, settings: Settings) -> Callable[[Api, str], Application]:
    """Открыть кабинет сразу залогиненным: токен API-клиента кладём в localStorage до загрузки страницы.

    Так e2e-тест готовит данные быстро через API, а в браузере проверяет только то, что видит пользователь.
    """

    def open_as(api: Api, email: str) -> Application:
        context = new_context(storage_state={
            "cookies": [],
            "origins": [{"origin": settings.base_url, "localStorage": [
                {"name": "token", "value": api.client.token},
                {"name": "email", "value": email},
            ]}],
        })
        app = open_app(context.new_page(), settings)
        app.dashboard_page.open().wait_loaded()
        return app

    return open_as
