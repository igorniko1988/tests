from playwright.sync_api import Page, expect
import pytest


def test_user_can_register_with_valid_credentials(app, credentials):
    app.auth_page.open().fill_credentials(credentials['email'], credentials['password']).click_register()
    app.dashboard_page.wait_loaded()
    expect(app.dashboard_page.header.email).to_have_text(credentials['email'])


@pytest.mark.parametrize('email,password', [
    ('sadasdsa', ''),
    ('asdasdas', 'asoj23213po'),
])
def test_register_with_invalid_credentials(app, email, password):
    app.auth_page.open().fill_credentials(email, password).click_register()
    expect(app.auth_page.error_message).to_contain_text('valid email address')
    expect(app.dashboard_page.dashboard).to_be_hidden()


def test_check_deposit_money_success(logged_user):
    dashboard = logged_user.dashboard_page

    response = dashboard.deposit_form.deposit('USDT', '10')

    assert response.ok, response.text()
    expect(dashboard.balances.available('USDT')).to_have_text('10')


def test_place_order_with_not_enough_balance(logged_user):
    dashboard = logged_user.dashboard_page

    response = dashboard.order_form.place('BUY', '1', '2', symbol='BTC-USDT')

    assert response.status == 400, response.text()
    expect(dashboard.order_form.error).to_have_text('Not enough USDT to place order')


def test_place_order_with_enough_balance(logged_user):
    dashboard = logged_user.dashboard_page
    dashboard.deposit_form.deposit('USDT', '10')

    response = dashboard.order_form.place('BUY', '1', '2', symbol='BTC-USDT')

    assert response.ok, response.text()
    expect(dashboard.balances.locked('USDT')).to_have_text('2')
    dashboard.orders.row(response.json()['id']).cancel()
