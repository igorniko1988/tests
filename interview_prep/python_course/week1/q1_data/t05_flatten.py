"""Q1 t05 (required, ~20 min). Flatten a nested dict.

Nested API responses are easier to compare when flattened. Given a dict,
return a new dict where nested dict keys are joined with sep.

Requirements:
- Only dicts are flattened; lists and other values are kept as they are.
- An empty nested dict is kept as a value: {"a": {}} -> {"a": {}}.
- Key order: depth-first, as keys appear.
- Do not modify the input.

Examples:
    flatten({"a": 1, "b": {"c": 2, "d": {"e": 3}}})
        -> {"a": 1, "b.c": 2, "b.d.e": 3}
    flatten({"user": {"tags": ["x"]}}, sep="/")
        -> {"user/tags": ["x"]}
    flatten({}) -> {}

Follow-up questions:
- Recursive or iterative: what is the risk of recursion on deep data?
- How would you un-flatten it back?

Run (from interview_prep/python_course/week1/q1_data): uv run pytest -k t05
Теория: interview_prep/python_course/c01_objects/s10_autotests/THEORY.md.
"""


def flatten(data: dict, sep: str = ".") -> dict:
    raise NotImplementedError
