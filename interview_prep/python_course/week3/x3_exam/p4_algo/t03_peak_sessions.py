"""X3 t03 (algorithm, part of 40 min). Peak number of concurrent sessions.

sessions is a list of [start, end) times (ints, start < end) from a server log.
Return (peak, first_moment): the maximum number of sessions active at the same time and the
earliest moment when that maximum is reached. A session ending at t is NOT active at t.
For an empty list return (0, None).

Requirements:
- O(n log n). Tests use 100 000 sessions.

Examples:
    peak_sessions([[1, 5], [2, 6], [5, 7]])   -> (2, 2)
    peak_sessions([[1, 3], [3, 5]])           -> (1, 1)
    peak_sessions([[0, 10], [1, 2], [1, 3]])  -> (3, 1)

Follow-up questions:
- At the same moment, why must ends be processed before starts?

Run (from interview_prep/python_course/week3/x3_exam): uv run pytest -k t03
"""


def peak_sessions(sessions: list[list[int]]) -> tuple:
    raise NotImplementedError
