"""C6 t01 (required, ~10 min). timer decorator.

Implement a decorator timer that measures how long the decorated function runs.

Requirements:
- After every call print exactly: "<function name> took <seconds>s", seconds with
  3 decimals, e.g. "slow_add took 0.100s".
- Store the last duration (float, seconds) in the attribute last_duration
  of the decorated function.
- Return the original result; keep the name and docstring (functools.wraps).
- Use time.perf_counter().

Example:
    @timer
    def slow_add(a, b):
        time.sleep(0.1)
        return a + b

    slow_add(1, 2)          -> 3, prints "slow_add took 0.100s"
    slow_add.last_duration  -> 0.1003...
    slow_add.__name__       -> "slow_add"

Follow-up questions:
- Why perf_counter and not time.time()?
- Where does the decorator store func between calls?

Run (from interview_prep/python_course/week2_core): uv run pytest -k c06_t01
Теория: THEORY.md в этой папке, раздел 1–3.
"""


import time  # noqa: F401
from functools import wraps  # noqa: F401


def timer(func):
    raise NotImplementedError
