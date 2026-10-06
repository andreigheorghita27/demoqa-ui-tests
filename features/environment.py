import sys
from pathlib import Path
from urllib.parse import urlparse

# Make `pages`, `locators` and `utils` importable whichever directory behave is started from.
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from playwright.sync_api import Route, expect, sync_playwright  # noqa: E402

from utils.api import BookStoreApi  # noqa: E402
from utils.config import (  # noqa: E402
    ALLOWED_HOSTS,
    BASE_URL,
    HEADLESS,
    HIDDEN_ELEMENTS_CSS,
    SCREENSHOT_DIR,
    TIMEOUT_MS,
)
from pages.book_store_page import BookStorePage  # noqa: E402
from pages.login_page import LoginPage  # noqa: E402
from pages.profile_page import ProfilePage  # noqa: E402

# Adds HIDDEN_ELEMENTS_CSS to every page as soon as its <head> exists.
HIDE_ELEMENTS_SCRIPT = f"""
document.addEventListener("DOMContentLoaded", () => {{
    const style = document.createElement("style");
    style.textContent = {HIDDEN_ELEMENTS_CSS!r};
    document.head.appendChild(style);
}});
"""


def is_allowed(host: str) -> bool:
    return any(host == allowed or host.endswith("." + allowed) for allowed in ALLOWED_HOSTS)


def block_third_parties(route: Route) -> None:
    # Ads and trackers are blocked by not being on the allowlist (see ALLOWED_HOSTS).
    if is_allowed(urlparse(route.request.url).hostname or ""):
        route.continue_()
    else:
        route.abort()


def before_all(context):
    # expect has its own timeout, separate from the page's action timeout set in before_scenario.
    expect.set_options(timeout=TIMEOUT_MS)
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=HEADLESS)
    context.api = BookStoreApi(context.playwright.request.new_context(base_url=BASE_URL))


def before_scenario(context, scenario):
    # A fresh browser context per scenario: no cookies or storage leak between scenarios.
    context.browser_context = context.browser.new_context(viewport={"width": 1920, "height": 1080})
    context.browser_context.route("**/*", block_third_parties)
    context.browser_context.add_init_script(HIDE_ELEMENTS_SCRIPT)
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(TIMEOUT_MS)
    context.users = {}  # named users ("A", "B") in scenarios with more than one
    # Page objects, alphabetical.
    context.book_store_page = BookStorePage(context.page)
    context.login_page = LoginPage(context.page)
    context.profile_page = ProfilePage(context.page)


def after_step(context, step):
    if step.status == "failed":
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        name = "".join(c if c.isalnum() else "_" for c in context.scenario.name)
        context.page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"), full_page=True)


def after_scenario(context, scenario):
    # The browser context is closed even when the cleanup fails.
    try:
        context.api.delete_created_users()
    finally:
        context.browser_context.close()


def after_all(context):
    # before_all may have stopped half-way (missing browser, Ctrl+C): close only what was started,
    # so its error is the one that gets reported.
    if hasattr(context, "api"):
        context.api.request.dispose()
    if hasattr(context, "browser"):
        context.browser.close()
    if hasattr(context, "playwright"):
        context.playwright.stop()
