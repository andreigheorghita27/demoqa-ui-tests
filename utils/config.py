import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent  # utils/ -> project root

# Values come from an optional .env (see the README); the defaults keep a fresh clone runnable.
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "https://demoqa.com/")
HEADLESS = os.getenv("HEADLESS", "False") == "True"
# How long actions (click, fill, goto) and expect checks wait before failing, in milliseconds.
# The site is a slow shared demo, so the default is above Playwright's 5 seconds.
TIMEOUT_MS = int(os.getenv("TIMEOUT_MS", "10000"))
SCREENSHOT_DIR = ROOT_DIR / "reports" / "screenshots"

# The only hosts the browser may load from; every other request is blocked. An allowlist, not a
# list of ad networks, so a new ad or tracking network is blocked without anyone adding it here.
# Besides the site itself, it needs google.com and gstatic.com for reCAPTCHA and fonts
# (checked 2026-10-06). Subdomains are included: "gstatic.com" also allows fonts.gstatic.com.
ALLOWED_HOSTS = (
    urlparse(BASE_URL).hostname,
    "google.com",
    "gstatic.com",
)

# CSS hidden on every page: the fixed footer stays over the bottom of the page and can cover
# elements there.
HIDDEN_ELEMENTS_CSS = "footer { display: none !important; }"
