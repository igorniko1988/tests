"""C7 t05 (required, ~20 min). Read-only Money.

Implement a class Money(amount, currency):

- amount accepts str, int or Decimal (float -> TypeError: money is never float);
  stored as Decimal rounded to 2 places (ROUND_HALF_UP);
- currency: 3 letters, stored upper case; otherwise ValueError;
- amount and currency are READ-ONLY properties (assignment -> AttributeError);
- add(other) returns a NEW Money with the sum; different currencies -> ValueError;
- formatted property: "<amount> <currency>", e.g. "10.50 USD".

Example:
    m = Money("10.5", "usd")
    m.amount, m.currency, m.formatted     -> Decimal("10.50"), "USD", "10.50 USD"
    m.add(Money(2, "USD")).formatted      -> "12.50 USD"
    m.amount = 1                          -> AttributeError

Follow-up questions:
- Why reject float instead of converting it?
- Why does add return a new object instead of changing self?

Run (from interview_prep/python_course/week3/c07_classes): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 3.
"""


from decimal import ROUND_HALF_UP, Decimal  # noqa: F401


class Money:
    def __init__(self, amount, currency: str) -> None:
        raise NotImplementedError
