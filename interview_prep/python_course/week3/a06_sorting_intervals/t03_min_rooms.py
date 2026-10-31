"""A6 t03 (required, ~25 min). Meeting rooms: how many are needed.

meetings is a list of [start, end) - a meeting occupies a room from start up to (but not
including) end, so a meeting ending at 10 and one starting at 10 can share a room.
Return the minimum number of rooms needed.

Requirements:
- O(n log n). Tests use 100 000 meetings.

Examples:
    min_rooms([[0, 30], [5, 10], [15, 20]])   -> 2
    min_rooms([[7, 10], [2, 4]])              -> 1
    min_rooms([[1, 5], [5, 10]])              -> 1
    min_rooms([])                             -> 0

Follow-up questions:
- Explain the "events" idea: +1 at start, -1 at end.
- How would a heap of end times solve it?

Run (from interview_prep/python_course/week3/a06_sorting_intervals): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 3.
"""


def min_rooms(meetings: list[list[int]]) -> int:
    raise NotImplementedError
