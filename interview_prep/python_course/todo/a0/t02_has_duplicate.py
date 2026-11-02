"""A0 t02 (required, ~10 min). Contains duplicate - optimize O(n^2) to O(n).

Given a list of hashable values, return True if any value appears at least twice,
otherwise False. Do not modify the input.

Examples:
    has_duplicate([1, 2, 3, 1])  -> True
    has_duplicate([1, 2, 3])     -> False
    has_duplicate([])            -> False
    has_duplicate(["a", "A"])    -> False

The code below is a working brute-force solution: it compares every pair, O(n^2).
On 10 000 items it takes ~3 s, the test allows 0.2 s. Rewrite it in O(n) time.

Follow-up questions:
- Time and memory complexity before and after?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_a0.py -k t02
Теория: interview_prep/python_course/a00_big_o/s07_method/THEORY.md и interview_prep/python_course/a00_big_o/s04_hidden_cost/THEORY.md.
"""


def has_duplicate(items: list) -> bool:
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False
