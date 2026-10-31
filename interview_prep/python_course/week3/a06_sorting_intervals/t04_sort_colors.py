"""A6 t04 (required, ~20 min). Sort colors (Dutch national flag).

nums contains only 0, 1 and 2. Sort it IN PLACE in one pass, O(1) extra memory,
without sort() / sorted() / counting into a new list (the test checks the source).
Return None.

Examples:
    nums = [2, 0, 2, 1, 1, 0]
    sort_colors(nums); nums  -> [0, 0, 1, 1, 2, 2]

    [2, 0, 1] -> [0, 1, 2]        [] -> []

Follow-up questions:
- What do low, mid and high point to? Why is mid not moved after swapping with high?

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 5.
"""


def sort_colors(nums: list[int]) -> None:
    raise NotImplementedError
