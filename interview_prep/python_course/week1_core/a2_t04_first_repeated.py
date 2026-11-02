"""A2 t04 (required, ~10 min). First repeated character.

Return the first character that appears in s for the SECOND time while
scanning left to right. Return None if no character repeats.

Examples:
    first_repeated("abcba")   -> "b"     # "b" repeats at index 3, before "a" at 4
    first_repeated("abca")    -> "a"
    first_repeated("abc")     -> None
    first_repeated("")        -> None

Follow-up questions:
- Why is a set enough here, while first_unique (X0) needed counts?
- Time and memory complexity?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a2_t04
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def first_repeated(s: str) -> str | None:
    for index,ch in enumerate(s):
        if s.count(ch) > 1:
            print(s.index(ch,index,len(s)))

print(first_repeated("abcba"))


