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
        idempotency_key: str | None = None,
        expires_in_seconds: int | None = None,
        auth: httpx.Auth | None = None,
    ) -> httpx.Response:
        body = {
            "symbol": symbol,
            "side": side,
            "type": type,
            "price": price,
            "quantity": quantity,
        }
        if expires_in_seconds:
            body["expires_in_seconds"] = expires_in_seconds
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else {}
        return self._client.post("/orders", json=body, headers=headers, auth=auth)

    def get_order(self, order_id: str, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.get(f"/orders/{order_id}", auth=auth)

    def get_orders(
        self, limit: int | None = None, cursor: str | None = None, auth: httpx.Auth | None = None
    ) -> httpx.Response:
        params = {}
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor
        return self._client.get("/orders", params=params, auth=auth)

    def cancel_order(self, order_id: str, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.delete(f"/orders/{order_id}", auth=auth)
