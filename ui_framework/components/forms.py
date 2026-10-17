from playwright.sync_api import Page


class DepositForm:
    def __init__(self, page: Page):
        self.page = page
        self.asset = page.get_by_test_id('deposit-asset')
        self.amount = page.get_by_test_id('deposit-amount')
        self.submit_button = page.get_by_test_id('deposit-button')

    def deposit(self, asset, amount):
        with self.page.expect_response(lambda r: r.request.method == 'POST' and r.url.endswith('/balances/deposit')) as info:
            self.asset.select_option(asset)
            self.amount.fill(amount)
            self.submit_button.click()
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

    def place(self, side, price, quantity, symbol='ETH-USDT'):
        with self.page.expect_response(lambda r: r.request.method == 'POST' and r.url.endswith('/orders')) as info:
            self.symbol.select_option(symbol)
            self.side(side)
            self.price.fill(price)
            self.quantity.fill(quantity)
            self.submit_button.click()
        return info.value
