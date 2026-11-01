"""A1 t06 (required, ~15 min). String compression.

Given a string s, replace every run of the same character with the character
followed by the run length.

Requirements:
- Every run gets a count, even a run of 1: "abc" -> "a1b1c1".
- Case matters: "aA" -> "a1A1".
- Build the result with a list and "".join().

Examples:
    compress("aaab")       -> "a3b1"
    compress("aabcccccaa") -> "a2b1c5a2"
    compress("abc")        -> "a1b1c1"
    compress("")           -> ""

Follow-up questions:
- Why is Counter(s) wrong here? (Look at "aabaa".)
- How do you handle the last run?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a1_t06
Теория: interview_prep/python_course/c02_numbers_strings/s04_strings/THEORY.md (сборка строки).
"""


def compress(s: str) -> str:
    raise NotImplementedError
