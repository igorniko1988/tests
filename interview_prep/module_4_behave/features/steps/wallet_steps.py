from behave import given, then, when

from app.wallet import Wallet


@given("a wallet with balance {balance:d}")
def step_wallet(context, balance):
    context.wallet = Wallet(balance)


@when("I spend {amount:d}")
def step_spend(context, amount):
    context.result = context.wallet.spend(amount)


@when("I add {amount:d}")
def step_add(context, amount):
    context.wallet.add(amount)


@when("I make the following payments:")
def step_payments(context):
    for row in context.table:
        context.wallet.spend(int(row["amount"]))


@then("the payment is accepted")
def step_accepted(context):
    assert context.result is True, "payment was declined"


@then("the payment is declined")
def step_declined(context):
    assert context.result is False, "payment was accepted"


@then("the balance is {expected:d}")
def step_balance(context, expected):
    assert context.wallet.balance == expected, (
        f"expected balance {expected}, got {context.wallet.balance}"
    )
