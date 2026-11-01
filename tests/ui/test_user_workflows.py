import allure
import pytest
from playwright.sync_api import expect

from framework.api.models.order import CreateOrder
from framework.utils.money import format_amount


@allure.epic('Биржа')
@allure.feature('Авторизация')
@allure.story('Регистрация')
@allure.title('Регистрация с валидными данными открывает кабинет')
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
def test_user_can_register_with_valid_credentials(app, credentials):
    app.auth_page.open().fill_credentials(credentials['email'], credentials['password']).click_register()
    app.dashboard_page.wait_loaded()

    with allure.step('Проверить email пользователя в шапке'):
        expect(app.dashboard_page.header.email).to_have_text(credentials['email'])


@pytest.mark.parametrize('email,password', [
    ('sadasdsa', ''),
    ('asdasdas', 'asoj23213po'),
])
def test_register_with_invalid_credentials(app, email, password):
    app.auth_page.open().fill_credentials(email, password).click_register()

    with allure.step('Проверить ошибку регистрации'):
        expect(app.auth_page.error_message).to_contain_text('valid email address')
        expect(app.dashboard_page.dashboard).to_be_hidden()


@allure.epic('Биржа')
@allure.feature('Баланс')
@allure.story('Пополнение')
@allure.title('Пополнение USDT увеличивает доступный баланс')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_check_deposit_money_success(logged_user):
    dashboard = logged_user.dashboard_page

    response = dashboard.deposit_form.deposit('USDT', '10')

    with allure.step('Проверить, что баланс пополнен'):
        assert response.ok, response.text()
        expect(dashboard.balances.available('USDT')).to_have_text('10')


def test_place_order_with_not_enough_balance(logged_user):
    dashboard = logged_user.dashboard_page

    response = dashboard.order_form.place('BUY', '1', '2', symbol='BTC-USDT')

    with allure.step('Проверить отказ из-за нехватки баланса'):
        assert response.status == 400, response.text()
        expect(dashboard.order_form.error).to_have_text('Not enough USDT to place order')


@allure.epic('Биржа')
@allure.feature('Ордера')
@allure.story('Блокировка средств')
@allure.title('BUY-ордер блокирует стоимость в USDT')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.balance(USDT='1000')
def test_place_order_with_enough_balance(logged_user):
    order_data = CreateOrder(price='100.5', quantity='2')
    dashboard = logged_user.dashboard_page

    response = dashboard.order_form.place(order_data.side, order_data.price, order_data.quantity, order_data.symbol)

    with allure.step('Проверить, что стоимость ордера заблокирована'):
        assert response.ok, response.text()
        expect(dashboard.balances.locked('USDT')).to_have_text(format_amount(order_data.cost))
        expect(dashboard.balances.available('USDT')).to_have_text(format_amount(1000 - order_data.cost))

    with allure.step('Убрать за собой: отменить ордер'):
        dashboard.orders.row(response.json()['id']).cancel()

@pytest.mark.balance(ETH='2')
def test_user_with_balance(logged_user):
    balance = logged_user.dashboard_page.balances

    with allure.step('Проверить баланс из маркера'):
        expect(balance.available('ETH')).to_have_text('2')

@pytest.mark.balance(USDT="10")
def test_cleanup_skips_cancelled_order(order_factory, logged_user):
    with allure.step('Создать 3 ордера'):
        orders = [order_factory('BUY','1','1') for _ in range(3)]
    first_id = orders[0].json()["id"]

    with allure.step('Отменить первый ордер вручную'):
        logged_user.dashboard_page.orders.row(first_id).cancel()
        expect(logged_user.dashboard_page.orders.row(first_id).status).to_have_text("CANCELED")


def test_deposit_each_asset(logged_user, asset):
    dashboard = logged_user.dashboard_page
    response = dashboard.deposit_form.deposit(asset, "1")

    with allure.step(f'Проверить, что {asset} пополнен на 1'):
        assert response.ok
        expect(dashboard.balances.available(asset)).to_have_text("1")


@allure.issue('DEMO-1')
@pytest.mark.xfail(strict=True, reason='демо: артефакты при падении')
def test_artifacts_on_failure(logged_user):
    expect(logged_user.dashboard_page.header.email).to_have_text('wrong@email.com', timeout=1000)


@allure.epic('Биржа')
@allure.feature('Баланс')
@allure.story('Пополнение')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize('amount', ['0', '-5', 'abc'])
def test_deposit_invalid_amount(logged_user, amount):
    allure.dynamic.title(f'Пополнение на {amount!r} отклоняется')
    dashboard = logged_user.dashboard_page

    response = dashboard.deposit_form.deposit('USDT', amount)

    with allure.step('Проверить отказ и нулевой баланс'):
        assert not response.ok, response.text()
        expect(dashboard.balances.available('USDT')).to_have_text('0')

