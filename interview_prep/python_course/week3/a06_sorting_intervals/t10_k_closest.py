"""A6 t10 (★ optional, ~15 min). K closest points to the origin.

Return the k points [x, y] closest to (0, 0), ordered by distance; ties keep the input order.

Examples:
    k_closest([[1, 3], [-2, 2]], 1)          -> [[-2, 2]]
    k_closest([[3, 3], [5, -1], [-2, 4]], 2) -> [[3, 3], [-2, 4]]

Follow-up questions:
- Why compare x*x + y*y without sqrt?
- heapq.nsmallest vs full sort: complexity?

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t10
Теория: THEORY.md в этой папке, раздел 1.
"""


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    raise NotImplementedError
