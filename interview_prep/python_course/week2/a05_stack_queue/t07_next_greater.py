"""A5 t07 (★ optional, ~20 min). Next greater element.

For every element of nums return the next element to the RIGHT that is greater than it,
or -1 if there is none.

Requirements:
- O(n) with a monotonic stack.

Examples:
    next_greater([2, 1, 2, 4, 3])  -> [4, 2, 4, -1, -1]
    next_greater([5, 4, 3])        -> [-1, -1, -1]
    next_greater([])               -> []

Follow-up questions:
- How does it change for a circular array?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t07
Теория: THEORY.md в этой папке, раздел 3.
"""


def next_greater(nums: list[int]) -> list[int]:
    raise NotImplementedError
