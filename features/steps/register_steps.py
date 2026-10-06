from behave import given, when, then

from utils.test_data import new_user


@given("a user that is already registered")
def step_registered_user(context):
    context.user = new_user()
    context.api.register(context.user)


@when("the user is registered through the API")
def step_register_through_api(context):
    context.response = context.api.create_user(context.user)


@then('the registration is rejected with "{message}"')
def step_registration_rejected(context, message):
    assert context.response.status == 406, f"Expected 406, got {context.response.status}: {context.response.text()}"
    body = context.response.json()
    assert body["message"] == message, f"Expected message {message!r}, got {body}"
