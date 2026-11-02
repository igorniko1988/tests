"""A4 t03 (required, ~20 min). Minimum size subarray sum.

nums contains POSITIVE integers. Return the minimal length of a contiguous subarray
whose sum is >= target, or 0 if there is none.

Requirements:
- O(n) time. Tests use 200 000 numbers.

Examples:
    min_subarray_len(7, [2, 3, 1, 2, 4, 3])  -> 2     # [4, 3]
    min_subarray_len(4, [1, 4, 4])           -> 1
    min_subarray_len(11, [1, 1, 1, 1])       -> 0

Follow-up questions:
- Why do you update the answer INSIDE the while loop here?
- Why would negative numbers break this approach?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 2.
"""


def min_subarray_len(target: int, nums: list[int]) -> int:
    raise NotImplementedError
