from framework.services.auth_service import Auth
from framework.transport.api_client import ApiClient
from framework.services.balances import Balance
from framework.services.orders import Order


class Api:
    def __init__(self, client: ApiClient):
        self.client = client
        self.auth = Auth(self.client)
        self.balances = Balance(self.client)
        self.orders = Order(self.client)