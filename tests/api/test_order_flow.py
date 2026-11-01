from framework.api.models.order import CreateOrder


def test_deposit_and_place_order(auth_api):
    response = auth_api.balances.deposit("USDT", "100")
    assert response.status_code == 200

    response = auth_api.orders.create(CreateOrder(price="10", quantity="1"))
    assert response.status_code == 201
