"""C3 t02 ★ (optional, ~30 min). Implement a hash map.

Implement a simple hash map WITHOUT using the built-in dict or set.
Use separate chaining: self._buckets is a list of buckets, each bucket is a list
of [key, value] pairs.

    bucket index = hash(key) % len(self._buckets)

Implement:
- HashMap() - starts with 8 buckets (self._buckets is a list of length 8).
- put(key, value) - insert the pair; if the key already exists, overwrite the value.
- get(key, default=None) - return the value for key, or default if it is missing.
- remove(key) - delete the key and return its value; raise KeyError(key) if missing.
- len(m) - number of stored pairs.
- key in m - whether the key is present.

Resizing: after inserting a NEW key, if size > 0.75 * number of buckets,
double the number of buckets and rehash all pairs.
Unhashable keys (e.g. a list) must raise TypeError, like dict does.

Example:
    m = HashMap()
    m.put("a", 1)
    m.put("a", 2)
    m.get("a")       -> 2
    len(m)           -> 1
    m.get("zzz", 0)  -> 0
    m.remove("a")    -> 2
    "a" in m         -> False
    # after 7 distinct keys there are 16 buckets (7 > 0.75 * 8)

Follow-up questions:
- Why is lookup O(1) on average but O(n) in the worst case?
- What breaks if a key is mutated after it was put into the map?

Run: uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 3.
"""


class HashMap:
    def __init__(self) -> None:
        self._buckets: list[list] = [[] for _ in range(8)]
        self._size = 0

    def put(self, key, value) -> None:
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, key) -> bool:
        raise NotImplementedError
