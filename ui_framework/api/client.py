from playwright.sync_api import APIRequestContext, APIResponse
from ui_framework.data.models import OrderData

class ExchangeApi:
    def __init__(self, ctx: APIRequestContext):
        self.ctx = ctx
        self.headers = {}
        self.token = None

    def register(self, email, password):
        return self.ctx.post('/auth/register', data={'email': email, 'password': password})

    def login(self, email, password):
        response = self.ctx.post('/auth/login', data={'email': email, 'password': password})
        self.token = response.json()['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}
        return response

    def deposit(self, asset, amount):
        return self.ctx.post('/balances/deposit', data={'asset': asset, 'amount': amount}, headers=self.headers)

    def place_order(self, order: OrderData):
        data = {'symbol': order.symbol, 'side': order.side, 'price': order.price, 'quantity': order.quantity}
        return self.ctx.post('/orders', data=data, headers=self.headers)
