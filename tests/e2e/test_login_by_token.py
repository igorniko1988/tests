import allure
import pytest
from playwright.sync_api import expect


@allure.epic("Биржа")
@allure.feature("Авторизация")
@allure.title("Браузер открывается залогиненным по токену из API")
@pytest.mark.smoke
def test_browser_logged_in_by_token(auth_api, credentials, login_in_browser):
    app = login_in_browser(auth_api, credentials["email"])

    expect(app.dashboard_page.header.email).to_have_text(credentials["email"])
    expect(app.auth_page.auth_form).to_be_hidden()


@allure.epic("Биржа")
@allure.feature("Баланс")
@allure.title("Депозит через API виден в кабинете")
def test_api_deposit_visible_in_ui(auth_api, credentials, login_in_browser):
    response = auth_api.balances.deposit("USDT", "25.5")
    assert response.status_code == 200

    app = login_in_browser(auth_api, credentials["email"])

    expect(app.dashboard_page.balances.available("USDT")).to_have_text("25.5")
