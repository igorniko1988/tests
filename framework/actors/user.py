from framework.models.balance import Balance
from framework.services.balances import BalancesApi
from framework.services.orders import OrdersApi
from framework.transport.client import ApiClient


class LoggedInUser:
    """Зарегистрированный пользователь со своим авторизованным клиентом."""

    def __init__(self, email: str, client: ApiClient):
        self.email = email
        self.client = client
        self.balances = BalancesApi(client)
        self.orders = OrdersApi(client)

    def get_balance(self, asset: str) -> Balance:
        balances = [Balance.model_validate(b) for b in self.balances.get().json()]
        return next(b for b in balances if b.asset == asset)
