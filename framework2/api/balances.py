from framework2.client import ApiClient


class BalancesApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_all(self):
        return self.client.get("/balances")

    def deposit(self, asset: str, amount: str):
        return self.client.post("/balances/deposit", json={"asset": asset, "amount": amount})
