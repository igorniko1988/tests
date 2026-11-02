"""A2 t08 (★ optional, ~15 min). Isomorphic strings.

Two strings are isomorphic if characters of s can be replaced to get t:
every occurrence of a character maps to the same character, and no two
characters map to the same one.

Examples:
    is_isomorphic("egg", "add")      -> True
    is_isomorphic("foo", "bar")      -> False
    is_isomorphic("badc", "baba")    -> False   # b->b and d->b: two map to one
    is_isomorphic("", "")            -> True

Follow-up questions:
- Why do you need two dicts (or a dict and a set)?

Run (from interview_prep/python_course/week1/a2_hashing): uv run pytest -k t08
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def is_isomorphic(s: str, t: str) -> bool:
    raise NotImplementedError
