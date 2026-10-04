from framework.models.order import Order, OrderStatus
from framework.utils.waiting import wait_until


def test_order_expires_and_returns_funds(funded_user):
    response = funded_user.orders.create_order(
        "ETH-USDT", "BUY", price="2", quantity="3", expires_in_seconds=1
    )
    order = Order.model_validate(response.json())
    assert order.expires_at is not None
    assert funded_user.get_balance("USDT").locked == 6

    wait_until(
        lambda: funded_user.get_order(order.id).status == OrderStatus.EXPIRED,
        timeout=10,
        message="ордер истёк",
    )

    usdt = funded_user.get_balance("USDT")
    assert usdt.locked == 0
    assert usdt.available == 100


def test_order_without_expiry_stays_open(funded_user):
    response = funded_user.orders.create_order("ETH-USDT", "BUY", price="2", quantity="3")
    order = Order.model_validate(response.json())

    assert order.expires_at is None
    assert order.status == OrderStatus.NEW
