"""C5 t03 (required, ~15 min). Split a stream into batches.

Implement a generator batched(iterable, n) that yields lists of n items;
the last batch may be shorter.

Requirements:
- Works with any iterable, including generators and infinite iterators
  (take items one by one - no len(), no slicing of the input).
- n < 1 raises ValueError on the call.
- Do not use itertools.batched.

Examples:
    list(batched([1, 2, 3, 4, 5], 2))   -> [[1, 2], [3, 4], [5]]
    list(batched("abc", 3))             -> [["a", "b", "c"]]
    list(batched([], 2))                -> []

Follow-up questions:
- Why can't you use len(iterable) here?
- Where would you use it in API tests? (Hint: bulk endpoints with a size limit.)

Run (from interview_prep/python_course/week2_core): uv run pytest -k c05_t03
Теория: THEORY.md в этой папке, раздел 4, 8.
"""


def batched(iterable, n):
    raise NotImplementedError
