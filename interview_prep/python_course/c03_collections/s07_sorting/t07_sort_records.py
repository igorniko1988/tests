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
        {"name": "cat", "amount": None},
        {"name": "dan", "amount": "100"},
        {"name": "Abe", "amount": None},
    ])
    -> names in order: Ann, dan, bob, Abe, cat
       ("100.00" and "100" are equal as Decimal, so they are ordered by name)

Follow-up questions:
- Why does -Decimal(...) work in a sort key, but negation doesn't work for strings?
- How would you sort by name descending, then by amount ascending?

Run: uv run pytest -k t07
Теория: THEORY.md в этой папке, раздел 7.
"""


def sort_records(records: list[dict]) -> list[dict]:
    raise NotImplementedError
