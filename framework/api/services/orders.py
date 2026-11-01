from uuid import uuid4

from requests import Response

from framework.api.client import ApiClient
from framework.api.models.order import CreateOrder


class OrderService:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def create(self, order: CreateOrder, exclude: set[str] | None = None) -> Response:
        # Idempotency-Key: повтор запроса после сбоя не создаст второй ордер (см. ORDERS_RETRY)
        return self.client.post(
            "/orders",
            json=order.model_dump(exclude=exclude),
            headers={"Idempotency-Key": str(uuid4())},
        )

    def list(self, status: str | None = None) -> Response:
        return self.client.get("/orders", params={"status": status})

    def get(self, order_id) -> Response:
        return self.client.get(f"/orders/{order_id}")

    def cancel(self, order_id) -> Response:
        return self.client.delete(f"/orders/{order_id}")
