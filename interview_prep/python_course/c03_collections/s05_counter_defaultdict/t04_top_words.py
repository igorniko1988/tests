r"""C3 t04 (required, ~15 min). Top K frequent words.

Given a text and an integer k, return the k most frequent words
as a list of (word, count) tuples.

Rules:
- A word is a sequence of letters/digits (the regex \w+ is fine).
  Everything else is a separator: spaces, punctuation, newlines.
- Case-insensitive: "The" and "the" are the same word; return words in lowercase.
- Sort by count descending; TIES are broken alphabetically.
- If there are fewer than k distinct words, return all of them.
- If k <= 0, return an empty list.

Examples:
    top_words("b a b a c", 2)                  -> [("a", 2), ("b", 2)]
    top_words("The cat. the CAT, the dog!", 2) -> [("the", 3), ("cat", 2)]
    top_words("", 3)                           -> []

Follow-up questions:
- Why does Counter(words).most_common(k) fail the first example?
- What is the time complexity of your solution?

Run: uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 5.
"""


def top_words(text: str, k: int) -> list[tuple[str, int]]:
    raise NotImplementedError
