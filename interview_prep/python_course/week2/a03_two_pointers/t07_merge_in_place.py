"""A3 t07 (★ optional, ~20 min). Merge sorted arrays in place.

a has length m + n: the first m elements are sorted values, the last n are zeros
(free space). b has n sorted values. Merge b into a IN PLACE so a is sorted.

Requirements:
- O(m + n) time, no extra list, no sort. Return None.

Example:
    a = [1, 2, 3, 0, 0, 0]
    merge_in_place(a, 3, [2, 5, 6], 3)
    a  -> [1, 2, 2, 3, 5, 6]

Follow-up questions:
- Why fill from the END?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t07
Теория: THEORY.md в этой папке, раздел 3.
"""


def merge_in_place(a: list[int], m: int, b: list[int], n: int) -> None:
    raise NotImplementedError
