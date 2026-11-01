"""A1 t04 (required, ~15 min). Best time to buy and sell a stock.

prices[i] is the price of a stock on day i. Choose one day to buy and a LATER
day to sell. Return the maximum profit; if no profit is possible, return 0.

Requirements:
- O(n) time, O(1) memory. Tests use 200 000 prices.

Examples:
    max_profit([7, 1, 5, 3, 6, 4])   -> 5    # buy at 1, sell at 6
    max_profit([7, 6, 4, 3, 1])      -> 0    # prices only fall
    max_profit([])                   -> 0
    max_profit([5])                  -> 0

Follow-up questions:
- Why is max(prices) - min(prices) wrong? Give an example.
- What do you keep in variables while scanning, and why is that enough?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a1_t04
Теория: interview_prep/python_course/a00_big_o/s07_method/THEORY.md (метод решения).
"""


def max_profit(prices: list[int]) -> int:
    raise NotImplementedError
