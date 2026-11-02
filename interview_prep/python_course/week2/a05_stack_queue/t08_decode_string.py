"""A5 t08 (★ optional, ~30 min). Decode string.

Decode strings like "3[a2[c]]": k[encoded] means encoded repeated k times. k is a positive
integer (may have several digits); brackets can be nested; the input is valid.

Examples:
    decode_string("3[a]2[bc]")    -> "aaabcbc"
    decode_string("3[a2[c]]")     -> "accaccacc"
    decode_string("2[abc]3[cd]ef") -> "abcabccdcdcdef"
    decode_string("10[x]")        -> "xxxxxxxxxx"

Follow-up questions:
- What do you push on "[" and what do you pop on "]"?

Run (from interview_prep/python_course/week2/a05_stack_queue): uv run pytest -k t08
Теория: THEORY.md в этой папке, раздел 4.
"""


def decode_string(s: str) -> str:
    raise NotImplementedError
