"""A1 t01 (required, ~10 min). Reverse words in a string.

Given a string s, return the words in reverse order, joined by a single space.

Requirements:
- A word is a sequence of non-space characters.
- s may have leading/trailing spaces and several spaces between words;
  the result has no extra spaces.

Examples:
    reverse_words("the sky is blue")       -> "blue is sky the"
    reverse_words("  hello   world  ")     -> "world hello"
    reverse_words("a")                     -> "a"
    reverse_words("   ")                   -> ""

Follow-up questions:
- Why build a list and "".join() it instead of result += word?
- What are the time and memory complexity?

Run (from interview_prep/python_course/week1/a1_arrays_strings): uv run pytest -k t01
Теория: interview_prep/python_course/c02_numbers_strings/s04_strings/THEORY.md (split, join).
"""


def reverse_words(s: str) -> str:
    raise NotImplementedError
