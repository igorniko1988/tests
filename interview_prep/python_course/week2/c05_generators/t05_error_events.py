"""C5 t05 (required, ~20 min). A lazy pipeline of generators.

Build a lazy pipeline over log lines like:
    "2026-10-30T10:00:00 ERROR orders Timeout to price-feed"
    (timestamp, level, service, message with spaces)

Implement three generator functions and compose them in error_events(lines):
- parse(lines)          -> yields dicts {"ts", "level", "service", "msg"};
                           lines with fewer than 4 parts are skipped;
- only(events, level)   -> yields events with that level;
- error_events(lines)   -> only(parse(lines), "ERROR").

Requirements:
- Everything is lazy: error_events must work on an INFINITE iterator of lines
  (the test takes the first items with itertools.islice).
- error_events returns an iterator, not a list.

Example:
    lines = ["t1 INFO a ok", "t2 ERROR b db down", "bad", "t3 ERROR c x"]
    [e["service"] for e in error_events(lines)]  -> ["b", "c"]

Follow-up questions:
- In which order are lines read, parsed and filtered? Draw the "pull" chain.
- What breaks if parse() returns a list?

Run (from interview_prep/python_course/week2/c05_generators): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 7.
"""


def parse(lines):
    raise NotImplementedError


def only(events, level):
    raise NotImplementedError


def error_events(lines):
    raise NotImplementedError
