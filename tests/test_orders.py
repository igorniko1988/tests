from framework.models.balance import Balance
from framework.models.order import Order, OrderStatus


def get_usdt_balance(balance_api, auth) -> Balance:
    balances = [Balance.model_validate(b) for b in balance_api.get(auth=auth).json()]
    return next(b for b in balances if b.asset == "USDT")


def test_create_order(balance_api, orders_api, bearer_token):
    balance_api.deposit("USDT", "10", auth=bearer_token)

    response = orders_api.create_order(
        "ETH-USDT", "BUY", price="2", quantity="3", auth=bearer_token
    )

    assert response.status_code == 201
    order = Order.model_validate(response.json())
    assert order.status == OrderStatus.NEW
    assert order.filled_quantity == 0

    usdt = get_usdt_balance(balance_api, bearer_token)
    assert usdt.available == 4
    assert usdt.locked == 6


def test_cancel_order(balance_api, orders_api, bearer_token):
    balance_api.deposit("USDT", "10", auth=bearer_token)
    created = orders_api.create_order("ETH-USDT", "BUY", price="2", quantity="3", auth=bearer_token)
    order = Order.model_validate(created.json())

    response = orders_api.cancel_order(order.id, auth=bearer_token)

    assert response.status_code == 200
    canceled = Order.model_validate(response.json())
    assert canceled.status == OrderStatus.CANCELED

    usdt = get_usdt_balance(balance_api, bearer_token)
    assert usdt.available == 10
    assert usdt.locked == 0
