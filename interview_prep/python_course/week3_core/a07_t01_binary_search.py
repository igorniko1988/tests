"""A7 t01 (required, ~10 min). Binary search.

nums is sorted ascending with distinct values. Return the index of target or -1.

Requirements:
- O(log n). Tests make 100 000 searches in a list of 1 000 000.
- Write the search yourself: no bisect, no index(), no `in` on the list (the test checks the source).

Examples:
    binary_search([-1, 0, 3, 5, 9, 12], 9)  -> 4
    binary_search([-1, 0, 3, 5, 9, 12], 2)  -> -1
    binary_search([], 1)                    -> -1

Follow-up questions:
- Why lo <= hi and mid + 1 / mid - 1?

Run (from interview_prep/python_course/week3_core): uv run pytest -k a07_t01
Теория: THEORY.md в этой папке, раздел 1.
"""


def binary_search(nums: list[int], target: int) -> int:
    raise NotImplementedError
