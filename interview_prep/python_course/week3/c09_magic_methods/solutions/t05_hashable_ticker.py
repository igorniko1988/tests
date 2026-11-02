class Ticker:
    def __init__(self, symbol: str, exchange: str) -> None:
        self._symbol = symbol.strip().upper()
        self._exchange = exchange.strip().upper()

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def exchange(self) -> str:
        return self._exchange

    def __eq__(self, other):
        if not isinstance(other, Ticker):
            return NotImplemented
        return (self.symbol, self.exchange) == (other.symbol, other.exchange)

    def __hash__(self) -> int:
        return hash((self.symbol, self.exchange))

    def __repr__(self) -> str:
        return f"Ticker({self.symbol!r}, {self.exchange!r})"
