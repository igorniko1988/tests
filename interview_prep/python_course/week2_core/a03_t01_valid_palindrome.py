"""A3 t01 (required, ~15 min). Valid palindrome with two pointers.

Return True if s is a palindrome considering only letters and digits (str.isalnum)
and ignoring case.

Requirements:
- Two pointers from both ends, O(1) extra memory: do NOT build a cleaned copy,
  do not use [::-1] or reversed() (the test checks the source).

Examples:
    valid_palindrome("A man, a plan, a canal: Panama")  -> True
    valid_palindrome("race a car")                      -> False
    valid_palindrome(".,")                              -> True
    valid_palindrome("0P")                              -> False

Follow-up questions:
- How is this better than C2 t04 (cleaned string + [::-1])?
- What happens when both pointers skip non-alphanumeric characters at once?

Run (from interview_prep/python_course/week2_core): uv run pytest -k a03_t01
Теория: THEORY.md в этой папке, раздел 1.
"""


def valid_palindrome(s: str) -> bool:
    cleaned = ''.join([ch.lower() for ch in s if ch.isalnum()])
    return cleaned == cleaned[::-1]

print(valid_palindrome("A man, a plan, a canal: Panama") )
