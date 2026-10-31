"""C6 t04 (required, ~15 min). A class-based decorator.

Implement a CLASS CountCalls that works as a decorator:

    @CountCalls
    def ping():
        return "pong"

Requirements:
- ping() calls the original function with any arguments and returns its result.
- ping.count - how many times it was called (an exception counts as a call too).
- ping.reset() sets count back to 0.
- ping.__name__ and ping.__doc__ come from the original (functools.update_wrapper).

Example:
    ping(); ping()
    ping.count   -> 2
    ping.reset()
    ping.count   -> 0

Follow-up questions:
- Which magic method makes an object callable?
- Function decorator with an attribute vs class decorator: pros and cons?

Run (from interview_prep/python_course/week2/c06_decorators): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 6.
"""


from functools import update_wrapper  # noqa: F401


class CountCalls:
    def __init__(self, func) -> None:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
