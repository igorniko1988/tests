from behave import then, when


@when("the user requests the profile")
def step_profile(context):
    context.response = context.api.auth.me()


@when("an anonymous client requests the profile")
def step_profile_anonymous(context):
    context.response = context.api.auth.me()


@then("the profile email is the user's email")
def step_profile_email(context):
    assert context.response.json()["email"] == context.credentials["email"], context.response.text
