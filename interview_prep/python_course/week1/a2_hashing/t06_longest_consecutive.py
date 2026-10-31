"""A2 t06 (required, ~20 min). Longest consecutive sequence.

Given an unsorted list of integers, return the length of the longest run of
consecutive values (x, x + 1, x + 2, ...). Values may repeat.

Requirements:
- O(n) time. Do NOT sort (the test checks the source).

Examples:
    longest_consecutive([100, 4, 200, 1, 3, 2])   -> 4    # 1, 2, 3, 4
    longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])  -> 9
    longest_consecutive([1, 2, 2, 3])             -> 3
    longest_consecutive([])                       -> 0

Follow-up questions:
- Why start counting only from x where x - 1 is NOT in the set?
- Why is the whole algorithm O(n) even with a while loop inside the for?

Run (from interview_prep/python_course/week1/a2_hashing): uv run pytest -k t06
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def longest_consecutive(nums: list[int]) -> int:
    raise NotImplementedError
