"""A8 t04 (required, ~25 min). Longest subarray with equal 0s and 1s.

nums contains only 0 and 1. Return the length of the longest contiguous subarray with the
same number of 0s and 1s.

Requirements:
- O(n). Hint: count 0 as -1, then you need the longest subarray with sum 0;
  remember the FIRST index of every prefix sum.

Examples:
    contiguous_array([0, 1])           -> 2
    contiguous_array([0, 1, 0])        -> 2
    contiguous_array([0, 0, 1, 0, 0, 0, 1, 1])  -> 6
    contiguous_array([1, 1])           -> 0

Follow-up questions:
- Why the FIRST index, not the last?

Run (from interview_prep/python_course/week3/a08_prefix_sums): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 2.
"""


def contiguous_array(nums: list[int]) -> int:
    raise NotImplementedError
