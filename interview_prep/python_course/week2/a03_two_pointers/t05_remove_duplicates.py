"""A3 t05 (required, ~15 min). Remove duplicates from a sorted list in place.

nums is sorted. Remove duplicates IN PLACE so that the first k elements are the unique
values in order; return k. What stays after the first k elements does not matter.

Requirements:
- Do not create a new list; O(1) extra memory (read / write pointers).

Examples:
    nums = [1, 1, 2, 2, 3]
    remove_duplicates(nums)  -> 3, nums[:3] == [1, 2, 3]

    [] -> 0        [5] -> 1        [0, 0, 0] -> 1

Follow-up questions:
- What is always true about nums[:write] during the loop?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 2.
"""


def remove_duplicates(nums: list[int]) -> int:
    raise NotImplementedError
