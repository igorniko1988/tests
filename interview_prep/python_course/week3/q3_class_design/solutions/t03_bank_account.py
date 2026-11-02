from decimal import Decimal


class BankError(Exception):
    pass


class InsufficientFunds(BankError):
    def __init__(self, balance: Decimal, amount: Decimal) -> None:
        super().__init__(f"balance {balance} is less than {amount}")
        self.balance = balance
        self.amount = amount


class AccountClosed(BankError):
    pass


class Account:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self._balance = Decimal("0.00")
        self._history = []
        self._closed = False

    @staticmethod
    def _money(amount) -> Decimal:
        if isinstance(amount, float):
            raise TypeError("amount must not be float")
        value = Decimal(amount)
        if value <= 0:
            raise ValueError("amount must be positive")
        return value

    def _check_open(self) -> None:
        if self._closed:
            raise AccountClosed(self.owner)

    def deposit(self, amount) -> None:
        self._check_open()
        value = self._money(amount)
        self._balance += value
        self._history.append(("deposit", value))

    def withdraw(self, amount) -> None:
        self._check_open()
        value = self._money(amount)
        if value > self._balance:
            raise InsufficientFunds(self.balance, value)
        self._balance -= value
        self._history.append(("withdraw", value))

    @property
    def balance(self) -> Decimal:
        return self._balance.quantize(Decimal("0.01"))

    @property
    def history(self) -> list:
        return list(self._history)

    def close(self) -> None:
        self._check_open()
        if self._balance != 0:
            raise BankError("balance must be zero")
        self._closed = True
