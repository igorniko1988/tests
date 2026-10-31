"""A4 t06 (required, ~20 min). Find all anagram start indices.

Return all start indices i where text[i:i + len(pattern)] is an anagram of pattern,
in ascending order.

Requirements:
- O(len(text)) for a fixed alphabet. Tests use a 100 000-character text.

Examples:
    find_anagrams("cbaebabacd", "abc")  -> [0, 6]
    find_anagrams("abab", "ab")         -> [0, 1, 2]
    find_anagrams("a", "ab")            -> []

Follow-up questions:
- How is this different from t04, and what code did you reuse?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 1, 3.
"""


def find_anagrams(text: str, pattern: str) -> list[int]:
    raise NotImplementedError
