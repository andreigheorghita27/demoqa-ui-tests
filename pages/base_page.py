from urllib.parse import urljoin

from playwright.sync_api import Page, Locator, expect

from utils.config import BASE_URL


class BasePage:
    # Base class for all page objects: navigation and assertions shared by every page.
    # Clicks and fills are called on the locator directly; Playwright already waits until
    # the element is visible, enabled and able to receive the action.

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open(self, path: str = "") -> None:
        # Open a path relative to BASE_URL and wait until the DOM is ready.
        self.page.goto(urljoin(BASE_URL, path), wait_until="domcontentloaded")

    # ── Interactions ───────────────────────────────────────────────────────────

    def click_and_accept_alert(self, locator: Locator) -> str:
        # Click something that opens a native alert, accept the alert and return its text.
        # Without accepting it the page stays blocked.
        with self.page.expect_event("dialog") as dialog_info:
            locator.click()
        dialog = dialog_info.value
        message = dialog.message
        dialog.accept()
        return message

    # ── Assertions ─────────────────────────────────────────────────────────────

    def expect_url(self, path: str) -> None:
        # Assert that the page is at a path relative to BASE_URL.
        expect(self.page).to_have_url(urljoin(BASE_URL, path))

    def expect_visible(self, locator: Locator) -> None:
        # Assert that a locator is visible.
        expect(locator).to_be_visible()

    def expect_exact_text(self, locator: Locator, text: str) -> None:
        # Assert that a locator has exactly the given text.
        expect(locator).to_have_text(text)

    def expect_texts(self, locator: Locator, texts: list[str]) -> None:
        # Assert that a locator matches exactly these elements, with these texts, in this order.
        expect(locator).to_have_text(texts)
