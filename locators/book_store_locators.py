from playwright.sync_api import Locator, Page


class BookStoreLocators:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.add_to_collection_button = page.get_by_role("button", name="Add To Your Collection", exact=True)

    def book_link(self, title: str) -> Locator:
        # In the book list every title is a link to the book's page.
        return self.page.get_by_role("link", name=title, exact=True)
