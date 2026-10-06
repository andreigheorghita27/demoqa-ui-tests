from playwright.sync_api import Locator, Page


class ProfileLocators:
    def __init__(self, page: Page) -> None:
        self.page = page
        # The username is shown in a <label> with no accessible role or name, so it is located by id.
        self.username_value = page.locator("#userName-value")
        self.logout_button = page.get_by_role("button", name="Logout", exact=True)
        # Shown instead of the profile when nobody is logged in. Plain text with no role, so it is
        # located by its text; being visible is the check.
        self.not_logged_in_message = page.get_by_text("Currently you are not logged into the Book Store application")
        # In the collection table the only links are the book titles (Delete is an icon, not a link).
        self.collection_titles = page.get_by_role("table").get_by_role("link")
        self.delete_book_dialog = page.get_by_role("dialog", name="Delete Book")
        # exact=True matters here: without it "OK" also matches "Go To Bo(ok) Store" on the page.
        self.confirm_delete_button = self.delete_book_dialog.get_by_role("button", name="OK", exact=True)

    def delete_book_icon(self, title: str) -> Locator:
        # The Delete icon has no role or accessible name, only a "Delete" tooltip (title attribute),
        # so it is found by that tooltip inside the row of the book.
        row = self.page.get_by_role("row").filter(has=self.page.get_by_role("link", name=title, exact=True))
        return row.get_by_title("Delete")
