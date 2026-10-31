"""A4 t01 (required, ~10 min). Maximum sum of k consecutive elements.

Return the maximum sum of k consecutive elements of nums.
If len(nums) < k or k <= 0, return None.

Requirements:
- O(n) time: do not call sum() on every window. Tests use 200 000 numbers, k = 1000.

Examples:
    max_sum_k([2, 1, 5, 1, 3, 2], 3)  -> 9      # [5, 1, 3]
    max_sum_k([-1, -2, -3], 2)        -> -3
    max_sum_k([1, 2], 3)              -> None

Follow-up questions:
- What is the complexity of sum(nums[i:i + k]) in a loop?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t01
Теория: THEORY.md в этой папке, раздел 1.
"""


def max_sum_k(nums: list[int], k: int) -> int | None:
    raise NotImplementedError
