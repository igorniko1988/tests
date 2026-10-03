import httpx

from framework.http.client import ApiClient


class BalancesApi:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.get("/balances", auth=auth)

    def deposit(self, asset: str, amount: str, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.post(
            "/balances/deposit", json={"asset": asset, "amount": amount}, auth=auth
        )
