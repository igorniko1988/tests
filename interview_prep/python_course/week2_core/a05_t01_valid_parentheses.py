"""A5 t01 (required, ~15 min). Valid parentheses.

s contains only the characters ()[]{}. Return True if every bracket is closed by the
same type of bracket and in the correct order.

Examples:
    valid_parentheses("()[]{}")   -> True
    valid_parentheses("([]{})")   -> True
    valid_parentheses("(]")       -> False
    valid_parentheses("([)]")     -> False
    valid_parentheses("((")       -> False
    valid_parentheses("")         -> True

Follow-up questions:
- Which three kinds of errors does your solution catch, and where?

Run (from interview_prep/python_course/week2_core): uv run pytest -k a05_t01
Теория: THEORY.md в этой папке, раздел 2.
"""


def valid_parentheses(s: str) -> bool:
    raise NotImplementedError
