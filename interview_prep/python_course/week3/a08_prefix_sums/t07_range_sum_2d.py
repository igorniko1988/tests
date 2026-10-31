"""A8 t07 (★ optional, ~25 min). Range sum query 2D.

Implement RangeSum2D(matrix) with query(r1, c1, r2, c2) -> sum of the rectangle with corners
(r1, c1) and (r2, c2) inclusive, in O(1) after O(rows * cols) precomputation.

Example:
    m = RangeSum2D([[3, 0, 1], [5, 6, 3], [1, 2, 0]])
    m.query(1, 1, 2, 2)  -> 11
    m.query(0, 0, 0, 0)  -> 3

Follow-up questions:
- Draw the inclusion-exclusion formula.

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t07
Теория: THEORY.md в этой папке, раздел 1.
"""


class RangeSum2D:
    def __init__(self, matrix: list[list[int]]) -> None:
        raise NotImplementedError

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        raise NotImplementedError
