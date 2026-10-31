"""A1 t07 (★ optional, ~20 min). Rotate a list to the right, in place.

Given a list nums and an integer k >= 0, rotate the list to the right by k steps.

Requirements:
- Modify nums IN PLACE and return None.
- k may be larger than len(nums).

Examples:
    nums = [1, 2, 3, 4, 5]
    rotate(nums, 2)
    nums   -> [4, 5, 1, 2, 3]

    [1, 2] with k=3  -> [2, 1]
    [] with k=5      -> []

Follow-up questions:
- Why k % len(nums)?
- How to do it with O(1) extra memory? (Hint: three reversals.)

Run (from interview_prep/python_course/week1/a1_arrays_strings): uv run pytest -k t07
"""


def rotate(nums: list[int], k: int) -> None:
    raise NotImplementedError
