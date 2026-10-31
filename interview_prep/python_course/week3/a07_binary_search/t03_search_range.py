"""A7 t03 (required, ~20 min). First and last position of a value.

nums is sorted ascending and may contain duplicates. Return [first, last] indices of target,
or [-1, -1] if it is absent.

Requirements:
- O(log n): two binary searches, not one search + walking left/right
  (the test uses 1 000 000 equal values).
- Write the search yourself: no bisect, no index(), no `in` on the list (the test checks the source).

Examples:
    search_range([5, 7, 7, 8, 8, 10], 8)  -> [3, 4]
    search_range([5, 7, 7, 8, 8, 10], 6)  -> [-1, -1]
    search_range([], 0)                   -> [-1, -1]

Follow-up questions:
- How do you count occurrences of x in O(log n)?

Run (from interview_prep/python_course/week3/a07_binary_search): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 2.
"""


def search_range(nums: list[int], target: int) -> list[int]:
    raise NotImplementedError
