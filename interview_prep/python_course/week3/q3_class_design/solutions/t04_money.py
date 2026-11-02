from decimal import ROUND_HALF_UP, Decimal
from functools import total_ordering


@total_ordering
class Money:
    __slots__ = ("_amount", "_currency")

    def __init__(self, amount, currency: str) -> None:
        if isinstance(amount, float):
            raise TypeError("money must not be float")
        if not (isinstance(currency, str) and len(currency) == 3 and currency.isalpha()):
            raise ValueError(f"bad currency: {currency!r}")
        object.__setattr__(self, "_amount", Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        object.__setattr__(self, "_currency", currency.upper())

    def __setattr__(self, name, value):
        raise AttributeError("Money is immutable")

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    @classmethod
    def zero(cls, currency: str) -> "Money":
        return cls(0, currency)

    def _same(self, other: "Money") -> None:
        if other.currency != self.currency:
            raise ValueError("currency mismatch")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, k):
        if isinstance(k, bool) or not isinstance(k, (int, Decimal)):
            return NotImplemented
        return Money(self.amount * k, self.currency)

    __rmul__ = __mul__

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same(other)
        return self.amount < other.amount

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    def __repr__(self) -> str:
        return f"Money({str(self.amount)!r}, {self.currency!r})"
