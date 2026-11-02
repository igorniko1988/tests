"""A6 t05 (required, ~20 min). Largest number from numbers.

Given non-negative integers, arrange them to form the largest number; return it as a string.

Examples:
    largest_number([10, 2])            -> "210"
    largest_number([3, 30, 34, 5, 9])  -> "9534330"
    largest_number([0, 0])             -> "0"
    largest_number([1])                -> "1"

Follow-up questions:
- Why is plain reverse string sorting wrong for [3, 30]?
- What does functools.cmp_to_key do?

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 5.
"""


def largest_number(nums: list[int]) -> str:
    raise NotImplementedError
