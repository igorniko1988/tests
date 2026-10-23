from behave import given, then, when

from pages.login_page import LoginPage


@given("I am on the login page")
def step_open_login(context):
    context.page = LoginPage(context.driver, context.base_url).open_page()


@when('I log in as "{user}" with password "{password}"')
def step_login(context, user, password):
    context.page.login(user, password)


@then('I see the message "{message}"')
def step_message(context, message):
    assert context.page.message() == message
