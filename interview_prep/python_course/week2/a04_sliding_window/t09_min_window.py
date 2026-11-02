"""A4 t09 (★ optional, ~35 min). Minimum window substring.

Return the shortest substring of s that contains every character of t (with counts).
Return "" if there is none. If several have the same length, return the leftmost.

Examples:
    min_window("ADOBECODEBANC", "ABC")  -> "BANC"
    min_window("a", "a")                -> "a"
    min_window("a", "aa")               -> ""

Follow-up questions:
- How do you know in O(1) that the window covers t?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t09
Теория: THEORY.md в этой папке, раздел 2.
"""


def min_window(s: str, t: str) -> str:
    raise NotImplementedError
