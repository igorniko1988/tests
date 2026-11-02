"""C7 t02 (required, ~20 min). Alternative constructor from an API response.

Implement a class Order(order_id, symbol, side, qty, price) with a classmethod
Order.from_json(data) that builds an order from an API dict where every value is a string:

    {"id": "17", "symbol": "BTC/USDT", "side": "buy", "qty": "2", "price": "10.50"}

- order_id: int, qty: int, price: Decimal (never float), symbol as is,
  side normalized to upper case and must be "BUY" or "SELL" (else ValueError).
- A missing key -> KeyError (do not hide it).
- from_json must create an object of the class it was called on: for
  class LimitOrder(Order), LimitOrder.from_json(...) returns a LimitOrder.
- total property: qty * price (Decimal).

Example:
    o = Order.from_json({"id": "17", "symbol": "BTC/USDT", "side": "buy", "qty": "2", "price": "10.50"})
    o.order_id, o.side, o.price, o.total   -> 17, "BUY", Decimal("10.50"), Decimal("21.00")

Follow-up questions:
- Why cls(...) and not Order(...) inside from_json?
- Why is a model object better than passing the raw dict around in tests?

Run (from interview_prep/python_course/week3_core): uv run pytest -k c07_t02
Теория: THEORY.md в этой папке, раздел 4.
"""


from decimal import Decimal  # noqa: F401


class Order:
    def __init__(self, order_id: int, symbol: str, side: str, qty: int, price) -> None:
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: dict):
        raise NotImplementedError
