"""C5 t06 (★ optional, ~20 min). groupby by hand.

Implement a generator group_consecutive(iterable, key=None) that groups
CONSECUTIVE items with the same key and yields (key, list_of_items), like
itertools.groupby but with lists. key=None means the item itself is the key.

Requirements:
- Do not use itertools. Lazy: works on an infinite iterator (take groups with islice).

Examples:
    list(group_consecutive("aabaa"))
        -> [("a", ["a", "a"]), ("b", ["b"]), ("a", ["a", "a"])]
    list(group_consecutive([1, 3, 2, 4, 5], key=lambda x: x % 2))
        -> [(1, [1, 3]), (0, [2, 4]), (1, [5])]
    list(group_consecutive([]))  -> []

Follow-up questions:
- How do you group ALL equal keys, not only consecutive ones?

Run (from interview_prep/python_course/week2/c05_generators): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 8.
"""


def group_consecutive(iterable, key=None):
    raise NotImplementedError
