"""A4 t05 (required, ~25 min). Longest repeating character replacement.

You may replace at most k characters of s with any letters. Return the length of the
longest substring that can be made of ONE repeated letter.

Requirements:
- O(n) time.

Examples:
    character_replacement("ABAB", 2)     -> 4
    character_replacement("AABABBA", 1)  -> 4     # "AABA" -> "AAAA"
    character_replacement("", 2)         -> 0
    character_replacement("ABC", 0)      -> 1

Follow-up questions:
- Why is "window length - max frequency <= k" the condition of a good window?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 2, 3.
"""


def character_replacement(s: str, k: int) -> int:
    raise NotImplementedError
