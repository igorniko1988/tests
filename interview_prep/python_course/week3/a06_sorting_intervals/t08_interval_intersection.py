"""A6 t08 (★ optional, ~20 min). Interval list intersections.

a and b are lists of closed intervals, each list sorted and non-overlapping.
Return their intersection (also sorted). A single point [x, x] counts.

Examples:
    interval_intersection([[0, 2], [5, 10]], [[1, 5], [8, 12]])
        -> [[1, 2], [5, 5], [8, 10]]
    interval_intersection([], [[1, 2]])  -> []

Follow-up questions:
- Which pointer moves, and why?

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t08
Теория: THEORY.md в этой папке, раздел 2.
"""


def interval_intersection(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError
