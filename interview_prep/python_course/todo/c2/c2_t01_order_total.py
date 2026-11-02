"""C2 t01 (required, ~15 min). Order total with fee, in Decimal.

A balance test must compute the EXPECTED amount itself. Implement
order_total(lines, fee_percent="0") -> str.

Input:
- lines: list of (price, quantity) pairs; price is a STRING as it comes from the API
  ("19.99"), quantity is an int.
- fee_percent: a string, "0.1" means 0.1 %.

Requirements:
- total = sum(price * quantity) + fee_percent % of that sum.
- Round to 2 decimal places, half up (ROUND_HALF_UP).
- Return a string with exactly two decimals: "59.97", "0.30", "0.00".
- Do not use float anywhere.

Examples:
    order_total([("19.99", 3)])          -> "59.97"
    order_total([("19.99", 3)], "0.1")   -> "60.03"   # 59.97 + 0.1 % = 60.02997
    order_total([("0.1", 3)])            -> "0.30"
    order_total([("0.125", 1)])          -> "0.13"    # half up, not banker's rounding
    order_total([])                      -> "0.00"

Follow-up questions:
- What changes if you write Decimal(19.99) instead of Decimal("19.99")?
- Why is float a bad choice for money?

Run (from interview_prep/python_course/todo): uv run pytest -k c2_t01
Теория: interview_prep/python_course/c02_numbers_strings/s03_decimal/THEORY.md, раздел 3.
"""

from decimal import Decimal

from decimal import Decimal

def order_total(lines: list[tuple[str, int]], fee_percent: str = "0") -> str:
    price, quantity = lines[0][0], lines[0][1]

    if not Decimal(fee_percent):
        return Decimal(price) * Decimal(quantity)
    return Decimal(price) * Decimal(quantity) + Decimal(fee_percent)

print(order_total([("19.99", 3)], "0.1"))