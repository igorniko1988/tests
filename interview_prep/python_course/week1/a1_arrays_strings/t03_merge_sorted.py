"""A1 t03 (required, ~15 min). Merge two sorted lists.

Given two lists a and b, each sorted in ascending order, return ONE new
list with all elements of both, sorted in ascending order.

Requirements:
- O(n + m) time. Do NOT use sorted() or .sort() - the test checks the source.
- Do not modify a and b.

Examples:
    merge_sorted([1, 3, 5], [2, 4])   -> [1, 2, 3, 4, 5]
    merge_sorted([1, 1], [1])         -> [1, 1, 1]
    merge_sorted([], [7])             -> [7]

Follow-up questions:
- Why is sorted(a + b) O((n + m) log(n + m)) and what does merging gain?
- Where is this step used? (Hint: merge sort.)

Run (from interview_prep/python_course/week1/a1_arrays_strings): uv run pytest -k t03
Теория: interview_prep/python_course/a00_big_o/s07_method/THEORY.md (метод решения).
"""


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    raise NotImplementedError
