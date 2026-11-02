class RequestLog:
    def __init__(self, name: str) -> None:
        self.name = name
        self.entries = []  # свой список у каждого объекта

    def add(self, method: str, path: str) -> None:
        self.entries.append(f"{method} {path}")

    def clear(self) -> None:
        self.entries.clear()
