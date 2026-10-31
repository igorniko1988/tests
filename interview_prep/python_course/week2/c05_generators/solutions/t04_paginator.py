class Paginator:
    def __init__(self, fetch_page) -> None:
        self._fetch_page = fetch_page
        self._page = 0
        self._buffer = []
        self._done = False
        self.pages_fetched = 0

    def __iter__(self):
        return self

    def __next__(self):
        while not self._buffer:
            if self._done:
                raise StopIteration
            self._page += 1
            self.pages_fetched += 1
            items = self._fetch_page(self._page)
            if not items:
                self._done = True
                raise StopIteration
            self._buffer = list(items)
        return self._buffer.pop(0)
