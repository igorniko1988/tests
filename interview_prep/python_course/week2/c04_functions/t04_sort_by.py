"""C4 t04 (required, ~20 min). Sort records by several fields.

Implement sort_by(records, *fields) that returns a NEW list of dicts sorted by
the given fields, in priority order. A field starting with "-" means descending.

Requirements:
- Any field may be descending, including strings ("-name").
- Fields compare by their natural order (numbers as numbers, strings as strings).
- The input list is not modified. With no fields, return a copy in the same order.

Examples:
    users = [
        {"name": "bob", "age": 30},
        {"name": "ann", "age": 25},
        {"name": "cat", "age": 30},
    ]
    sort_by(users, "age")           -> ann, bob, cat
    sort_by(users, "-age", "name")  -> bob, cat, ann
    sort_by(users, "-age", "-name") -> cat, bob, ann

Follow-up questions:
- Why can't you negate a string in a key tuple?
- Why does sorting in several passes (last field first) work?

Run (from interview_prep/python_course/week2/c04_functions): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 8; interview_prep/python_course/c03_collections/s07_sorting/THEORY.md.
"""


def sort_by(records: list[dict], *fields: str) -> list[dict]:
    raise NotImplementedError
