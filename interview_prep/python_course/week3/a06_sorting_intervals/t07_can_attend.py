"""A6 t07 (★ optional, ~10 min). Can attend all meetings.

Return True if one person can attend all meetings [start, end) (a meeting ending at 10
and one starting at 10 do not conflict).

Examples:
    can_attend([[0, 30], [5, 10], [15, 20]])  -> False
    can_attend([[7, 10], [2, 4]])             -> True
    can_attend([[1, 5], [5, 6]])              -> True

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t07
Теория: THEORY.md в этой папке, раздел 3.
"""


def can_attend(meetings: list[list[int]]) -> bool:
    raise NotImplementedError
