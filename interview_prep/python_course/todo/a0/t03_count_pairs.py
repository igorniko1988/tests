"""A0 t03 (required, ~15 min). Count pairs with target sum - optimize O(n^2) to O(n).

Given a list of integers nums and an integer target, return the number of index
pairs i < j such that nums[i] + nums[j] == target.
Numbers may repeat and may be negative. Do not modify the input.

Examples:
    count_pairs([1, 2, 3, 4], 5)   -> 2    # (1, 4) and (2, 3)
    count_pairs([3, 3, 3], 6)      -> 3    # index pairs (0,1), (0,2), (1,2)
    count_pairs([1, 1], 3)         -> 0
    count_pairs([], 0)             -> 0
    count_pairs([-1, 1, 0, 0], 0)  -> 2

The code below is a working brute-force solution over all pairs, O(n^2).
Rewrite it in O(n) time.

Follow-up questions:
- Why does [3, 3, 3] give 3, not 6 or 9?
- Time and memory complexity before and after?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_a0.py -k t03
Теория: interview_prep/python_course/a00_big_o/s07_method/THEORY.md (пример two sum).
"""


def count_pairs(nums: list[int], target: int) -> int:
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                count += 1
    return count
