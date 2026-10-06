from behave import given, when, then

from utils.test_data import with_wrong_credentials


@given("the login page is open")
@when("the user opens the login page")
def step_open_login_page(context):
    context.login_page.open_login()


@when("the user logs in with their username and password")
def step_log_in(context):
    context.login_page.log_in(context.user)


@then("the profile shows the user's username")
def step_profile_shows_username(context):
    context.profile_page.verify_logged_in_as(context.user.username)


@when('the user logs in with "{case}"')
def step_log_in_wrong_credentials(context, case):
    context.login_page.log_in(with_wrong_credentials(context.user, case))


@then('the login error "{message}" is shown')
def step_login_error_shown(context, message):
    context.login_page.verify_login_error(message)


@then("the user stays on the login page")
def step_stays_on_login_page(context):
    context.login_page.verify_is_open()


@then("the profile says the user is not logged in")
def step_profile_not_logged_in(context):
    context.profile_page.verify_not_logged_in()


@when("the user logs out")
@when("user {name} logs out")
def step_log_out(context, name=None):
    context.profile_page.log_out()
