"""C9 t04 (required, ~20 min). Order as a dataclass with validation.

Write a dataclass Order with fields, in this order:
    symbol: str
    side: str
    qty: int = 1
    price: Decimal = Decimal("0")
    tags: list[str] = empty list, NOT shared between orders

__post_init__ must:
- normalize side to upper case and check it is "BUY" or "SELL" (else ValueError);
- check qty > 0 (else ValueError);
- convert price to Decimal if it came as str or int; float -> TypeError.

Also add a method to_payload() -> dict for a request body:
    {"symbol": ..., "side": ..., "qty": ..., "price": "<price as string>", "tags": [...]}
(use dataclasses.asdict, then make price a string).

Example:
    o = Order("BTC", "buy", qty=2, price="10.50")
    o.side, o.price   -> "BUY", Decimal("10.50")
    Order("ETH", "sell") == Order("ETH", "SELL")   -> True
    Order("BTC", "BUY").tags is not Order("BTC", "BUY").tags   -> True

Follow-up questions:
- Why field(default_factory=list) and not tags: list = []?
- dataclass vs pydantic for validating API responses?

Run (from interview_prep/python_course/week3/c09_magic_methods): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 8.
"""


from dataclasses import asdict, dataclass, field  # noqa: F401
from decimal import Decimal  # noqa: F401


class Order:
    pass
