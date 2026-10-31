"""A3 t06 (required, ~15 min). Squares of a sorted array.

nums is sorted ascending and may contain negatives. Return a new list of the squares,
sorted ascending.

Requirements:
- O(n) time: do NOT sort (the test checks the source). Hint: the largest square is at
  one of the ENDS of nums.

Examples:
    sorted_squares([-4, -1, 0, 3, 10])  -> [0, 1, 9, 16, 100]
    sorted_squares([-7, -3, 2, 3, 11])  -> [4, 9, 9, 49, 121]
    sorted_squares([])                  -> []

Follow-up questions:
- Why fill the result from the end?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 1.
"""


def sorted_squares(nums: list[int]) -> list[int]:
    raise NotImplementedError
