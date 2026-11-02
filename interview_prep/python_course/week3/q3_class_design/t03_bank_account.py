"""Q3 t03 (required, ~25 min). Bank account with history and custom exceptions.

Implement:

- exceptions: BankError(Exception); InsufficientFunds(BankError) with attributes balance and
  amount; AccountClosed(BankError);
- Account(owner): balance starts at Decimal("0.00");
- deposit(amount), withdraw(amount): amount is str/int/Decimal (float -> TypeError),
  must be > 0 (else ValueError); withdraw more than the balance -> InsufficientFunds;
  any operation on a closed account -> AccountClosed;
- balance - read-only property (Decimal, 2 places);
- history - list of tuples ("deposit" | "withdraw", Decimal amount) of SUCCESSFUL operations;
  return a copy, so callers cannot change the real history;
- close(): only with zero balance (else BankError("balance must be zero")).

Example:
    acc = Account("ann")
    acc.deposit("100"); acc.withdraw(30)
    acc.balance   -> Decimal("70.00")
    acc.withdraw(100)   -> InsufficientFunds(balance=70.00, amount=100)
    acc.history   -> [("deposit", Decimal("100")), ("withdraw", Decimal("30"))]

Follow-up questions:
- Why a hierarchy of exceptions and attributes instead of one Exception with a message?
- Which invariants does the class keep?

Run (from interview_prep/python_course/week3/q3_class_design): uv run pytest -k t03
Теория: THEORY.md в этой папке, раздел 4.
"""


from decimal import Decimal  # noqa: F401


class BankError(Exception):
    pass


class Account:
    def __init__(self, owner: str) -> None:
        raise NotImplementedError
