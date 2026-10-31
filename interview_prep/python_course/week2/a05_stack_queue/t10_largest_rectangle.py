"""A5 t10 (★ optional, ~40 min). Largest rectangle in a histogram.

heights[i] is the height of a bar of width 1. Return the area of the largest rectangle
that fits inside the histogram.

Requirements:
- O(n) with a monotonic stack. Tests use 100 000 bars.

Examples:
    largest_rectangle([2, 1, 5, 6, 2, 3])  -> 10
    largest_rectangle([2, 4])              -> 4
    largest_rectangle([])                  -> 0

Follow-up questions:
- When a bar is popped, how do you know its left and right borders?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t10
Теория: THEORY.md в этой папке, раздел 3.
"""


def largest_rectangle(heights: list[int]) -> int:
    raise NotImplementedError
