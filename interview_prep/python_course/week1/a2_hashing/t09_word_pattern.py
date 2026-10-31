"""A2 t09 (★ optional, ~15 min). Word pattern.

Given a pattern of letters and a string of words separated by single spaces,
return True if the words follow the pattern (a one-to-one mapping between
letters and words).

Examples:
    word_pattern("abba", "dog cat cat dog")   -> True
    word_pattern("abba", "dog cat cat fish")  -> False
    word_pattern("aaaa", "dog cat cat dog")   -> False
    word_pattern("abba", "dog dog dog dog")   -> False
    word_pattern("ab", "dog")                 -> False

Follow-up questions:
- Which check catches "abba" vs "dog dog dog dog"?

Run (from interview_prep/python_course/week1/a2_hashing): uv run pytest -k t09
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def word_pattern(pattern: str, s: str) -> bool:
    raise NotImplementedError
