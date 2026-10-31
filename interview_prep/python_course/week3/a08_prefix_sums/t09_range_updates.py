"""A8 t09 (★ optional, ~20 min). Apply many range updates (difference array).

Start with n zeros. Each update (l, r, delta) adds delta to every index from l to r inclusive.
Return the final list.

Requirements:
- O(n + number of updates). Tests use n = 100 000 and 100 000 wide updates.

Example:
    range_updates(5, [(1, 3, 2), (2, 4, 3), (0, 2, -2)])  -> [-2, 0, 3, 5, 3]

Follow-up questions:
- Why diff[r + 1] -= delta?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t09
Теория: THEORY.md в этой папке, раздел 3.
"""


def range_updates(n: int, updates: list[tuple[int, int, int]]) -> list[int]:
    raise NotImplementedError
