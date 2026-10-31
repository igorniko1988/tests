"""X3 t01 (20 min, from scratch, no notes). LRU cache.

Implement LRUCache(capacity):
- get(key, default=None) - value or default; a successful get makes the key most recent;
- put(key, value) - insert or update (update also makes it most recent); over capacity ->
  evict the least recently used key;
- len(cache); keys() - keys from least to most recently used;
- capacity < 1 -> ValueError.
get and put must be O(1). You may use collections.OrderedDict.

Example:
    c = LRUCache(2)
    c.put("a", 1); c.put("b", 2); c.get("a"); c.put("c", 3)
    c.keys()  -> ["a", "c"]

Run (from interview_prep/python_course/week3/x3_exam): uv run pytest -k t01
"""


class LRUCache:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError
