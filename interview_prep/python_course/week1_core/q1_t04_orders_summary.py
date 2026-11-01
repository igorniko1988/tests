"""Q1 t04 (required, ~20 min). Orders summary by status.

Given orders {"id": int, "status": str, "amount": str} (amounts are strings
from an API), return a summary per status:

    {status: {"count": int, "total": str}}

Requirements:
- total is the sum of amounts as Decimal, rounded to 2 places (ROUND_HALF_UP),
  returned as a string with exactly two decimals: "10.50".
- Statuses in order of first appearance. Do not use float.

Example:
    orders_summary([
        {"id": 1, "status": "NEW", "amount": "10.10"},
        {"id": 2, "status": "FILLED", "amount": "5"},
        {"id": 3, "status": "NEW", "amount": "0.2"},
    ]) -> {"NEW": {"count": 2, "total": "10.30"}, "FILLED": {"count": 1, "total": "5.00"}}

    orders_summary([]) -> {}

Follow-up questions:
- What would float give for "0.1" + "0.2"?
- Why quantize only at the end, not on every addition?

Run (from interview_prep/python_course/week1_core): uv run pytest -k q1_t04
Теория: interview_prep/python_course/c02_numbers_strings/s03_decimal/THEORY.md.
"""


def orders_summary(orders: list[dict]) -> dict[str, dict]:
    raise NotImplementedError
