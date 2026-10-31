"""C9 t01 (required, ~20 min). Vector with operators.

Implement a class Vector(x, y) with:
- v + w, v - w -> new Vector; v * k and k * v (k is a number) -> new Vector;
- v == w by coordinates; comparing with a non-Vector returns NotImplemented
  (so Vector(1, 2) == (1, 2) is False, not an error);
- abs(v) -> length (float);
- repr(v) -> "Vector(1, 2)";
- sum(list_of_vectors) works (hint: __radd__ with 0);
- vectors are hashable consistently with ==.

Example:
    Vector(1, 2) + Vector(3, 4)   -> Vector(4, 6)
    2 * Vector(1, 2)              -> Vector(2, 4)
    abs(Vector(3, 4))             -> 5.0
    sum([Vector(1, 1), Vector(2, 2)])  -> Vector(3, 3)

Follow-up questions:
- Why does 3 * v need __rmul__?
- Why return NotImplemented, not False?

Run (from interview_prep/python_course/week3/c09_magic_methods): uv run pytest -k t01
Теория: THEORY.md в этой папке, раздел 2, 4.
"""


class Vector:
    def __init__(self, x, y) -> None:
        raise NotImplementedError
