"""C4 t02 (required, ~15 min). Log calls of any function.

Implement call_logger(func, log) that returns a NEW function. The new function
accepts ANY arguments, calls func with exactly the same arguments, appends a line
to the list log and returns func's result.

Log line format (args via repr, kwargs as name=repr(value), in call order):
    "add(1, 2, c=3) -> 6"
    "greet('Ann') -> 'Hello, Ann'"
    "ping() -> None"

Requirements:
- Use *args and **kwargs; do not change func.
- If func raises, the exception goes up and nothing is logged.

Example:
    log = []
    def add(a, b, c=0): return a + b + c
    logged_add = call_logger(add, log)
    logged_add(1, 2, c=3)   -> 6
    log                     -> ["add(1, 2, c=3) -> 6"]

Follow-up questions:
- Why repr() and not str() for arguments in logs?
- How will this become a decorator in C6?

Run (from interview_prep/python_course/week2/c04_functions): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 3.
"""


def call_logger(func, log: list[str]):
    raise NotImplementedError
