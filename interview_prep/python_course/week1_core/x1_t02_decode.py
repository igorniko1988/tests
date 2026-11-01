"""X1 t02 (algorithm, part of 40 min). Decode a compressed string.

The reverse of A1 t06: decode a string where every character is followed
by its run length.

Requirements:
- A count may have several digits: "a12" means twelve "a".
- The input is always valid: a non-digit character, then a count >= 1.
- Build the result with a list and "".join().

Examples:
    decode("a3b1")      -> "aaab"
    decode("a2b1c5a2")  -> "aabcccccaa"
    decode("z12")       -> "zzzzzzzzzzzz"
    decode("")          -> ""

Follow-up questions:
- How do you collect a multi-digit number while scanning?
- What is the complexity in terms of the OUTPUT length?

Run (from interview_prep/python_course/week1_core): uv run pytest -k x1_t02
"""


def decode(s: str) -> str:
    raise NotImplementedError
