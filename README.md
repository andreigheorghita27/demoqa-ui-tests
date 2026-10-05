# demoqa-ui-tests

UI test suite for https://demoqa.com/ — Behave + Playwright (Python), Page Object Model.

## Structure

```
.
├── behave.ini
├── requirements.txt
├── .env.example          # copy to .env (gitignored)
├── features/
│   ├── environment.py    # hooks: browser per run, fresh context per scenario, screenshot on failure
│   ├── config.py         # BASE_URL, HEADLESS — read from .env
│   ├── *.feature
│   └── steps/            # thin steps: one call into a page object
└── pages/
    ├── base_page.py      # shared Playwright helpers (fill, expect_*, waits)
    ├── locators.py       # every selector, one class per page
    └── *_page.py         # one page object per screen
```

## Setup

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m playwright install chromium
cp .env.example .env
```

## Run

```bash
behave                          # all features
behave features/<name>.feature  # one feature
behave --tags=@<tag>            # by tag
```

Set `HEADLESS=True` in `.env` for a headless run.
