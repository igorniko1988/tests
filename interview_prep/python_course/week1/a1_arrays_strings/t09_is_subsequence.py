"""A1 t09 (★ optional, ~10 min). Is subsequence.

Return True if s is a subsequence of t: all characters of s appear in t
in the same order, not necessarily next to each other.

Examples:
    is_subsequence("abc", "ahbgdc")  -> True
    is_subsequence("axc", "ahbgdc")  -> False
    is_subsequence("", "abc")        -> True
    is_subsequence("aa", "a")        -> False

Follow-up questions:
- Why is `all(ch in t for ch in s)` wrong?
- Complexity of the two-pointer solution?

Run (from interview_prep/python_course/week1/a1_arrays_strings): uv run pytest -k t09
"""


def is_subsequence(s: str, t: str) -> bool:
    raise NotImplementedError
