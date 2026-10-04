import uuid

import pytest

from framework.models.error import ErrorResponse
from framework.models.order import Order


def get_error(response):
    return ErrorResponse.model_validate(response.json()).error


def test_order_without_funds(orders_api, bearer_token):
    response = orders_api.create_order(
        "ETH-USDT", "BUY", price="2", quantity="3", auth=bearer_token
    )

    assert response.status_code == 400
    assert get_error(response).code == "insufficient_funds"


def test_get_unknown_order(orders_api, bearer_token):
    response = orders_api.get_order(uuid.uuid4(), auth=bearer_token)

    assert response.status_code == 404
    assert get_error(response).code == "order_not_found"


def test_cancel_order_twice(balance_api, orders_api, bearer_token):
    balance_api.deposit("USDT", "10", auth=bearer_token)
    created = orders_api.create_order("ETH-USDT", "BUY", price="2", quantity="3", auth=bearer_token)
    order = Order.model_validate(created.json())
    orders_api.cancel_order(order.id, auth=bearer_token)

    response = orders_api.cancel_order(order.id, auth=bearer_token)

    assert response.status_code == 409
    assert get_error(response).code == "order_not_open"


@pytest.mark.parametrize(
    ("symbol", "price", "bad_field"),
    [
        ("DOGE-USDT", "2", "symbol"),
        ("ETH-USDT", "-1", "price"),
        ("ETH-USDT", "0", "price"),
    ],
)
def test_create_order_invalid_data(orders_api, bearer_token, symbol, price, bad_field):
    response = orders_api.create_order(symbol, "BUY", price=price, quantity="1", auth=bearer_token)

    assert response.status_code == 422
    error = get_error(response)
    assert error.code == "validation_error"
    assert bad_field in [d.field for d in error.details]
