"""A4 t02 (required, ~20 min). Longest substring without repeating characters.

Return the length of the longest substring of s with no repeated characters.

Requirements:
- O(n) time. Tests use a 200 000-character string.

Examples:
    longest_unique("abcabcbb")  -> 3     # "abc"
    longest_unique("bbbbb")     -> 1
    longest_unique("pwwkew")    -> 3     # "wke"
    longest_unique("")          -> 0
    longest_unique("abba")      -> 2

Follow-up questions:
- Why does "abba" break a naive left = last_seen[ch] + 1?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 2.
"""


def longest_unique(s: str) -> int:
    raise NotImplementedError
