from playwright.sync_api import Page

from locators.profile_locators import ProfileLocators
from pages.base_page import BasePage


class ProfilePage(BasePage):
    PATH = "profile"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = ProfileLocators(page)

    def open_profile(self) -> None:
        self.open(self.PATH)

    def verify_logged_in_as(self, username: str) -> None:
        self.expect_exact_text(self.locators.username_value, username)

    def verify_not_logged_in(self) -> None:
        self.expect_visible(self.locators.not_logged_in_message)

    def verify_collection(self, titles: list[str]) -> None:
        # Exactly these books, in this order: an extra or missing book fails the check. It waits
        # through the moment the table is still empty, before the books have loaded.
        self.expect_texts(self.locators.collection_titles, titles)

    def delete_book(self, title: str) -> str:
        # Deletes the book through its icon and the confirmation dialog. Returns the text of the
        # alert the site shows afterwards.
        self.locators.delete_book_icon(title).click()
        return self.click_and_accept_alert(self.locators.confirm_delete_button)

    def log_out(self) -> None:
        self.locators.logout_button.click()
