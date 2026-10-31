"""A2 t07 (★ optional, ~25 min). Count subarrays with sum k.

Return the number of contiguous non-empty subarrays of nums whose sum equals k.
Numbers may be negative.

Requirements:
- O(n) time. Tests use 20 000 numbers.

Examples:
    subarray_sum([1, 1, 1], 2)      -> 2
    subarray_sum([1, 2, 3], 3)      -> 2     # [1, 2] and [3]
    subarray_sum([1, -1, 0], 0)     -> 3
    subarray_sum([], 0)             -> 0

Follow-up questions:
- What is a prefix sum, and why does "prefix - k seen before" mean a subarray?
- Why does a sliding window not work with negative numbers?

Run (from interview_prep/python_course/week1/a2_hashing): uv run pytest -k t07
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def subarray_sum(nums: list[int], k: int) -> int:
    raise NotImplementedError
