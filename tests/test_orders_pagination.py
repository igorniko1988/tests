from framework.models.order import Order


def create_orders(user, count: int) -> list[str]:
    ids = []
    for _ in range(count):
        response = user.orders.create_order("ETH-USDT", "BUY", price="1", quantity="1")
        ids.append(response.json()["id"])
    return ids


def test_pages_cover_all_orders_once(funded_user):
    created = create_orders(funded_user, 5)

    seen, cursor = [], None
    while True:
        response = funded_user.orders.get_orders(limit=2, cursor=cursor)
        seen += [Order.model_validate(o).id for o in response.json()]
        cursor = response.headers.get("X-Next-Cursor")
        if cursor is None:  # страниц больше нет
            break

    assert len(seen) == len(set(seen)) == 5  # без дублей и пропусков
    assert {str(i) for i in seen} == set(created)


def test_new_orders_do_not_shift_pages(funded_user):
    create_orders(funded_user, 4)

    first = funded_user.orders.get_orders(limit=2)
    create_orders(funded_user, 3)  # пока «листаем», появились новые ордера
    second = funded_user.orders.get_orders(limit=2, cursor=first.headers["X-Next-Cursor"])

    first_ids = {o["id"] for o in first.json()}
    second_ids = {o["id"] for o in second.json()}
    assert first_ids.isdisjoint(second_ids)  # новые ордера не «сдвинули» вторую страницу
    assert len(second_ids) == 2


def test_broken_cursor_is_rejected(funded_user):
    response = funded_user.orders.get_orders(cursor="not-a-cursor")

    assert response.status_code == 400
