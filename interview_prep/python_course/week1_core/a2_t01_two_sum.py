"""A2 t01 (required, ~15 min). Two sum.

Given a list of integers nums and an integer target, return the indices
[i, j] (i < j) of the two numbers that add up to target.

Requirements:
- Exactly one answer exists; you may not use the same element twice.
- O(n) time. Tests use 100 000 numbers.

Examples:
    two_sum([2, 7, 11, 15], 9)   -> [0, 1]
    two_sum([3, 2, 4], 6)        -> [1, 2]
    two_sum([3, 3], 6)           -> [0, 1]

Follow-up questions:
- What do you store in the dict: key -> value? Why not a set?
- Why check `target - x in seen` BEFORE adding x?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a2_t01
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    raise NotImplementedError
