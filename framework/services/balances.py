from framework.transport.api_client import ApiClient


class Balance:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_balance(self):
        return self.api_client.get('/balances')

    def deposit(self, asset, amount):
        return self.api_client.post('/balances/deposit', json={'asset': asset, 'amount': amount})