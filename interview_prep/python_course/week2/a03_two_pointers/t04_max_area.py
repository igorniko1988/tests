"""A3 t04 (required, ~20 min). Container with most water.

heights[i] is the height of a vertical line at x = i. Two lines with the x-axis form
a container holding min(h[i], h[j]) * (j - i) water. Return the maximum.

Requirements:
- O(n) time. Tests use 100 000 lines.

Examples:
    max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])  -> 49
    max_area([1, 1])                       -> 1
    max_area([4])                          -> 0

Follow-up questions:
- Why do you always move the SHORTER line?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 1.
"""


def max_area(heights: list[int]) -> int:
    raise NotImplementedError
