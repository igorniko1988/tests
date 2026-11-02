from playwright.sync_api import expect

# --- а) ошибка формы ордера ---

def test_order_with_empty_price_shows_form_error(logged_user):
    dashboard = logged_user.dashboard_page

    response = dashboard.order_form.place('BUY', '', '1')

    assert response.status == 422, response.text()
    expect(dashboard.order_form.error).to_be_visible()
    expect(dashboard.order_form.error).to_contain_text('price')
    # Положительный признак загрузки таблицы — и только потом проверка «строк нет»
    expect(dashboard.orders.empty).to_be_visible()
    expect(dashboard.orders.rows).to_have_count(0)


# --- б) строка таблицы, отмена и фильтр ---

def test_cancel_one_of_three_orders_and_filter_by_status(logged_user):
    dashboard = logged_user.dashboard_page
    dashboard.deposit_form.deposit('USDT', '100')
    ids = {}
    for price in ('10', '20', '30'):
        response = dashboard.order_form.place('BUY', price, '1')
        assert response.ok, response.text()
        ids[price] = response.json()['id']

    response = dashboard.orders.row(ids['20']).cancel()
    assert response.ok, response.text()

    dashboard.orders.filter_by_status('CANCELED')
    expect(dashboard.orders.rows).to_have_count(1)
    expect(dashboard.orders.row(ids['20']).cell('Цена')).to_have_text('20')

    dashboard.orders.filter_by_status('NEW')
    expect(dashboard.orders.table.column('Цена')).to_have_text(['30', '10'])

    # Уборка: не оставляем открытые ордера в общем стакане
    for price in ('30', '10'):
        dashboard.orders.row(ids[price]).cancel()


# --- в) таблица балансов ---

def test_new_user_has_zero_balances(logged_user):
    balances = logged_user.dashboard_page.balances

    # Стенд отдаёт активы по алфавиту; в форме пополнения порядок другой (USDT первым)
    expect(balances.table.column('Актив')).to_have_text(['BTC', 'ETH', 'USDT'])
    for asset in ('BTC', 'ETH', 'USDT'):
        expect.soft(balances.available(asset)).to_have_text('0')


# --- г) выход через шапку и повторный вход ---

def test_logout_and_login_again(logged_user, credentials):
    logged_user.dashboard_page.header.logout()
    logged_user.auth_page.wait_loaded()

    logged_user.auth_page.fill_credentials(credentials['email'], credentials['password']).click_login()

    logged_user.dashboard_page.wait_loaded()
    expect(logged_user.dashboard_page.header.email).to_have_text(credentials['email'])
