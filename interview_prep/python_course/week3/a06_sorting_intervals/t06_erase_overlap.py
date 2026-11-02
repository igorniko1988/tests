"""A6 t06 (required, ~20 min). Non-overlapping intervals.

Return the minimum number of intervals to remove so that the rest do not overlap.
Touching intervals ([1, 2] and [2, 3]) do NOT overlap.

Requirements:
- O(n log n), greedy.

Examples:
    erase_overlap([[1, 2], [2, 3], [3, 4], [1, 3]])  -> 1
    erase_overlap([[1, 2], [1, 2], [1, 2]])          -> 2
    erase_overlap([[1, 2], [2, 3]])                  -> 0
    erase_overlap([])                                -> 0

Follow-up questions:
- Why sort by END, not by start?

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 4.
"""


def erase_overlap(intervals: list[list[int]]) -> int:
    raise NotImplementedError
