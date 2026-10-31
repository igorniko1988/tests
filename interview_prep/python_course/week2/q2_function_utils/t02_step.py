"""Q2 t02 (required, ~15 min). Test step decorator: status, time, log.

Implement a decorator with parameters step(name, log). Every call appends one line to
the list log:

    "STEP <name>: PASSED in <seconds>s"         seconds with 2 decimals, e.g. 0.05s
    "STEP <name>: FAILED <ExceptionName>"      then re-raise the exception

`name` may contain {placeholders} filled from the call's KEYWORD arguments:

    @step("create order {symbol}", log)
    def create_order(*, symbol, qty): ...

    create_order(symbol="BTC", qty=1)   # "STEP create order BTC: PASSED in 0.00s"

Requirements:
- Return the original result; keep the name (functools.wraps). Use time.perf_counter().

Follow-up questions:
- Why must the exception be re-raised?
- How does allure.step show nested steps?

Run (from interview_prep/python_course/week2/q2_function_utils): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 4.
"""


import time  # noqa: F401
from functools import wraps  # noqa: F401


def step(name: str, log: list[str]):
    raise NotImplementedError
