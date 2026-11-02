"""C7 t04 (required, ~10 min). Find and fix the bug.

RequestLog collects requests made by an API client so a test can attach them to its report.
In a test run, logs of different clients get mixed up: a fresh client already has requests
from other tests. Find the bug in the code below and fix it, keeping the interface:

- RequestLog(name) - a new empty log;
- add(method, path) - remember a request as "METHOD path";
- entries - list of remembered requests in order;
- clear() - forget everything in THIS log only.

Follow-up questions:
- Explain where entries lived before the fix and why clear() made it worse.

Run (from interview_prep/python_course/week3/c07_classes): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 2.
"""


class RequestLog:
    entries = []
    name = "default"

    def __init__(self, name: str) -> None:
        self.name = name

    def add(self, method: str, path: str) -> None:
        self.entries.append(f"{method} {path}")

    def clear(self) -> None:
        self.entries.clear()
