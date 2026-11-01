"""A3 t02 (required, ~15 min). Two sum II: sorted input.

nums is sorted in ascending order. Return the indices [i, j] (i < j) of two numbers
that add up to target, or [] if there are none. If several pairs exist, return the one
found by the classic two-pointer scan (left from 0, right from the end).

Requirements:
- O(n) time, O(1) memory. Tests use 200 000 numbers.

Examples:
    two_sum_sorted([2, 7, 11, 15], 9)   -> [0, 1]
    two_sum_sorted([1, 3, 4, 6, 9], 7)  -> [0, 3]
    two_sum_sorted([1, 2], 10)          -> []

Follow-up questions:
- Why can you drop nums[right] when the sum is too big?
- Two sum with a dict (A2 t01) vs two pointers: when each?

Run (from interview_prep/python_course/week2_core): uv run pytest -k a03_t02
Теория: THEORY.md в этой папке, раздел 1.
"""


def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    raise NotImplementedError
