from framework.transport.api_client import ApiClient
from uuid import uuid4
from framework.models.order import CreateOrder, Order


class OrderService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create(self, order: CreateOrder, exclude=None):
        return self.api_client.post('/orders', json=order.model_dump(exclude=exclude), headers={'Idempotency-Key': str(uuid4())})

    def list(self, status = None):
        return self.api_client.get('/orders', params={'status': status})

    def get(self, order_id):
        return self.api_client.get(f'/orders/{order_id}')

    def cancel(self, order_id):
        return self.api_client.delete(f'/orders/{order_id}')