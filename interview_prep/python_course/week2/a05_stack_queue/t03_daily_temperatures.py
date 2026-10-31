"""A5 t03 (required, ~25 min). Daily temperatures.

temps[i] is the temperature on day i. Return a list answer where answer[i] is the number
of days to wait after day i for a warmer temperature, or 0 if there is no such day.

Requirements:
- O(n) time with a monotonic stack. Tests use 200 000 days.

Examples:
    daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])  -> [1, 1, 4, 2, 1, 1, 0, 0]
    daily_temperatures([30, 40, 50, 60])                  -> [1, 1, 1, 0]
    daily_temperatures([30, 30])                          -> [0, 0]

Follow-up questions:
- What does the stack hold and in what order?
- Why is the total work O(n) despite the inner while?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 3.
"""


def daily_temperatures(temps: list[int]) -> list[int]:
    raise NotImplementedError
