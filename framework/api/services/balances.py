from requests import Response

from framework.api.client import ApiClient


class BalanceService:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_balance(self) -> Response:
        return self.client.get("/balances")

    def deposit(self, asset: str, amount: str | int) -> Response:
        return self.client.post("/balances/deposit", json={"asset": asset, "amount": str(amount)})
