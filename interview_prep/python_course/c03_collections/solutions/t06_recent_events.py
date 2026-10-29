from collections import deque


class RecentEvents:
    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError("n must be >= 1")
        self._events = deque(maxlen=n)
        self._total = 0

    def add(self, event) -> None:
        self._events.append(event)  # при переполнении старое событие выпадет слева
        self._total += 1

    def items(self) -> list:
        return list(self._events)

    @property
    def total(self) -> int:
        return self._total

    def __len__(self) -> int:
        return len(self._events)
