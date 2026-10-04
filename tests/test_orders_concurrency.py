from concurrent.futures import ThreadPoolExecutor

from framework.actors.user import LoggedInUser


def place_orders_at_once(user: LoggedInUser, count: int) -> list[int]:
    """Отправляет count одинаковых ордеров одновременно, возвращает коды ответов."""

    def place(_):
        response = user.orders.create_order("ETH-USDT", "BUY", price="1", quantity="1")
        return response.status_code

    with ThreadPoolExecutor(max_workers=count) as pool:
        return list(pool.map(place, range(count)))


def test_concurrent_orders_do_not_overspend(make_user):
    alice = make_user()
    alice.balances.deposit("USDT", "10").raise_for_status()

    # 50 ордеров по 1 USDT одновременно, а денег хватает только на 10
    codes = place_orders_at_once(alice, count=50)

    assert codes.count(201) == 10
    assert codes.count(400) == 40

    usdt = alice.get_balance("USDT")
    assert usdt.available == 0
    assert usdt.locked == 10
