"""C1 t07 (required, ~15 min). Remove duplicates, keep order.

Given a list of values from a JSON response, return a new list with duplicates
removed, keeping the FIRST occurrence and the original order.

Requirements:
- Items may be unhashable: dicts and lists (so set(items) fails with TypeError).
- Dicts are equal regardless of key order; [1, 2] and [2, 1] are different values.
- Return the ORIGINAL objects, not copies (the test checks with `is`).
- Time complexity O(n). Tests use 20 000 items.
- You may use the ready helper: `from freeze_helper import freeze` - it turns
  dicts/lists/sets into hashable frozensets/tuples.

Examples:
    dedupe([3, 1, 3, 2, 1])                       -> [3, 1, 2]
    dedupe([{"id": 1}, {"id": 2}, {"id": 1}])     -> [{"id": 1}, {"id": 2}]
    dedupe([[1, 2], [1, 2], [2, 1]])              -> [[1, 2], [2, 1]]
    dedupe([{"a": 1, "b": 2}, {"b": 2, "a": 1}])  -> [{"a": 1, "b": 2}]
    dedupe([])                                    -> []

Follow-up questions:
- Why not list(set(items))?
- Why is `if item not in result` O(n^2)?
- What are the time and memory complexity of your solution?

Run (from interview_prep/python_course/todo): uv run pytest -k c1_t07
Теория: interview_prep/python_course/c01_objects/s09_hashable/THEORY.md, раздел 9.
"""


def dedupe(items: list) -> list:
    raise NotImplementedError
