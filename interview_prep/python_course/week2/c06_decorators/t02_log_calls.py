"""C6 t02 (required, ~15 min). log_calls decorator with a parameter.

Implement a decorator with a parameter: log_calls(log) where log is a list.
Every call of the decorated function appends one line to log:

    "<name>(<args>) -> <result>"     on success
    "<name>(<args>) raised <ExceptionName>"   on an exception (then re-raise it)

<args>: positional args via repr, then kwargs as name=repr(value), joined by ", ".

Requirements:
- Use functools.wraps. Return the original result; exceptions go up unchanged.

Example:
    log = []

    @log_calls(log)
    def divide(a, b=1):
        return a / b

    divide(6, b=3)    -> 2.0
    divide(1, 0)      -> ZeroDivisionError
    log -> ["divide(6, b=3) -> 2.0", "divide(1, 0) raised ZeroDivisionError"]

Follow-up questions:
- Why three nested functions here and two in timer?
- What happens with @log_calls without parentheses?

Run (from interview_prep/python_course/week2/c06_decorators): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 4.
"""


from functools import wraps  # noqa: F401


def log_calls(log: list[str]):
    raise NotImplementedError
