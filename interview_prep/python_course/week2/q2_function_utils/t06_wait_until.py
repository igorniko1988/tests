"""Q2 t06 (required, ~20 min). wait_until: wait for a condition with a timeout.

Implement wait_until(condition, timeout=5.0, interval=0.1, *, message="condition",
clock=time.monotonic, sleep=time.sleep):

- call condition(); if the result is truthy - return the result;
- otherwise, if clock() - start >= timeout - raise
  TimeoutError(f"{message} not met in {timeout}s, last value: {result!r}");
- otherwise sleep(interval) and repeat.

Requirements:
- condition is checked at least once, even with timeout=0.
- Exceptions from condition go up unchanged.
- Use only clock and sleep from the parameters (tests pass fake ones).

Example:
    statuses = iter(["NEW", "NEW", "FILLED"])
    wait_until(lambda: next(statuses) == "FILLED", timeout=1, interval=0.1)  -> True

Follow-up questions:
- Why return the condition's value and not just True?
- Why is time.sleep(5) in a test worse?

Run (from interview_prep/python_course/week2/q2_function_utils): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 2–3.
"""


import time


def wait_until(condition, timeout=5.0, interval=0.1, *, message="condition", clock=time.monotonic, sleep=time.sleep):
    raise NotImplementedError
