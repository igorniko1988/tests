"""A8 t06 (required, ~20 min). Maximum subarray sum.

Return the largest sum of a contiguous NON-EMPTY subarray.

Requirements:
- O(n), O(1) memory (Kadane: "current best ending here" or
  "prefix minus the smallest earlier prefix").

Examples:
    max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])  -> 6     # [4, -1, 2, 1]
    max_subarray([-3, -1, -2])                     -> -1
    max_subarray([5])                              -> 5

Follow-up questions:
- How is Kadane's algorithm related to prefix sums?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 4.
"""


def max_subarray(nums: list[int]) -> int:
    raise NotImplementedError
