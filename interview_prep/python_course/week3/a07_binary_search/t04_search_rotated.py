"""A7 t04 (required, ~25 min). Search in a rotated sorted array.

nums was sorted ascending with distinct values and then rotated at an unknown pivot,
e.g. [0, 1, 2, 4, 5, 6, 7] -> [4, 5, 6, 7, 0, 1, 2]. Return the index of target or -1.

Requirements:
- O(log n).
- Write the search yourself: no bisect, no index(), no `in` on the list (the test checks the source).

Examples:
    search_rotated([4, 5, 6, 7, 0, 1, 2], 0)  -> 4
    search_rotated([4, 5, 6, 7, 0, 1, 2], 3)  -> -1
    search_rotated([1], 1)                    -> 0

Follow-up questions:
- Why is at least one half always sorted?

Run (from interview_prep/python_course/week3/a07_binary_search): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 4.
"""


def search_rotated(nums: list[int], target: int) -> int:
    raise NotImplementedError
