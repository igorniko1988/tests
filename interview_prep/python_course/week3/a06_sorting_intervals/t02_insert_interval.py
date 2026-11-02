"""A6 t02 (required, ~20 min). Insert an interval.

intervals are sorted by start and do NOT overlap. Insert new (merging if needed) and
return the resulting sorted, non-overlapping list. Touching intervals are merged.

Requirements:
- O(n) - the input is already sorted, do not sort again.

Examples:
    insert_interval([[1, 3], [6, 9]], [2, 5])                  -> [[1, 5], [6, 9]]
    insert_interval([[1, 2], [3, 5], [6, 7], [8, 10]], [4, 8]) -> [[1, 2], [3, 10]]
    insert_interval([], [5, 7])                                -> [[5, 7]]
    insert_interval([[1, 5]], [6, 8])                          -> [[1, 5], [6, 8]]

Follow-up questions:
- Name the three phases of the loop.

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 2.
"""


def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    raise NotImplementedError
