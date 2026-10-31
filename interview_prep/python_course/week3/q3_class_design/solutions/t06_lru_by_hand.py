class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None) -> None:
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._map = {}
        self._head, self._tail = _Node(), _Node()  # заглушки: head.next — самый старый
        self._head.next, self._tail.prev = self._tail, self._head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node: _Node) -> None:
        node.prev, node.next = self._tail.prev, self._tail
        self._tail.prev.next = node
        self._tail.prev = node

    def get(self, key, default=None):
        node = self._map.get(key)
        if node is None:
            return default
        self._unlink(node)
        self._append(node)
        return node.value

    def put(self, key, value) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._append(node)
            return
        node = _Node(key, value)
        self._map[key] = node
        self._append(node)
        if len(self._map) > self.capacity:
            oldest = self._head.next
            self._unlink(oldest)
            del self._map[oldest.key]

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key) -> bool:
        return key in self._map

    def keys(self) -> list:
        result, node = [], self._head.next
        while node is not self._tail:
            result.append(node.key)
            node = node.next
        return result
