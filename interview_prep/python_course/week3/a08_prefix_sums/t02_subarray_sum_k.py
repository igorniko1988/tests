"""A8 t02 (required, ~25 min). Count subarrays with sum k.

Return the number of contiguous non-empty subarrays of nums whose sum equals k.
Numbers may be negative.

Requirements:
- O(n) time (prefix sums + dict). Tests use 100 000 numbers.

Examples:
    subarray_sum_k([1, 1, 1], 2)      -> 2
    subarray_sum_k([1, 2, 3], 3)      -> 2
    subarray_sum_k([1, -1, 0], 0)     -> 3
    subarray_sum_k([], 0)             -> 0

Follow-up questions:
- Why seen = {0: 1} at the start?
- Why doesn't a sliding window work here?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 2.
"""


def subarray_sum_k(nums: list[int], k: int) -> int:
    raise NotImplementedError
