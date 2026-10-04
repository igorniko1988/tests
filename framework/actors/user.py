from framework.models.balance import Balance
from framework.models.order import Order, OrderStatus
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
        empty = Balance(asset=asset, available=0, locked=0)  # счёта ещё нет — значит, ноль
        return next((b for b in balances if b.asset == asset), empty)

    def get_order(self, order_id) -> Order:
        return Order.model_validate(self.orders.get_order(order_id).json())

    def cancel_open_orders(self) -> None:
        for raw in self.orders.get_orders().json():
            order = Order.model_validate(raw)
            if order.status in (OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED):
                self.orders.cancel_order(order.id)
