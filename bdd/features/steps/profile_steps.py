from behave import given, then, when

from framework.data.generators import credentials


@given("a registered user")
def step_registered_user(context):
    context.credentials = credentials()                  # в context: email нужен шагу Then
    context.api.auth.register(**context.credentials)
    login = context.api.auth.login(**context.credentials)  # локально: нужен только здесь
    context.api.client.set_token(login.json()["access_token"])


@when("the user requests the profile")
def step_request_profile(context):
    context.response = context.api.auth.me()


@when("an anonymous client requests the profile")
def step_request_profile_anonymous(context):
    context.response = context.api.auth.me()             # токена нет: никто не логинился


@then("the response status is {status:d}")
def step_check_status(context, status):
    assert context.response.status_code == status, context.response.text


@then("the profile email is the user's email")
def step_check_email(context):
    assert context.response.json()["email"] == context.credentials["email"], context.response.text
