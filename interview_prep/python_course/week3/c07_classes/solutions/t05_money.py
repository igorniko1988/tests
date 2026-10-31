from decimal import ROUND_HALF_UP, Decimal


class Money:
    def __init__(self, amount, currency: str) -> None:
        if isinstance(amount, float):
            raise TypeError("money must not be float")
        if not (isinstance(currency, str) and len(currency) == 3 and currency.isalpha()):
            raise ValueError(f"bad currency: {currency!r}")
        self._amount = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self._currency = currency.upper()

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def formatted(self) -> str:
        return f"{self._amount} {self._currency}"

    def add(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError(f"cannot add {other.currency} to {self.currency}")
        return Money(self.amount + other.amount, self.currency)
