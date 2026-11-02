"""C4 t06 (★ optional, ~20 min). Your own memoize.

Implement memoize(func) - your own cache (no functools.cache / lru_cache).
It returns a new function that:
- calls func only once for the same arguments and returns the stored result after that;
- supports positional and keyword arguments: f(1, b=2) and f(1, b=2) hit the cache,
  keyword order does not matter (f(a=1, b=2) == f(b=2, a=1));
- has an attribute `calls` - how many times func was really called.

Arguments are always hashable.

Example:
    @memoize
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    fib(100)      -> 354224848179261915075   (instantly)
    fib.calls     -> 101

Follow-up questions:
- Why must arguments be hashable?
- What is the memory risk of an unbounded cache, and what does lru_cache add?

Run (from interview_prep/python_course/week2/c04_functions): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 6, 9.
"""


def memoize(func):
    raise NotImplementedError
