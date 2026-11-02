"""A4 t10 (★ optional, ~20 min). Subarrays with product less than k.

nums contains positive integers. Return the number of contiguous subarrays whose
product is strictly less than k.

Examples:
    product_less_k([10, 5, 2, 6], 100)  -> 8
    product_less_k([1, 2, 3], 0)        -> 0
    product_less_k([1, 1, 1], 2)        -> 6

Follow-up questions:
- Why does each right end add (right - left + 1) subarrays?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t10
Теория: THEORY.md в этой папке, раздел 2.
"""


def product_less_k(nums: list[int], k: int) -> int:
    raise NotImplementedError
