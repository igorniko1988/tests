 """A2 t03 (required, ~15 min). Group anagrams.

Given a list of words, group the anagrams together.

Requirements:
- Groups are ordered by the first appearance of their first word.
- Words inside a group keep the input order.

Examples:
    group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    group_anagrams([""])  -> [[""]]
    group_anagrams([])    -> []

Follow-up questions:
- What is your dict key and why must it be a tuple or str, not a list?
- Complexity for n words of length up to k?

Run (from interview_prep/python_course/week1_core): uv run pytest -k a2_t03
Теория: interview_prep/python_course/c03_collections/s03_dict/THEORY.md и s04_set/THEORY.md.
"""


def group_anagrams(words: list[str]) -> list[list[str]]:
    raise NotImplementedError
