from decimal import Decimal

from behave import given, then, when

from framework.api.models.order import CreateOrder


@given("the user has deposited {amount} {asset}")
def step_deposit(context, amount, asset):
    response = context.api.balances.deposit(asset, amount)
    assert response.status_code == 200, response.text


@given("the user has placed a {side} order for {quantity} ETH at {price} USDT")
@when("the user places a {side} order for {quantity} ETH at {price} USDT")
def step_place_order(context, side, quantity, price):
    context.response = context.api.orders.create(CreateOrder(side=side, quantity=quantity, price=price))
    if context.response.status_code == 201:
        context.order_id = context.response.json()["id"]   # нужен шагу отмены


@when('the user places an order with {field} set to "{value}"')
def step_place_invalid_order(context, field, value):
    context.response = context.api.orders.create(CreateOrder(**{field: value}))


@when("the user cancels the order")
def step_cancel(context):
    context.response = context.api.orders.cancel(context.order_id)


@then('the order status is "{status}"')
def step_order_status(context, status):
    assert context.response.json()["status"] == status, context.response.text


@then("the {asset} balance is {available} available and {locked} locked")
def step_balance(context, asset, available, locked):
    balances = {b["asset"]: b for b in context.api.balances.get_balance().json()}
    assert Decimal(balances[asset]["available"]) == Decimal(available), balances[asset]
    assert Decimal(balances[asset]["locked"]) == Decimal(locked), balances[asset]


@then('the error points to the field "{field}"')
def step_error_field(context, field):
    fields = [d["field"] for d in context.response.json()["error"]["details"]]
    assert field in fields, fields
