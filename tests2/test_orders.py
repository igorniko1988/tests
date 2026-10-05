from framework2.models.order import Order


def test_create_order_locks_funds(rich_user):
    response = rich_user.orders.create("ETH-USDT", "BUY", price="2", quantity="3")

    assert response.status_code == 201
    order = Order.model_validate(response.json())
    assert order.status == "NEW"

    usdt = rich_user.balance("USDT")
    assert usdt.available == 94
    assert usdt.locked == 6


def test_cancel_order_returns_funds(rich_user):
    created = Order.model_validate(rich_user.orders.create("ETH-USDT", "BUY", "2", "3").json())

    response = rich_user.orders.cancel(created.id)

    assert response.status_code == 200
    assert Order.model_validate(response.json()).status == "CANCELED"
    assert rich_user.balance("USDT").available == 100


def test_user_cannot_cancel_foreign_order(make_user):
    alice, bob = make_user(), make_user()
    alice.balances.deposit("USDT", "10")
    order = Order.model_validate(alice.orders.create("ETH-USDT", "BUY", "2", "3").json())

    response = bob.orders.cancel(order.id)

    assert response.status_code == 404
