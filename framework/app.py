from framework.services.auth import AuthService
from framework.transport.api_client import ApiClient
from framework.services.balances import BalanceService
from framework.services.orders import OrderService


class Api:
    def __init__(self, client: ApiClient):
        self.client = client
        self.auth = AuthService(self.client)
        self.balances = BalanceService(self.client)
        self.orders = OrderService(self.client)