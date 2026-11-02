"""X2 t03 (algorithm, part of 40 min). Max consecutive ones with k flips.

nums contains only 0 and 1. You may flip at most k zeros to ones. Return the length
of the longest run of consecutive ones you can get.

Requirements:
- O(n) time. Tests use 200 000 numbers.

Examples:
    longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2)  -> 6
    longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3)  -> 10
    longest_ones([0, 0], 0)                             -> 0
    longest_ones([], 1)                                 -> 0

Follow-up questions:
- Which pattern is it and what makes the window "bad"?

Run (from interview_prep/python_course/week2/x2_exam): uv run pytest -k t03
"""


def longest_ones(nums: list[int], k: int) -> int:
    raise NotImplementedError
