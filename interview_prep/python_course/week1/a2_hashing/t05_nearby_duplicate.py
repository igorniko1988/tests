"""A2 t05 (required, ~15 min). Contains nearby duplicate.

Return True if there are two indices i != j with nums[i] == nums[j]
and abs(i - j) <= k.

Requirements:
- O(n) time. Tests use 100 000 numbers.

Examples:
    nearby_duplicate([1, 2, 3, 1], 3)        -> True
    nearby_duplicate([1, 0, 1, 1], 1)        -> True
    nearby_duplicate([1, 2, 3, 1, 2, 3], 2)  -> False
    nearby_duplicate([], 0)                  -> False

Follow-up questions:
- What do you store per value, and why only the LAST index?

Run (from interview_prep/python_course/week1/a2_hashing): uv run pytest -k t05
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def nearby_duplicate(nums: list[int], k: int) -> bool:
    raise NotImplementedError
