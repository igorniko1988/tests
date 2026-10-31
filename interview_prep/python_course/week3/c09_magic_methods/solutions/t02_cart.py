class Cart:
    def __init__(self) -> None:
        self._items = {}

    def add(self, item, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._items[item] = self._items.get(item, 0) + qty

    def remove(self, item) -> None:
        del self._items[item]

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item) -> bool:
        return item in self._items

    def __getitem__(self, item) -> int:
        return self._items[item]

    def __iter__(self):
        return iter(list(self._items.items()))

    def __bool__(self) -> bool:
        return bool(self._items)

    @property
    def total_qty(self) -> int:
        return sum(self._items.values())
