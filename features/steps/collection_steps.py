import re

from behave import given, register_type, when, then

from utils.test_data import new_user


def parse_titles(text: str) -> list[str]:
    # One or more quoted book titles: "A", or "A" and "B".
    return re.findall(r'"([^"]+)"', text)


parse_titles.pattern = r'"[^"]+"(?: and "[^"]+")*'  # what {titles:Titles} matches in a step
register_type(Titles=parse_titles)


# Scenarios with more than one user name them ("user A", "user B"); context.users holds them.


@given('user {name} has "{title}" in their collection')
def step_user_with_book(context, name, title):
    context.users[name] = new_user()
    context.api.create_user_with_books(context.users[name], [title])


@given("the user has {titles:Titles} in their collection")
def step_user_with_books(context, titles):
    context.user = new_user()
    context.api.create_user_with_books(context.user, titles)


# Login is tested through the login page in login.feature; other scenarios start logged in
# through the API. It comes after the API setup steps, because a new API token ends the
# browser session (see BookStoreApi.generate_token).
@given("the user is logged in through the API")
def step_logged_in_through_api(context):
    context.login_page.start_session(context.api.session_cookies(context.user))


@given("the profile is open")
@when("the user opens their profile")
def step_open_profile(context):
    context.profile_page.open_profile()


@when('the user deletes "{title}" from their collection')
def step_delete_book(context, title):
    context.alert_message = context.profile_page.delete_book(title)


@when('the user adds "{title}" from the Book Store')
def step_add_book(context, title):
    context.alert_message = context.book_store_page.add_to_collection(title)


@then('the confirmation "{message}" is shown')
def step_confirmation_shown(context, message):
    assert context.alert_message == message, f"Expected the alert {message!r}, got {context.alert_message!r}"


@then('the collection shows only "{title}"')
def step_collection_shows_only(context, title):
    context.profile_page.verify_collection([title])


@when('a book with ISBN "{isbn}" is added through the API')
def step_add_isbn_through_api(context, isbn):
    context.response = context.api.add_isbns(context.user, [isbn])


@then('the request is rejected with "{message}"')
def step_request_rejected(context, message):
    assert context.response.status == 400, f"Expected 400, got {context.response.status}: {context.response.text()}"
    body = context.response.json()
    assert body["message"] == message, f"Expected message {message!r}, got {body}"


@then('the Book Store API has only "{title}" in the user\'s collection')
def step_api_collection(context, title):
    titles = context.api.collection_titles(context.user)
    assert titles == [title], f"Expected only {title!r} in the collection, the API has {titles}"
