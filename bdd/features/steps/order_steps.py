from behave import given, then, when

from framework.api.models.order import CreateOrder


@when("the user places a {side} order for {quantity} ETH at {price} USDT")
@given("the user has placed a {side} order for {quantity} ETH at {price} USDT")
def step_place_order(context, side, quantity, price):
    context.response = context.api.orders.create(CreateOrder(side=side, quantity=quantity, price=price))
    if context.response.status_code == 201:
        context.order_id = context.response.json()["id"]


@when('the user places an order with {field} set to "{value}"')
def step_place_invalid_order(context, field, value):
    context.response = context.api.orders.create(CreateOrder(**{field: value}))


@when("the user cancels the order")
def step_cancel(context):
    context.response = context.api.orders.cancel(context.order_id)


@then('the order status is "{status}"')
def step_order_status(context, status):
    assert context.response.json()["status"] == status, context.response.text


@then('the error points to the field "{field}"')
def step_error_field(context, field):
    fields = [d["field"] for d in context.response.json()["error"]["details"]]
    assert field in fields, fields
