"""A7 t06 (required, ~25 min). Koko eating bananas (search on the answer).

piles[i] bananas are in pile i. Each hour Koko picks one pile and eats up to k bananas from it
(if the pile has fewer, she finishes it and waits for the next hour). Return the minimum
integer speed k so that she eats everything within h hours (h >= len(piles)).

Requirements:
- O(n * log(max(piles))).

Examples:
    min_eating_speed([3, 6, 7, 11], 8)        -> 4
    min_eating_speed([30, 11, 23, 4, 20], 5)  -> 30
    min_eating_speed([30, 11, 23, 4, 20], 6)  -> 23

Follow-up questions:
- Why is "speed k is enough" monotonic in k?
- What are lo and hi of the search and why?

Run (from interview_prep/python_course/week3/a07_binary_search): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 3.
"""


def min_eating_speed(piles: list[int], h: int) -> int:
    raise NotImplementedError
