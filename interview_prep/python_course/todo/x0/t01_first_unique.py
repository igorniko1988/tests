"""X0 t01 (~20 min). First unique character.

Given a string s, return the index of the first character that appears in s
exactly once. If there is no such character, return -1.
Case matters: "a" and "A" are different characters.

Examples:
    first_unique("leetcode")      -> 0    # "l"
    first_unique("loveleetcode")  -> 2    # "v"
    first_unique("aabb")          -> -1
    first_unique("")              -> -1

Follow-up questions:
- What are the time and memory complexity of your solution?
- Why is s.count(ch) inside the loop a bad idea?

Run (from interview_prep/python_course/todo): uv run pytest tests/test_x0.py -k t01
"""


def first_unique(s: str) -> int:
    for index, char in enumerate(s):
        if s.count(char) == 1:
            return index
    return -1

print( first_unique("") )


