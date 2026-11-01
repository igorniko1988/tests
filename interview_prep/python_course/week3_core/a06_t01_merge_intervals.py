"""A6 t01 (required, ~20 min). Merge overlapping intervals.

Given a list of intervals [start, end] (start <= end), merge all overlapping intervals
and return them sorted by start. Touching intervals ([1, 2] and [2, 3]) are merged.

Requirements:
- O(n log n). Do not modify the input.

Examples:
    merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])  -> [[1, 6], [8, 10], [15, 18]]
    merge_intervals([[1, 4], [4, 5]])                     -> [[1, 5]]
    merge_intervals([[1, 10], [2, 3]])                    -> [[1, 10]]
    merge_intervals([])                                   -> []

Follow-up questions:
- Why is comparing with the LAST merged interval enough?

Run (from interview_prep/python_course/week3_core): uv run pytest -k a06_t01
Теория: THEORY.md в этой папке, раздел 2.
"""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError
