import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent

# Values come from .env (see .env.example); the defaults keep a fresh clone runnable.
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "https://demoqa.com/")
HEADLESS = os.getenv("HEADLESS", "False") == "True"
SCREENSHOT_DIR = ROOT_DIR / "reports" / "screenshots"
