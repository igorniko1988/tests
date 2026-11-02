"""C4 t01 (required, ~10 min). Counter on a closure.

Implement make_counter(start=0, step=1) that returns a function. Every call of
that function returns the next number: start, start + step, start + 2 * step, ...

Requirements:
- Use a closure (nonlocal), no global variables and no classes.
- Counters are independent of each other.

Example:
    c = make_counter()
    c(), c(), c()          -> 0, 1, 2
    d = make_counter(10, 5)
    d(), d()               -> 10, 15
    c()                    -> 3

Follow-up questions:
- What happens without nonlocal, and why?
- Where is n stored after make_counter has returned? (Hint: __closure__.)

Run (from interview_prep/python_course/week2_core): uv run pytest -k c04_t01
Теория: THEORY.md в этой папке, раздел 5–6.
"""


def make_counter(start: int = 0, step: int = 1):
    raise NotImplementedError
