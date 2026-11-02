"""X2 t02 (algorithm, part of 40 min). Backspace string compare.

"#" means backspace: it deletes the previous character (if any). Return True if
s and t are equal after typing both into an empty editor.

Requirements:
- O(n + m) time.

Examples:
    backspace_compare("ab#c", "ad#c")    -> True     # both "ac"
    backspace_compare("ab##", "c#d#")    -> True     # both ""
    backspace_compare("a#c", "b")        -> False
    backspace_compare("#a", "a")         -> True

Follow-up questions:
- Stack solution vs two pointers from the end: memory of each?

Run (from interview_prep/python_course/week2/x2_exam): uv run pytest -k t02
"""


def backspace_compare(s: str, t: str) -> bool:
    raise NotImplementedError
