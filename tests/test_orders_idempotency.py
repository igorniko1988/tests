import uuid
from concurrent.futures import ThreadPoolExecutor

from framework.models.error import ErrorResponse


def new_key() -> str:
    return str(uuid.uuid4())


def test_same_key_creates_one_order(funded_user):
    key = new_key()

    first = funded_user.orders.create_order("ETH-USDT", "BUY", "2", "3", idempotency_key=key)
    second = funded_user.orders.create_order("ETH-USDT", "BUY", "2", "3", idempotency_key=key)

    assert first.status_code == second.status_code == 201
    assert first.json()["id"] == second.json()["id"]  # тот же самый ордер
    assert len(funded_user.orders.get_orders().json()) == 1  # в системе он один
    assert funded_user.get_balance("USDT").locked == 6  # деньги заблокированы один раз


def test_without_key_repeat_creates_duplicate(funded_user):
    funded_user.orders.create_order("ETH-USDT", "BUY", "2", "3")
    funded_user.orders.create_order("ETH-USDT", "BUY", "2", "3")

    assert len(funded_user.orders.get_orders().json()) == 2


def test_same_key_with_other_body_is_rejected(funded_user):
    key = new_key()
    funded_user.orders.create_order("ETH-USDT", "BUY", "2", "3", idempotency_key=key)

    response = funded_user.orders.create_order("ETH-USDT", "BUY", "5", "1", idempotency_key=key)

    assert response.status_code == 422
    error = ErrorResponse.model_validate(response.json()).error
    assert error.code == "idempotency_key_reused"


def test_same_key_sent_at_once_creates_one_order(funded_user):
    key = new_key()

    def place(_):
        return funded_user.orders.create_order("ETH-USDT", "BUY", "2", "3", idempotency_key=key)

    with ThreadPoolExecutor(max_workers=10) as pool:
        responses = list(pool.map(place, range(10)))

    assert {r.status_code for r in responses} == {201}
    assert len({r.json()["id"] for r in responses}) == 1
    assert len(funded_user.orders.get_orders().json()) == 1


def test_key_belongs_to_one_user(make_user):
    alice, bob = make_user(), make_user()
    alice.balances.deposit("USDT", "10")
    bob.balances.deposit("USDT", "10")
    key = new_key()

    alice_order = alice.orders.create_order("ETH-USDT", "BUY", "2", "3", idempotency_key=key)
    bob_order = bob.orders.create_order("ETH-USDT", "BUY", "2", "3", idempotency_key=key)

    assert alice_order.json()["id"] != bob_order.json()["id"]
