"""A1 t02 (required, ~15 min). Move zeroes to the end, in place.

Given a list nums, move all 0s to the end while keeping the relative order
of the non-zero elements.

Requirements:
- Modify nums IN PLACE and return None (like list.sort()).
- O(n) time, O(1) extra memory. Tests use 100 000 items.

Examples:
    nums = [0, 1, 0, 3, 12]
    move_zeros(nums)   -> None
    nums               -> [1, 3, 12, 0, 0]

    [0] -> [0]         [1, 2] -> [1, 2]         [] -> []

Follow-up questions:
- Why is `nums.remove(0); nums.append(0)` in a loop O(n^2)?
- Explain your two-pointer idea: what does each index point to?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a1_t02
Теория: interview_prep/python_course/c03_collections/s01_list/THEORY.md (изменение на месте).
"""


def move_zeros(nums: list[int]) -> None:
    raise NotImplementedError
