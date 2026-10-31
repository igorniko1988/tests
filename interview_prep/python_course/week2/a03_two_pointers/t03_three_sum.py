"""A3 t03 (required, ~30 min). 3sum.

Return all unique triplets [a, b, c] from nums with a + b + c == 0.

Requirements:
- Each triplet sorted ascending; the list of triplets sorted ascending.
- No duplicate triplets. O(n^2) time. Tests use 1 500 numbers.

Examples:
    three_sum([-1, 0, 1, 2, -1, -4])  -> [[-1, -1, 2], [-1, 0, 1]]
    three_sum([0, 0, 0, 0])           -> [[0, 0, 0]]
    three_sum([1, 2, -2, -1])         -> []

Follow-up questions:
- Where exactly do you skip duplicates, and why there?
- Why is O(n^2) the best you can do here?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 5.
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError
