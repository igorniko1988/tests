"""A1 t05 (required, ~20 min). Product of array except self.

Given a list nums, return a list answer where answer[i] is the product of all
elements of nums except nums[i].

Requirements:
- Do NOT use division (the test checks the source for "/").
- O(n) time. Tests use 100 000 items.
- nums may contain zeros.

Examples:
    product_except_self([1, 2, 3, 4])   -> [24, 12, 8, 6]
    product_except_self([2, 0, 3])      -> [0, 6, 0]
    product_except_self([0, 0, 5])      -> [0, 0, 0]
    product_except_self([7])            -> [1]

Follow-up questions:
- Why does "total product / nums[i]" break on zeros?
- What are "prefix" and "suffix" products here?

Run (from interview_prep/python_course/week1/a1_arrays_strings): uv run pytest -k t05
Теория: interview_prep/python_course/a00_big_o/s07_method/THEORY.md (метод решения).
"""


def product_except_self(nums: list[int]) -> list[int]:
    raise NotImplementedError
