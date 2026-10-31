"""C5 t04 (required, ~20 min). Iterator class over a paginated API.

An API returns items page by page: fetch_page(page) returns a list of items for
page 1, 2, 3, ... and an EMPTY list after the last page.

Implement a class Paginator(fetch_page) that is an ITERATOR over all items of all
pages, written with __iter__ and __next__ (not a generator function).

Requirements:
- Pages are requested lazily: page k + 1 only when items of page k are used up.
- Stop (StopIteration) at the first empty page; do not request pages after it.
- Attribute pages_fetched: how many times fetch_page was called.

Example:
    data = {1: ["a", "b"], 2: ["c"]}
    p = Paginator(lambda page: data.get(page, []))
    next(p)            -> "a"      (pages_fetched == 1)
    list(p)            -> ["b", "c"]
    p.pages_fetched    -> 3        (pages 1, 2 and the empty 3)

Follow-up questions:
- Why does __iter__ return self?
- Rewrite it as a generator function - how many lines did you save?

Run (from interview_prep/python_course/week2/c05_generators): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 3.
"""


class Paginator:
    def __init__(self, fetch_page) -> None:
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError
