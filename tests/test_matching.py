from decimal import Decimal

from framework.models.order import Order, OrderStatus
from framework.utils.waiting import wait_until

# Своя цена, чтобы не пересечься с ордерами других тестов (у них ETH-USDT и цены до 5)
PRICE = "30000"


def place(user, side, quantity, price=PRICE) -> Order:
    response = user.orders.create_order("BTC-USDT", side, price=price, quantity=quantity)
    assert response.status_code == 201, response.text
    return Order.model_validate(response.json())


def wait_for_status(user, order: Order, status: OrderStatus) -> Order:
    def check():
        current = user.get_order(order.id)
        return current if current.status == status else None

    return wait_until(check, message=f"ордер {order.id} в статусе {status}")


def test_buy_and_sell_are_filled(make_user):
    alice, bob = make_user(), make_user()
    alice.balances.deposit("USDT", "60000")
    bob.balances.deposit("BTC", "2")

    buy = place(alice, "BUY", "2")
    sell = place(bob, "SELL", "2")

    wait_for_status(alice, buy, OrderStatus.FILLED)
    wait_for_status(bob, sell, OrderStatus.FILLED)

    assert alice.get_balance("BTC").available == 2
    assert alice.get_balance("USDT").locked == 0
    assert bob.get_balance("USDT").available == 60000
    assert bob.get_balance("BTC").locked == 0


def test_partial_fill(make_user):
    alice, bob = make_user(), make_user()
    alice.balances.deposit("USDT", "90000")
    bob.balances.deposit("BTC", "1")

    buy = place(alice, "BUY", "3")
    place(bob, "SELL", "1")

    order = wait_for_status(alice, buy, OrderStatus.PARTIALLY_FILLED)

    assert order.filled_quantity == 1
    usdt = alice.get_balance("USDT")
    assert usdt.locked == 60000  # ещё не исполненные 2 BTC
    assert alice.get_balance("BTC").available == 1


def test_buyer_gets_better_price_back(make_user):
    alice, bob = make_user(), make_user()
    bob.balances.deposit("BTC", "1")
    alice.balances.deposit("USDT", "31000")

    sell = place(bob, "SELL", "1", price="30000")  # раньше: его цена и будет ценой сделки
    buy = place(alice, "BUY", "1", price="31000")

    wait_for_status(alice, buy, OrderStatus.FILLED)
    wait_for_status(bob, sell, OrderStatus.FILLED)

    # блокировали по 31000, исполнилось по 30000 — разница вернулась
    assert alice.get_balance("USDT").available == Decimal("1000")
    assert bob.get_balance("USDT").available == Decimal("30000")
