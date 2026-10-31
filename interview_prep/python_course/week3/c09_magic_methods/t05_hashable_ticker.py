"""C9 t05 (required, ~15 min). Your objects in a set.

Implement a class Ticker(symbol, exchange) used as a dict key and in sets:
- symbol and exchange are compared case-insensitively and ignoring spaces around:
  Ticker(" btc ", "Binance") == Ticker("BTC", "binance");
- equal tickers have equal hashes, so a set keeps only one of them;
- symbol and exchange are READ-ONLY (assignment -> AttributeError), because a hash
  must not change while the object is in a set;
- repr -> "Ticker('BTC', 'BINANCE')" (stored upper case).

Example:
    {Ticker("btc", "binance"), Ticker("BTC", "Binance"), Ticker("ETH", "binance")}  -> 2 items
    prices = {Ticker("BTC", "binance"): 100}
    prices[Ticker(" btc", "BINANCE")]   -> 100

Follow-up questions:
- What would happen if symbol could be changed after adding the ticker to a set?

Run (from interview_prep/python_course/week3/c09_magic_methods): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 2.
"""


class Ticker:
    def __init__(self, symbol: str, exchange: str) -> None:
        raise NotImplementedError
