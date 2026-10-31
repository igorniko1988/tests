"""A2 t10 (★ optional, ~15 min). Intersection with counts.

Return the common elements of a and b, each repeated as many times as it
appears in BOTH lists (the minimum count). Keep the order of a.

Examples:
    intersect_counts([1, 2, 2, 1], [2, 2])        -> [2, 2]
    intersect_counts([4, 9, 5], [9, 4, 9, 8, 4])  -> [4, 9]
    intersect_counts([1, 1, 1], [1])              -> [1]
    intersect_counts([], [1])                     -> []

Follow-up questions:
- How is this different from C3 t03 (common_users)?

Run (from interview_prep/python_course/week1/a2_hashing): uv run pytest -k t10
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def intersect_counts(a: list[int], b: list[int]) -> list[int]:
    raise NotImplementedError
