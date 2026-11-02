"""C7 t03 (required, ~15 min). Count instances with class attributes.

Implement a class Session:

- Session.created - class attribute: how many sessions were created in total;
- Session.active  - class attribute: how many sessions are created and not closed;
- every session gets self.number - its sequential number (1, 2, 3, ...);
- close() closes the session; closing twice changes nothing; s.closed -> bool;
- Session.reset_counters() - classmethod that sets both counters to 0 (for tests).

Example:
    Session.reset_counters()
    a, b = Session(), Session()
    a.number, b.number            -> 1, 2
    a.close(); a.close()
    Session.created, Session.active  -> 2, 1

Follow-up questions:
- Why does self.created += 1 not work as a class counter?

Run (from interview_prep/python_course/week3/c07_classes): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 2.
"""


class Session:
    def __init__(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    @classmethod
    def reset_counters(cls) -> None:
        raise NotImplementedError
