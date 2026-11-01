"""Q1 t02 (required, ~20 min). Diff of two JSON objects.

A regression test compares an API response with a saved one. Given two
dicts old and new (top-level keys only), return:

    {"added": [...], "removed": [...], "changed": [...]}

- added - keys present only in new;
- removed - keys present only in old;
- changed - keys present in both with different values (compared with ==);
- every list is sorted alphabetically.

Example:
    json_diff(
        {"id": 1, "status": "NEW", "price": "10.00"},
        {"id": 1, "status": "FILLED", "qty": 2},
    ) -> {"added": ["qty"], "removed": ["price"], "changed": ["status"]}

    json_diff({}, {}) -> {"added": [], "removed": [], "changed": []}

Follow-up questions:
- Which set operations give added and removed?
- How would you extend it to nested dicts? (Hint: Q1 t05 flatten.)

Run (from interview_prep/python_course/week1_core): uv run pytest -k q1_t02
Теория: interview_prep/python_course/c03_collections/s04_set/THEORY.md и s08_autotests/THEORY.md.
"""


def json_diff(old: dict, new: dict) -> dict[str, list[str]]:
    raise NotImplementedError
