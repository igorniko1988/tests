"""Q2 t05 (★ optional, ~15 min). Flatten a list of any depth.

Return a flat list of all values from a nested structure of lists and tuples,
in order. Strings are values (do not split them into characters).

Examples:
    flatten([1, [2, [3, (4, 5)]], 6])   -> [1, 2, 3, 4, 5, 6]
    flatten(["ab", ["cd"]])             -> ["ab", "cd"]
    flatten([[], [[]]])                 -> []

Follow-up questions:
- Recursion limit: how deep can the input be? How to do it iteratively with a stack?

Run (from interview_prep/python_course/week2/q2_function_utils): uv run pytest -k t05
Теория: interview_prep/python_course/week2/c05_generators/THEORY.md, раздел 7.
"""


def flatten(nested) -> list:
    raise NotImplementedError
