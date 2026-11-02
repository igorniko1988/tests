"""A3 t08 (★ optional, ~20 min). Valid palindrome II.

Return True if s can become a palindrome after deleting AT MOST one character.
Compare characters as is (case-sensitive, no filtering).

Examples:
    almost_palindrome("aba")    -> True
    almost_palindrome("abca")   -> True     # delete "b" or "c"
    almost_palindrome("abc")    -> False
    almost_palindrome("")       -> True

Follow-up questions:
- At the first mismatch, which two options do you check?

Run (from interview_prep/python_course/week2/a03_two_pointers): uv run pytest -k t08
Теория: THEORY.md в этой папке, раздел 1.
"""


def almost_palindrome(s: str) -> bool:
    raise NotImplementedError
