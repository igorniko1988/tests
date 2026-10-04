from decimal import Decimal

from framework.models.order import Order


def test_order_saved_in_db(funded_user, db):
    response = funded_user.orders.create_order("ETH-USDT", "BUY", price="2", quantity="3")
    order = Order.model_validate(response.json())

    row = db.get_order(order.id)

    assert row is not None
    assert row["status"] == "NEW"
    assert row["price"] == Decimal("2")
    assert row["quantity"] == Decimal("3")
    assert row["filled_quantity"] == 0


def test_order_locks_balance_in_db(funded_user, db):
    funded_user.orders.create_order("ETH-USDT", "BUY", price="2", quantity="3")

    row = db.get_balance(funded_user.email, "USDT")

    assert row["available"] == Decimal("94")
    assert row["locked"] == Decimal("6")
