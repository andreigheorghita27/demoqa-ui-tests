from playwright.sync_api import Page

from locators.login_locators import LoginLocators
from pages.base_page import BasePage
from utils.test_data import User


class LoginPage(BasePage):
    PATH = "login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = LoginLocators(page)

    def open_login(self) -> None:
        self.open(self.PATH)

    def log_in(self, user: User) -> None:
        self.locators.username_input.fill(user.username)
        self.locators.password_input.fill(user.password)
        self.locators.login_button.click()

    def start_session(self, cookies: list[dict]) -> None:
        # Logs in without the login page: puts the session cookies (from the API) in the browser.
        self.page.context.add_cookies(cookies)

    def verify_login_error(self, message: str) -> None:
        self.expect_exact_text(self.locators.error_message, message)

    def verify_is_open(self) -> None:
        self.expect_url(self.PATH)
        self.expect_visible(self.locators.form_heading)
