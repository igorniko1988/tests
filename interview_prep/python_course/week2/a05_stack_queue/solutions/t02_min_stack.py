class MinStack:
    def __init__(self) -> None:
        self._items = []  # пары (значение, минимум на момент добавления)

    def push(self, x) -> None:
        current_min = min(x, self._items[-1][1]) if self._items else x
        self._items.append((x, current_min))

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()[0]

    def top(self):
        if not self._items:
            raise IndexError("top from empty stack")
        return self._items[-1][0]

    def get_min(self):
        if not self._items:
            raise IndexError("min of empty stack")
        return self._items[-1][1]

    def __len__(self) -> int:
        return len(self._items)
