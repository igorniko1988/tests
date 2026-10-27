from framework.contract import assert_matches_schema
from framework.models.order import Order, CreateOrder

def test_create_order_matches_openapi(auth_api):
    auth_api.balances.deposit('USDT','100')

    response = auth_api.orders.create(CreateOrder())

    assert response.status_code == 201
    assert_matches_schema(response.json(),'OrderOut')