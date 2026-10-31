"""A3 t10 (★ optional, ~30 min). Trapping rain water.

heights[i] is the height of a bar of width 1. Return how much rain water is trapped
between the bars.

Requirements:
- O(n) time, O(1) extra memory (two pointers with left_max / right_max).

Examples:
    trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])  -> 6
    trap_water([4, 2, 0, 3, 2, 5])                    -> 9
    trap_water([])                                    -> 0

Follow-up questions:
- Why is it safe to compute water on the side with the smaller max?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t10
Теория: THEORY.md в этой папке, раздел 1.
"""


def trap_water(heights: list[int]) -> int:
    raise NotImplementedError
