"""A4 t07 (★ optional, ~30 min). Sliding window maximum.

Return a list with the maximum of every window of size k (len(nums) - k + 1 values).

Requirements:
- O(n) time with a monotonic deque of indices. Tests use 200 000 numbers, k = 10 000.

Examples:
    window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)  -> [3, 3, 5, 5, 6, 7]
    window_max([4], 1)                         -> [4]

Follow-up questions:
- Why can you drop smaller elements from the right of the deque forever?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t07
Теория: THEORY.md в этой папке, раздел 3.
"""


def window_max(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError
