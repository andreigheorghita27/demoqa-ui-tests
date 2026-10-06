from playwright.sync_api import Page


class LoginLocators:
    def __init__(self, page: Page) -> None:
        self.form_heading = page.get_by_role("heading", name="Login in Book Store")
        self.username_input = page.get_by_role("textbox", name="UserName")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login", exact=True)
        # The error is a <p> with no accessible name. Locating it by its text would make the
        # text check pointless, so it is located by id and its text is checked separately.
        self.error_message = page.locator("#name")
