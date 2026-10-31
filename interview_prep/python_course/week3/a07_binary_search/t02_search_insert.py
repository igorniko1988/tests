"""A7 t02 (required, ~15 min). Search insert position.

nums is sorted ascending with distinct values. Return the index of target if it is present,
otherwise the index where it would be inserted to keep the order.

Requirements:
- O(log n).
- Write the search yourself: no bisect, no index(), no `in` on the list (the test checks the source).

Examples:
    search_insert([1, 3, 5, 6], 5)  -> 2
    search_insert([1, 3, 5, 6], 2)  -> 1
    search_insert([1, 3, 5, 6], 7)  -> 4
    search_insert([], 3)            -> 0

Follow-up questions:
- Which bisect function gives the same result?

Run (from interview_prep/python_course/week3/a07_binary_search): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 2.
"""


def search_insert(nums: list[int], target: int) -> int:
    raise NotImplementedError
