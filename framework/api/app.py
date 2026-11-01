"""Фасад API-слоя: один объект со всеми сервисами — api.auth, api.balances, api.orders."""

from framework.api.client import ApiClient
from framework.api.services.auth import AuthService
from framework.api.services.balances import BalanceService
from framework.api.services.orders import OrderService


class Api:
    def __init__(self, client: ApiClient) -> None:
        self.client = client
        self.auth = AuthService(client)
        self.balances = BalanceService(client)
        self.orders = OrderService(client)
