"""Q3 t01 (required, ~25 min). LRU cache.

Implement LRUCache(capacity) - a cache that evicts the least recently used key:

- get(key, default=None) - value or default; a successful get makes the key most recent;
- put(key, value) - insert or update (an update also makes the key most recent); when the size
  goes over capacity, evict the least recently used key;
- len(cache), key in cache (the `in` check does NOT change recency);
- keys() - keys from least to most recently used;
- capacity < 1 -> ValueError.

Requirements:
- get and put in O(1). Tests do 200 000 operations.

Example:
    c = LRUCache(2)
    c.put("a", 1); c.put("b", 2)
    c.get("a")        -> 1          # now "b" is the oldest
    c.put("c", 3)                   # evicts "b"
    c.keys()          -> ["a", "c"]
    c.get("b")        -> None

Follow-up questions:
- Why is OrderedDict a good fit? What would you build without it?
- How is this related to functools.lru_cache?

Run (from interview_prep/python_course/week3_core): uv run pytest -k q3_t01
Теория: THEORY.md в этой папке, раздел 2.
"""


class LRUCache:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError
