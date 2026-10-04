import httpx

from framework.transport.client import ApiClient


class OrdersApi:
    def __init__(self, client: ApiClient):
        self._client = client

    def create_order(
        self,
        symbol: str,
        side: str,
        price: str,
        quantity: str,
        type: str = "LIMIT",
        auth: httpx.Auth | None = None,
    ) -> httpx.Response:
        body = {
            "symbol": symbol,
            "side": side,
            "type": type,
            "price": price,
            "quantity": quantity,
        }
        return self._client.post("/orders", json=body, auth=auth)

    def get_order(self, order_id: str, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.get(f"/orders/{order_id}", auth=auth)

    def get_orders(self, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.get("/orders", auth=auth)

    def cancel_order(self, order_id: str, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.delete(f"/orders/{order_id}", auth=auth)
