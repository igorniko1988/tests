"""X2 t01 (15 min, from scratch, no notes). retry.

Write from scratch a decorator with parameters:

    retry(times=3, exceptions=(Exception,), delay=0.0)

- Call the function up to `times` times in total.
- On one of `exceptions`: time.sleep(delay) and try again; after the last attempt
  re-raise the last exception (no sleep after it).
- Other exceptions are raised immediately.
- times < 1 -> ValueError when the decorator is created.
- Keep the function's name and docstring.

Example:
    @retry(times=3, exceptions=(ConnectionError,))
    def get_price(): ...    # fails twice, then returns 100

    get_price()  -> 100

Run (from interview_prep/python_course/week2/x2_exam): uv run pytest -k t01
"""


def retry(times=3, exceptions=(Exception,), delay=0.0):
    raise NotImplementedError
