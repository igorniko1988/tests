"""A8 t03 (required, ~15 min). Pivot index.

Return the leftmost index i where the sum of elements strictly to the left equals the sum of
elements strictly to the right; -1 if there is none. Sums of empty sides are 0.

Requirements:
- O(n) time, O(1) extra memory.

Examples:
    pivot_index([1, 7, 3, 6, 5, 6])  -> 3
    pivot_index([1, 2, 3])           -> -1
    pivot_index([2, 1, -1])          -> 0
    pivot_index([])                  -> -1

Follow-up questions:
- How do you get the right sum from the total and the left sum?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 1.
"""


def pivot_index(nums: list[int]) -> int:
    raise NotImplementedError
