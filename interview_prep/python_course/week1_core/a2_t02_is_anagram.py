"""A2 t02 (required, ~10 min). Valid anagram.

Return True if b is an anagram of a: the same characters with the same
counts, in any order. Case and spaces matter (compare characters as is).

Examples:
    is_anagram("listen", "silent")  -> True
    is_anagram("rat", "car")        -> False
    is_anagram("aab", "abb")        -> False
    is_anagram("", "")              -> True

Follow-up questions:
- sorted(a) == sorted(b) vs Counter(a) == Counter(b): complexity of each?
- Why is set(a) == set(b) wrong?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a2_t02
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def is_anagram(a: str, b: str) -> bool:
    def count(s: str) -> dict:
        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1
        return counts

    return count(a) == count(b)

print(is_anagram("aab", "abb") )