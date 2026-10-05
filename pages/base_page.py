import re
from urllib.parse import urljoin

from playwright.sync_api import Page, Locator, expect

from config import BASE_URL


DEFAULT_TIMEOUT = 5000


class BasePage:
    # Base class for all page objects. Shared Playwright primitives for
    # navigation, interactions and assertions — page objects build business
    # actions on top of these and never re-implement them.

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT)

    # ── Navigation & Wait ──────────────────────────────────────────────────────

    def open(self, path: str = "") -> None:
        # Open a path relative to BASE_URL and wait until the DOM is ready.
        self.page.goto(urljoin(BASE_URL, path), wait_until="domcontentloaded")

    def wait_for_network(self) -> None:
        # Wait for all network requests to finish.
        self.page.wait_for_load_state("networkidle")

    def verify_page_loaded(self, heading_locator: Locator) -> None:
        # Generic page load check: the page heading is visible.
        self.expect_visible(heading_locator)

    # ── Assertions ─────────────────────────────────────────────────────────────

    def expect_visible(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a locator is visible within the given timeout.
        expect(locator).to_be_visible(timeout=timeout)

    def expect_hidden(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a locator is hidden within the given timeout.
        expect(locator).to_be_hidden(timeout=timeout)

    def expect_text(self, locator: Locator, text: str, timeout: int = DEFAULT_TIMEOUT, ignore_case: bool = False) -> None:
        # Assert that a locator contains the given text.
        expect(locator).to_contain_text(text, timeout=timeout, ignore_case=ignore_case)

    def expect_exact_text(self, locator: Locator, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a locator has exactly the given text.
        expect(locator).to_have_text(text, timeout=timeout)

    def expect_texts(self, locator: Locator, texts: list[str], timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a multi-element locator matches exactly these texts, in document order.
        expect(locator).to_have_text(texts, timeout=timeout)

    def expect_count(self, locator: Locator, count: int, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a locator matches exactly `count` elements.
        expect(locator).to_have_count(count, timeout=timeout)

    def expect_value(self, locator: Locator, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that an input locator has the given value.
        expect(locator).to_have_value(value, timeout=timeout)

    def expect_has_class(self, locator: Locator, class_name: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that the element carries `class_name` among its CSS classes.
        expect(locator).to_have_class(re.compile(rf"(^|\s){re.escape(class_name)}(\s|$)"), timeout=timeout)

    def expect_enabled(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a locator is enabled.
        expect(locator).to_be_enabled(timeout=timeout)

    def expect_disabled(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        # Assert that a locator is disabled.
        expect(locator).to_be_disabled(timeout=timeout)

    # ── Input Interactions ─────────────────────────────────────────────────────

    def fill(self, locator: Locator, value: str) -> None:
        # Fill an input field after asserting it is visible.
        self.expect_visible(locator)
        locator.fill(value)

    def clear_and_fill(self, locator: Locator, value: str) -> None:
        # Clear an input field and fill it with a new value.
        self.expect_visible(locator)
        locator.clear()
        locator.fill(value)

    def select_option_by_label(self, selector: str, label: str) -> None:
        # Select a <select> option by its visible label text.
        self.page.select_option(selector, label=label)

    def select_option_by_value(self, selector: str, value: str) -> None:
        # Select a <select> option by its underlying value.
        self.page.select_option(selector, value=value)

    def check_checkbox(self, locator: Locator) -> None:
        # Scroll a checkbox into view and check it.
        locator.scroll_into_view_if_needed()
        locator.check()

    def get_input_value(self, locator: Locator) -> str:
        # Return the current value of an input field.
        return locator.input_value()

    # ── Search ─────────────────────────────────────────────────────────────────

    def search(self, search_input: Locator, search_text: str) -> None:
        # Type the search text into a visible search input.
        self.expect_visible(search_input)
        search_input.fill(search_text)

    def clear_search(self, search_input: Locator) -> None:
        # Clear the search input field.
        self.expect_visible(search_input)
        search_input.clear()

    # ── Form Actions ───────────────────────────────────────────────────────────

    def click_and_submit(self, locator: Locator) -> None:
        # Assert visible, click, and wait for network — covers submit/update/confirm patterns.
        self.expect_visible(locator)
        locator.click()
        self.wait_for_network()

    # ── Table Rows ─────────────────────────────────────────────────────────────

    def click_row_action(self, row_locator: Locator, action_selector: str) -> None:
        # Click an action button (edit, delete…) inside one table row.
        button = row_locator.locator(action_selector)
        self.expect_visible(button)
        button.click()

    def verify_row_visible(self, row_locator: Locator) -> None:
        # Assert that a specific table row is visible.
        self.expect_visible(row_locator)
