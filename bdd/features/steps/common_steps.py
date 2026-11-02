"""Общие шаги: пользователь, деньги, статус ответа. Один шаг — одна строчка Gherkin."""

from decimal import Decimal

from behave import given, then

from framework.data.generators import credentials


@given("a registered user")
def step_registered_user(context):
    context.credentials = credentials()
    context.api.auth.register(**context.credentials)
    login = context.api.auth.login(**context.credentials)
    assert login.status_code == 200, login.text
    context.api.client.set_token(login.json()["access_token"])


@given("the user has deposited {amount} {asset}")
def step_deposit(context, amount, asset):
    response = context.api.balances.deposit(asset, amount)
    assert response.status_code == 200, response.text


@then("the response status is {status:d}")
def step_status(context, status):
    assert context.response.status_code == status, (
        f"expected {status}, got {context.response.status_code}: {context.response.text}"
    )


@then("the {asset} balance is {available} available and {locked} locked")
def step_balance(context, asset, available, locked):
    balances = {b["asset"]: b for b in context.api.balances.get_balance().json()}
    assert Decimal(balances[asset]["available"]) == Decimal(available), balances[asset]
    assert Decimal(balances[asset]["locked"]) == Decimal(locked), balances[asset]
