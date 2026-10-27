import json
from websockets.sync.client import connect
import resp

from framework.models.order import CreateOrder


def test_new_order_appears_in_orderbook(auth_api):
    with connect('ws://localhost:8080/ws/orderbook/ETH-USDT', open_timeout=5) as ws:
        snapshot = json.loads(ws.recv(timeout=5))
        print(snapshot)
        print(snapshot['type'])
        assert snapshot['type'] == 'snapshot'

        auth_api.balances.deposit('USDT', '100')
        auth_api.orders.create(CreateOrder(price='7.77'))

        update = json.loads(ws.recv(timeout=5))
        print(update)
        print(update['type'])
        assert update['type'] == 'update'
        assert ['7.77', '1'] in update['bids']