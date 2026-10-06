from playwright.sync_api import Page

from locators.book_store_locators import BookStoreLocators
from pages.base_page import BasePage


class BookStorePage(BasePage):
    PATH = "books"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = BookStoreLocators(page)

    def add_to_collection(self, title: str) -> str:
        # Opens the book from the list and adds it. Returns the text of the alert the site shows.
        self.open(self.PATH)
        self.locators.book_link(title).click()
        return self.click_and_accept_alert(self.locators.add_to_collection_button)
