from decimal import Decimal

import pytest

from framework.models.error import ErrorResponse


def test_deposits_add_up_exactly(make_user):
    alice = make_user()
    for _ in range(3):
        alice.balances.deposit("USDT", "0.1")

    # с float было бы 0.30000000000000004
    assert alice.get_balance("USDT").available == Decimal("0.3")


def test_eighteen_decimal_places_are_kept(make_user):
    alice = make_user()

    alice.balances.deposit("USDT", "0.000000000000000001")

    assert alice.get_balance("USDT").available == Decimal("0.000000000000000001")


@pytest.mark.parametrize(
    "amount",
    ["0", "-1", "abc", "0.0000000000000000001", "9999999999999999999"],
    ids=["zero", "negative", "not-a-number", "19-decimals", "19-digits"],
)
def test_invalid_deposit_amount_is_rejected(make_user, amount):
    alice = make_user()

    response = alice.balances.deposit("USDT", amount)

    assert response.status_code == 422
    assert ErrorResponse.model_validate(response.json()).error.code == "validation_error"


def test_order_cost_is_exact(funded_user):
    funded_user.orders.create_order("ETH-USDT", "BUY", price="0.1", quantity="3")

    usdt = funded_user.get_balance("USDT")
    assert usdt.locked == Decimal("0.3")
    assert usdt.available == Decimal("99.7")


@pytest.mark.xfail(reason="BUG: переполнение баланса даёт 500 вместо ошибки 4xx", strict=True)
def test_deposit_over_balance_limit_returns_client_error(make_user):
    alice = make_user()
    alice.balances.deposit("USDT", "999999999999999999")

    response = alice.balances.deposit("USDT", "999999999999999999")

    assert response.status_code in (400, 422)


@pytest.mark.xfail(reason="BUG: ордер дешевле 1e-18 USDT принимается бесплатно", strict=True)
def test_order_cheaper_than_precision_is_rejected(funded_user):
    # стоимость 0.000000001 × 0.0000000001 = 1e-19, меньше точности хранения
    response = funded_user.orders.create_order(
        "ETH-USDT", "BUY", price="0.000000001", quantity="0.0000000001"
    )

    assert response.status_code in (400, 422)
