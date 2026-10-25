import uuid

from framework.models.balance import Balance
from framework.models.order import Order


def test_create_order(auth_api):
    auth_api.balances.deposit('USDT',100)
    order = auth_api.orders.create('ETH-USDT','BUY',"LIMIT",1,1)

    assert order.status_code == 201
    Order.model_validate(order.json())


def test_get_orders(auth_api):
    auth_api.balances.deposit('USDT', 100)
    create = auth_api.orders.create('ETH-USDT','BUY','LIMIT','1','1')
    assert create.status_code == 201

    created = Order.model_validate(create.json())

    response = auth_api.orders.list('NEW')
    assert response.status_code == 200
    orders = [Order.model_validate(o) for o in response.json()]

    assert created.id in [o.id for o in orders]
    assert all([o.status == 'NEW' for o in orders])

def test_order_by_id(auth_api):
    auth_api.balances.deposit('USDT', 200)
    create = auth_api.orders.create('ETH-USDT','BUY','LIMIT','1','1')
    assert create.status_code == 201

    created = Order.model_validate(create.json())

    order_response = auth_api.orders.get(created.id)
    assert order_response.status_code == 200
    order = Order.model_validate(order_response.json())

    assert order.id == created.id


def test_get_order_not_found(auth_api):
    response = auth_api.orders.get(uuid.uuid4())

    assert response.status_code == 404
    assert response.json()['error']['code'] == 'order_not_found'


def test_cancel_orders(auth_api):
    auth_api.balances.deposit('USDT', 200)
    create = auth_api.orders.create('ETH-USDT','BUY','LIMIT','1','1')
    assert create.status_code == 201

    created = Order.model_validate(create.json())

    canceled = auth_api.orders.cancel(created.id)

    assert canceled.status_code == 200

    assert Order.model_validate(canceled.json()).status == 'CANCELED'

    balances = auth_api.balances.get_balance()

    usdt = next(Balance.model_validate(b) for b in balances.json() if b['asset'] == 'USDT')
    assert usdt.available == '200'
    assert usdt.locked == '0'
    assert auth_api.orders.cancel(created.id).status_code == 409