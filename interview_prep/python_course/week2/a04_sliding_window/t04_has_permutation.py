"""A4 t04 (required, ~20 min). Permutation in string.

Return True if some permutation of pattern is a substring of text
(i.e. text has a window of len(pattern) with exactly the same letter counts).

Requirements:
- O(len(text)) time for a fixed alphabet: slide a window of len(pattern), update counts
  in O(1) per step. Tests use a 100 000-character text.

Examples:
    has_permutation("ab", "eidbaooo")  -> True     # "ba"
    has_permutation("ab", "eidboaoo")  -> False
    has_permutation("", "abc")         -> True
    has_permutation("abc", "ab")       -> False

Follow-up questions:
- Why compare counts, not sorted strings?

Run (from interview_prep/python_course/week2/a04_sliding_window): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 1, 3.
"""


def has_permutation(pattern: str, text: str) -> bool:
    raise NotImplementedError
