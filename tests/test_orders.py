from framework.models.order import Order, OrderStatus


def test_create_order(make_user):
    alice = make_user()
    alice.balances.deposit("USDT", "10")

    response = alice.orders.create_order("ETH-USDT", "BUY", price="2", quantity="3")

    assert response.status_code == 201
    order = Order.model_validate(response.json())
    assert order.status == OrderStatus.NEW
    assert order.filled_quantity == 0

    usdt = alice.get_balance("USDT")
    assert usdt.available == 4
    assert usdt.locked == 6


def test_cancel_order(make_user):
    alice = make_user()
    alice.balances.deposit("USDT", "10")
    created = alice.orders.create_order("ETH-USDT", "BUY", price="2", quantity="3")
    order = Order.model_validate(created.json())

    response = alice.orders.cancel_order(order.id)

    assert response.status_code == 200
    assert Order.model_validate(response.json()).status == OrderStatus.CANCELED

    usdt = alice.get_balance("USDT")
    assert usdt.available == 10
    assert usdt.locked == 0


def test_user_cannot_cancel_foreign_order(make_user):
    alice = make_user()
    bob = make_user()
    alice.balances.deposit("USDT", "10")
    created = alice.orders.create_order("ETH-USDT", "BUY", price="2", quantity="3")
    order = Order.model_validate(created.json())

    response = bob.orders.cancel_order(order.id)

    assert response.status_code == 404
    assert alice.orders.get_order(order.id).json()["status"] == OrderStatus.NEW
