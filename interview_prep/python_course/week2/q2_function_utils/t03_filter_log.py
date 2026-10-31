"""Q2 t03 (★ optional, ~15 min). Filter log lines by level and request id.

Log lines look like: "<ts> <LEVEL> <request_id> <message with spaces>".
Implement a generator filter_log(lines, level=None, request_id=None) that yields
(line_number, line) for lines that match ALL given filters (None = any).

Requirements:
- line_number starts at 1; lines with fewer than 4 parts are skipped.
- Compare level and request_id exactly (not substring). Lazy: works on infinite input.

Example:
    lines = ["t1 INFO r1 start", "t2 ERROR r1 db down", "t3 ERROR r2 x", "bad"]
    list(filter_log(lines, level="ERROR"))                   -> [(2, ...), (3, ...)]
    list(filter_log(lines, level="ERROR", request_id="r1"))  -> [(2, "t2 ERROR r1 db down")]

Follow-up questions:
- Why is "ERROR" in line a bad filter?

Run (from interview_prep/python_course/week2/q2_function_utils): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 6.
"""


def filter_log(lines, level=None, request_id=None):
    raise NotImplementedError
