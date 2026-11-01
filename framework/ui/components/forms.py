import logging

import allure
from playwright.sync_api import Page

log = logging.getLogger('ui')


class DepositForm:
    def __init__(self, page: Page):
        self.page = page
        self.asset = page.get_by_test_id('deposit-asset')
        self.amount = page.get_by_test_id('deposit-amount')
        self.submit_button = page.get_by_test_id('deposit-button')

    @allure.step('Пополнить {asset} на {amount}')
    def deposit(self, asset, amount):
        log.info('deposit: %s %s', asset, amount)
        is_deposit = lambda r: r.request.method == 'POST' and r.url.endswith('/balances/deposit')  # noqa: E731
        with self.page.expect_response(is_deposit) as info:
            self.asset.select_option(asset)
            self.amount.fill(amount)
            self.submit_button.click()
        log.info('deposit response: %s', info.value.status)
        return info.value


class OrderForm:
    def __init__(self, page: Page):
        self.page = page
        self.symbol = page.get_by_test_id('order-symbol')
        self.radio_buy = page.get_by_role('radio', name='Купить')
        self.radio_sell = page.get_by_role('radio', name='Продать')
        self.price = page.get_by_test_id('order-price')
        self.quantity = page.get_by_test_id('order-quantity')
        self.error = page.get_by_test_id('order-error')
        self.submit_button = page.get_by_test_id('place-order-button')

    def side(self, side):
        (self.radio_buy if side == 'BUY' else self.radio_sell).check()

    @allure.step('Выставить ордер {side} {quantity} × {price} ({symbol})')
    def place(self, side, price, quantity, symbol='ETH-USDT'):
        log.info('place order: %s %s x %s %s', side, quantity, price, symbol)
        with self.page.expect_response(lambda r: r.request.method == 'POST' and r.url.endswith('/orders')) as info:
            self.symbol.select_option(symbol)
            self.side(side)
            self.price.fill(price)
            self.quantity.fill(quantity)
            self.submit_button.click()
        response = info.value
        order_id = response.json().get('id') if response.ok else None
        log.info('place order response: %s, id=%s', response.status, order_id)
        return response
