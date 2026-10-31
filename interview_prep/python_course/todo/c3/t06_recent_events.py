"""C3 t06 (required, ~10 min). Keep the last N events.

Implement a class that stores only the N most recent events
(e.g. the last requests of an API client, attached to a report on failure).

Implement:
- RecentEvents(n) - keep at most n latest events; raise ValueError if n < 1.
- add(event) - add an event.
- items() -> list - stored events from oldest to newest. Return a NEW list:
  changing it must not affect the storage.
- total - a property: how many events were added in total, including dropped ones.
- len(r) - how many events are stored right now.

Memory must be O(n): the test adds 200 000 events with n = 3.

Example:
    r = RecentEvents(3)
    for e in ["e1", "e2", "e3", "e4"]:
        r.add(e)
    r.items()  -> ["e2", "e3", "e4"]
    len(r)     -> 3
    r.total    -> 4

Follow-up questions:
- Why not a list with pop(0) when it is full?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_c3.py -k t06
Теория: interview_prep/python_course/c03_collections/s06_deque/THEORY.md, раздел 6.
"""


class RecentEvents:
    def __init__(self, n: int) -> None:
        raise NotImplementedError

    def add(self, event) -> None:
        raise NotImplementedError

    def items(self) -> list:
        raise NotImplementedError

    @property
    def total(self) -> int:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
