class MyQueue:
    def __init__(self) -> None:
        self._inbox = []
        self._outbox = []

    def _move(self) -> None:
        if not self._outbox:
            while self._inbox:
                self._outbox.append(self._inbox.pop())

    def push(self, x) -> None:
        self._inbox.append(x)

    def pop(self):
        self._move()
        if not self._outbox:
            raise IndexError("pop from empty queue")
        return self._outbox.pop()

    def peek(self):
        self._move()
        if not self._outbox:
            raise IndexError("peek from empty queue")
        return self._outbox[-1]

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)
