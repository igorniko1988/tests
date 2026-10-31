"""Q2 t01 (required, ~20 min). retry with exponential backoff.

Implement a decorator with parameters:

    retry(times=3, delay=0.5, backoff=2.0, exceptions=(ConnectionError, TimeoutError), sleep=time.sleep)

- Call the function up to `times` times in total.
- After a failed attempt with one of `exceptions`, call sleep(pause) and try again.
  The first pause is `delay`, every next one is multiplied by `backoff`:
  0.5, 1.0, 2.0, ...
- After the last failed attempt re-raise its exception; do not sleep after it.
- Other exceptions are raised immediately.
- The decorated function gets an attribute `attempts`: how many calls the LAST
  invocation made.
- times < 1 -> ValueError when the decorator is created. Use functools.wraps.

Example:
    pauses = []

    @retry(times=4, delay=0.5, backoff=2, sleep=pauses.append)
    def get_price(): ...      # fails 3 times with ConnectionError, then returns 100

    get_price()           -> 100
    pauses                -> [0.5, 1.0, 2.0]
    get_price.attempts    -> 4

Follow-up questions:
- Which HTTP errors are worth retrying and which are not?
- Why add random jitter in production?

Run (from interview_prep/python_course/week2/q2_function_utils): uv run pytest -k t01
Теория: THEORY.md в этой папке, раздел 1.
"""


import time
from functools import wraps  # noqa: F401


def retry(times=3, delay=0.5, backoff=2.0, exceptions=(ConnectionError, TimeoutError), sleep=time.sleep):
    raise NotImplementedError
