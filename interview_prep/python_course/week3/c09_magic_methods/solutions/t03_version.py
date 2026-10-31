from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, text: str) -> None:
        parts = text.split(".")
        if not all(p.isdigit() for p in parts):
            raise ValueError(f"invalid version: {text!r}")
        self.text = text
        numbers = [int(p) for p in parts]
        while len(numbers) > 1 and numbers[-1] == 0:
            numbers.pop()  # 1.2.0 == 1.2: хвостовые нули не важны
        self.key = tuple(numbers)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.key == other.key

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.key < other.key

    def __hash__(self) -> int:
        return hash(self.key)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"Version({self.text!r})"
