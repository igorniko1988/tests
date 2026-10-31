"""C2 t04 (required, ~10 min). Valid palindrome.

Given a string s, return True if it reads the same forward and backward,
considering ONLY letters and digits and ignoring case.

Requirements:
- Skip everything that is not alphanumeric (str.isalnum()): spaces, punctuation, "_".
- Case-insensitive (use casefold()).
- A string with no letters or digits ("", "!!") is a palindrome.
- Non-Latin letters count as letters too.

Examples:
    is_palindrome("A man, a plan, a canal: Panama")  -> True
    is_palindrome("race a car")                      -> False
    is_palindrome("А роза упала на лапу Азора")      -> True
    is_palindrome("0P")                              -> False
    is_palindrome("")                                -> True

Follow-up questions:
- What are the time and memory complexity of your solution?
- Can you do it with O(1) extra memory? (Hint: two pointers - lesson A3.)

Run (from interview_prep/python_course/todo): uv run pytest -k c2_t04
Теория: interview_prep/python_course/c02_numbers_strings/s04_strings/THEORY.md, раздел 4.
"""


def is_palindrome(s: str) -> bool:
    raise NotImplementedError
