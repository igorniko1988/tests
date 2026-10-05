from framework2.client import ApiClient


class OrdersApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def create(self, symbol: str, side: str, price: str, quantity: str):
        body = {"symbol": symbol, "side": side, "price": price, "quantity": quantity}
        return self.client.post("/orders", json=body)

    def get(self, order_id):
        return self.client.get(f"/orders/{order_id}")

    def get_all(self):
        return self.client.get("/orders")

    def cancel(self, order_id):
        return self.client.delete(f"/orders/{order_id}")
