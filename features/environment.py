import sys
from pathlib import Path

# Make `pages` and `config` importable whichever directory behave is started from.
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT_DIR), str(ROOT_DIR / "features")]

from playwright.sync_api import sync_playwright  # noqa: E402

from config import HEADLESS, SCREENSHOT_DIR  # noqa: E402
# Page objects: from pages.<module>_page import <Name>Page  # noqa: E402


def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=HEADLESS)


def before_scenario(context, scenario):
    # A fresh browser context per scenario: no cookies or storage leak between scenarios.
    context.browser_context = context.browser.new_context(viewport={"width": 1920, "height": 1080})
    context.page = context.browser_context.new_page()
    # Page objects, alphabetical: context.<name>_page = <Name>Page(context.page)


def after_step(context, step):
    if step.status == "failed":
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        name = "".join(c if c.isalnum() else "_" for c in context.scenario.name)
        context.page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"), full_page=True)


def after_scenario(context, scenario):
    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
