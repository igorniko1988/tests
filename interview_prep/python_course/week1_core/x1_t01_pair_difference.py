"""X1 t01 (algorithm, part of 40 min). Pair with a given difference.

Given a list of integers nums and an integer k >= 0, return True if there are
two DIFFERENT indices i and j such that nums[i] - nums[j] == k.

Requirements:
- O(n) time. Tests use 100 000 numbers.
- For k == 0 you need a value that appears at least twice.

Examples:
    pair_difference([5, 20, 3, 2, 50, 80], 78)  -> True    # 80 - 2
    pair_difference([90, 70, 20, 80, 50], 45)   -> False
    pair_difference([1, 2, 1], 0)               -> True    # 1 - 1, indices 0 and 2
    pair_difference([1, 2, 3], 0)               -> False
    pair_difference([], 1)                      -> False

Follow-up questions:
- What is the brute-force complexity and what do you store to speed it up?
- Why does k == 0 need special care?

Run (from interview_prep/python_course/week1_core): uv run pytest -k x1_t01
"""


def pair_difference(nums: list[int], k: int) -> bool:
    raise NotImplementedError
