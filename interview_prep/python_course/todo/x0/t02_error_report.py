"""X0 t02 (~25 min). Error report from a log.

You get a list of log lines like:
    "2026-10-28T10:00:00 ERROR orders Timeout to price-feed"
    timestamp, level, service, message (the message may contain spaces).

Return a list of (service, count) pairs for lines with level ERROR:
- sorted by count descending;
- ties broken by service name alphabetically;
- at most `top` pairs (default 3).
Skip empty lines and lines with fewer than four parts.

Example:
    error_report([
        "2026-10-28T10:00:00 ERROR orders Timeout to price-feed",
        "2026-10-28T10:00:01 INFO orders Created 42",
        "2026-10-28T10:00:02 ERROR auth Bad token",
        "2026-10-28T10:00:03 ERROR orders Insufficient funds",
        "",
    ]) -> [("orders", 2), ("auth", 1)]

Follow-up questions:
- Why split(maxsplit=3)?
- What is the complexity of your solution?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_x0.py -k t02
"""


def error_report(lines: list[str], top: int = 3) -> list[tuple[str, int]]:
    raise NotImplementedError
