"""A8 t08 (★ optional, ~20 min). Subarrays with sum divisible by k.

Return the number of non-empty contiguous subarrays whose sum is divisible by k (k > 0).
Numbers may be negative.

Examples:
    divisible_by_k([4, 5, 0, -2, -3, 1], 5)  -> 7
    divisible_by_k([5], 9)                   -> 0

Follow-up questions:
- Why compare prefix % k values?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t08
Теория: THEORY.md в этой папке, раздел 2.
"""


def divisible_by_k(nums: list[int], k: int) -> int:
    raise NotImplementedError
