"""C2 t07 (required, ~5 min). Coalesce: first value that is not None.

A framework config takes a value "from the argument, else from the environment,
else the default". Implement coalesce(*values, default=None).

Requirements:
- Return the first value that is NOT None - even if it is falsy (0, "", [], False).
- If all values are None, or there are no values, return default.

Examples:
    coalesce(None, 0, 5)        -> 0
    coalesce(None, "", "x")     -> ""
    coalesce(None, None)        -> None
    coalesce(None, default=1)   -> 1
    coalesce(False, True)       -> False

Follow-up questions:
- What does `None or 0 or 5` return, and why is `or` wrong here?

Run (from interview_prep/python_course/todo): uv run pytest -k c2_t07
Теория: interview_prep/python_course/c02_numbers_strings/s07_truthy/THEORY.md, раздел 7.
"""


def coalesce(*values, default=None):
    for value in values:
        if value is not None:
            return value
    return default

print(  coalesce(None, default=1))
