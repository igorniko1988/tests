"""Q3 t04 (required, ~25 min). Money: a value object with operators.

Implement an immutable Money(amount, currency):
- amount: str / int / Decimal (float -> TypeError), stored as Decimal with 2 places (ROUND_HALF_UP);
- currency: 3 letters, stored upper case (else ValueError);
- immutable: assigning any attribute -> AttributeError (frozen dataclass or properties);
- a + b, a - b -> new Money; different currencies -> ValueError ("currency mismatch");
- money * number (int or Decimal) and number * money -> new Money, rounded to 2 places;
- ==, hash: equal amount AND currency; Money("1", "USD") != Money("1", "EUR");
- <, <=, >, >= only for the same currency (else ValueError);
- str(m) -> "10.50 USD"; repr(m) -> "Money('10.50', 'USD')";
- Money.zero("usd") -> classmethod for 0.00 in that currency;
- sum([...], Money.zero("USD")) works.

Follow-up questions:
- Why must Money be immutable and hashable?
- Why raise on 5 USD < 3 EUR instead of returning False?

Run (from interview_prep/python_course/week3/q3_class_design): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 5.
"""


from decimal import ROUND_HALF_UP, Decimal  # noqa: F401


class Money:
    def __init__(self, amount, currency: str) -> None:
        raise NotImplementedError
