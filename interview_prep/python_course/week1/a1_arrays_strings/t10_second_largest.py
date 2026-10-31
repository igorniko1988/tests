"""A1 t10 (★ optional, ~10 min). Second largest distinct value.

Return the second largest DISTINCT value of nums, or None if it does not exist.

Requirements:
- One pass, O(n) time, O(1) memory. Do not sort.

Examples:
    second_largest([3, 1, 4, 4, 2])  -> 3
    second_largest([5, 5])           -> None
    second_largest([-1, -2])         -> -2
    second_largest([])               -> None

Follow-up questions:
- Why is sorted(set(nums))[-2] fine but not what was asked?

Run (from interview_prep/python_course/week1/a1_arrays_strings): uv run pytest -k t10
"""


def second_largest(nums: list[int]) -> int | None:
    raise NotImplementedError
