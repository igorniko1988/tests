# Решение задания refund (не открывать до решения)

app/wallet.py, добавить метод:

    def refund(self, amount):
        self.balance += amount

features/steps/wallet_steps.py, добавить шаг:

    @when("I refund {amount:d}")
    def step_refund(context, amount):
        context.wallet.refund(amount)
