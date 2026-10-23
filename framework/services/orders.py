from framework.transport.api_client import ApiClient

class OrderService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create(self, symbol, side, type, price, quantity):
        data = {
            'symbol': symbol,
            'side': side,
            'type': type,
            'price': price,
            'quantity': quantity
        }
        return self.api_client.post('/orders', json=data)

    def orders(self):
        pass

    def get_order_by_id(self):
        pass

    def delete_order_by_id(self):
        pass