import pytest
from playwright.sync_api import Page
from faker import Faker
from ui_framework.application import Application
from collections.abc import Callable

faker = Faker()


@pytest.fixture
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture
def logged_user(request: pytest.FixtureRequest, app: Application, credentials: dict[str, str]) -> Application:
    app.auth_page.open().fill_credentials(credentials["email"], credentials["password"]).click_register()
    app.dashboard_page.wait_loaded()

    marker = request.node.get_closest_marker('balance')
    if marker:
        for asset,amount in marker.kwargs.items():
            app.dashboard_page.deposit_form.deposit(asset, amount)
    return app


@pytest.fixture
def new_app(new_context) -> Callable[[], Application]:

    def create_app():
        page = new_context().new_page()
        app = Application(page)
        app.auth_page.open().fill_credentials(faker.unique.email(), faker.password()).click_register()
        app.dashboard_page.wait_loaded()
        return app
    return create_app

@pytest.fixture
def order_factory(logged_user):
    orders = []
    dashboard = logged_user.dashboard_page

    def create(side, price, quantity):
        response = dashboard.order_form.place(side, price, quantity)
        orders.append(response.json()['id'])
        return response
    yield create

    for order in orders:
        row = dashboard.orders.row(order)
        if row.cancel_button.count():
            row.cancel()
        print(f'teardown: order was deleted {order}')