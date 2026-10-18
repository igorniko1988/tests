from ui_framework.data.models import OrderData


def test_api(create_api):
    api, email = create_api()

    response = api.deposit('USDT', '100')
    assert response.status == 200

    response = api.place_order(OrderData(price='10', quantity='1'))
    assert response.status == 201
    print(response.json())
