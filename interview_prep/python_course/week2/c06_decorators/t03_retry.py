"""C6 t03 (required, ~20 min). retry(times, exceptions, delay).

Implement a decorator with parameters:

    retry(times=3, exceptions=(Exception,), delay=0.0)

The decorated function is called up to `times` times in total:
- if it returns - return the result immediately;
- if it raises one of `exceptions` - sleep `delay` seconds (time.sleep) and try again;
- if the last attempt fails - re-raise that last exception;
- any OTHER exception is raised immediately, without retries.

Requirements:
- times < 1 raises ValueError when the decorator is created.
- Do not sleep after the last attempt. Use functools.wraps.

Example:
    @retry(times=3, exceptions=(ConnectionError,))
    def get_price():
        ...   # fails twice with ConnectionError, then returns 100

    get_price()  -> 100    (3 calls)

Follow-up questions:
- Which requests are safe to retry and which are not? (idempotency)
- Why is catching Exception by default dangerous in tests?

Run (from interview_prep/python_course/week2/c06_decorators): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 4.
"""


import time  # noqa: F401
from functools import wraps  # noqa: F401


def retry(times: int = 3, exceptions: tuple = (Exception,), delay: float = 0.0):
    raise NotImplementedError
