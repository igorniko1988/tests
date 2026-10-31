"""C4 t03 (required, ~10 min). Fix late binding.

make_multipliers(n) must return a list of n functions; the i-th function
multiplies its argument by i. The naive version is broken:

    def make_multipliers(n):
        return [lambda x: x * i for i in range(n)]

    [f(10) for f in make_multipliers(3)]  -> [20, 20, 20]   # bug

Fix it so that:
    [f(10) for f in make_multipliers(3)]  -> [0, 10, 20]
    make_multipliers(0)                   -> []

Requirements:
- Each element must be callable with ONE argument: f(x).

Follow-up questions:
- Why do all lambdas see i == 2?
- Show a second fix (default argument vs functools.partial).

Run (from interview_prep/python_course/week2/c04_functions): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 7.
"""


def make_multipliers(n: int) -> list:
    raise NotImplementedError
