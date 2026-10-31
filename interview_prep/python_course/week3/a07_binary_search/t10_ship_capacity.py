"""A7 t10 (★ optional, ~25 min). Capacity to ship packages within D days.

weights are packages in a fixed order; every day the ship loads packages in order while the
total stays <= capacity. Return the minimum capacity to ship everything within days days.

Examples:
    ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)  -> 15
    ship_capacity([3, 2, 2, 4, 1, 4], 3)               -> 6
    ship_capacity([1, 2, 3, 1, 1], 4)                  -> 3

Follow-up questions:
- Why is lo = max(weights) and hi = sum(weights)?

Run (from interview_prep/python_course/week3/a07_binary_search): uv run pytest -k t10
Теория: THEORY.md в этой папке, раздел 3.
"""


def ship_capacity(weights: list[int], days: int) -> int:
    raise NotImplementedError
