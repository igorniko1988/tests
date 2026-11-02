class HashMap:
    def __init__(self) -> None:
        self._buckets: list[list] = [[] for _ in range(8)]
        self._size = 0

    def _bucket(self, key) -> list:
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value  # ключ уже есть — только меняем значение
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._resize()

    def _resize(self) -> None:
        old = self._buckets
        self._buckets = [[] for _ in range(len(old) * 2)]
        for bucket in old:
            for key, value in bucket:
                # размер изменился → у ключа другой номер корзины
                self._bucket(key).append([key, value])

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return v
        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key) -> bool:
        return any(k == key for k, _ in self._bucket(key))
