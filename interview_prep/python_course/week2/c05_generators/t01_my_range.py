"""C5 t01 (required, ~15 min). Your own range as a generator.

Implement a generator function my_range(start, stop, step=1) that yields numbers
like the built-in range: start, start + step, ... while they are before stop.

Requirements:
- Must be a generator (use yield), do not call range().
- Negative step counts down: my_range(5, 0, -2) -> 5, 3, 1.
- step == 0 raises ValueError immediately, on the call (hint: a generator body
  does not run until the first next(), so check it outside the generator).
- Works with floats: my_range(0, 1, 0.25) -> 0, 0.25, 0.5, 0.75.

Examples:
    list(my_range(0, 5))        -> [0, 1, 2, 3, 4]
    list(my_range(1, 10, 3))    -> [1, 4, 7]
    list(my_range(5, 0, -2))    -> [5, 3, 1]
    list(my_range(3, 3))        -> []

Follow-up questions:
- Why would `raise ValueError` inside the generator body not fire on the call?
- What is the memory complexity of your generator?

Run (from interview_prep/python_course/week2/c05_generators): uv run pytest -k t01
Теория: THEORY.md в этой папке, раздел 4.
"""


def my_range(start, stop, step=1):
    raise NotImplementedError
