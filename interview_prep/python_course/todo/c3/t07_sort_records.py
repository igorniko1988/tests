"""C3 t07 (required, ~15 min). Sort records by multiple fields.

Given a list of records {"name": str, "amount": str | None}, return a new
sorted list. Amounts come from an API as strings.

Sort order:
1. By amount DESCENDING, compared as numbers (Decimal), not as strings.
2. Equal amounts - by name, case-insensitive, ascending.
3. Records with amount None go last, sorted by name (case-insensitive).

Do not modify the input list.

Example:
    sort_records([
        {"name": "bob", "amount": "9.50"},
        {"name": "Ann", "amount": "100.00"},
        {"name": "cat", "amount": 23},
        {"name": "dan", "amount": "100"},
        {"name": "Abe", "amount": 1},
    ])
    -> names in order: Ann, dan, bob, Abe, cat
       ("100.00" and "100" are equal as Decimal, so they are ordered by name)

Follow-up questions:
- Why does -Decimal(...) work in a sort key, but negation doesn't work for strings?
- How would you sort by name descending, then by amount ascending?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_c3.py -k t07
Теория: interview_prep/python_course/c03_collections/s07_sorting/THEORY.md, раздел 7.
"""

from decimal import Decimal

def sort_records(records: list[dict]) -> list[dict]:
    sorted_list = sorted(records,key=lambda k: Decimal(k['amount'] if k['amount'] is not None else 0),reverse=True)
    return sorted_list

rec = [
    {"name": "bob", "amount": "9.50"},
    {"name": "Ann", "amount": "100.00"},
    {"name": "cat", "amount": None},      # ← было None, у тебя 23
    {"name": "dan", "amount": "100"},
    {"name": "Abe", "amount": None},      # ← было None, у тебя 1
]

print(sort_records(rec))
