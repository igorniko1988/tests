class Wallet:
    """Простой кошелёк, который тестируем сценариями."""

    def __init__(self, balance=0):
        self.balance = balance

    def add(self, amount):
        self.balance += amount

    def spend(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
