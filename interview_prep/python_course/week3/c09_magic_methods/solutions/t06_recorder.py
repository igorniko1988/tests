class Recorder:
    def __init__(self, path: str = "", root: "Recorder | None" = None) -> None:
        self._path = path
        self._root = root or self
        if root is None:
            self.calls = []
            self.returns = {}

    def __getattr__(self, name: str) -> "Recorder":
        # вызывается только если обычный поиск атрибута не нашёл имя
        if name.startswith("__"):
            raise AttributeError(name)
        path = f"{self._path}.{name}" if self._path else name
        return Recorder(path, self._root)

    def __call__(self, *args, **kwargs):
        self._root.calls.append((self._path, args, kwargs))
        return self._root.returns.get(self._path)
