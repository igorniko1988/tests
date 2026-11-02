"""A7 t09 (★ optional, ~20 min). Search a sorted 2D matrix.

Each row of matrix is sorted, and the first value of each row is greater than the last value
of the previous row. Return True if target is in the matrix, in O(log(rows * cols)).

Examples:
    search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3)   -> True
    search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13)  -> False
    search_matrix([], 1)                                                   -> False

Follow-up questions:
- How do you turn a flat index into (row, col)?

Run (from interview_prep/python_course/week3/a07_binary_search): uv run pytest -k t09
Теория: THEORY.md в этой папке, раздел 1.
"""


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    raise NotImplementedError
