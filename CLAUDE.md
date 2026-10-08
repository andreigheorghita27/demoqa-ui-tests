# CLAUDE.md

UI test suite for https://demoqa.com/ (Book Store Application) — Behave + Playwright
(Python, sync API), Page Object Model. The test plan is in `docs/test-plan.md`.

## Structure

```
.
├── .github/workflows/    # CI: tests on push, pull requests and weekly; dependency audit
├── behave.ini
├── requirements.txt
├── .env                  # optional local settings (gitignored); read by utils/config.py
├── docs/                 # test-plan, test-cases, known-bugs, ai-test-strategy (.md)
├── features/
│   ├── environment.py    # hooks: browser per run, fresh context per scenario, screenshot on failure
│   ├── *.feature
│   └── steps/            # thin steps: one call into a page object
├── pages/
│   ├── base_page.py      # shared helpers (open, alerts, expect_*)
│   └── *_page.py         # one page object per screen, inherits BasePage
├── locators/
│   └── *_locators.py     # one locator class per page, role-first
└── utils/
    ├── config.py         # BASE_URL, HEADLESS, TIMEOUT_MS, SCREENSHOT_DIR from .env
    ├── api.py            # Book Store API client: users, books, session cookies
    └── test_data.py      # unique test users
```

## Layers and rules

- **Feature files** describe behaviour in business language. No selectors, no URLs
  beyond page names.
- **Steps** are thin: each step calls one page-object method. No Playwright calls
  and no locators in steps.
- **No duplicate steps.** Before writing a step, search `features/steps/` for one that
  already does the same thing and reuse it. When the same action needs a `Given` and a
  `When` wording, stack both decorators on one function instead of writing two.
- **Page objects** (`pages/<name>_page.py`, class `<Name>Page(BasePage)`) hold the
  business actions and checks. They take locators from `locators/`, act on them
  directly (`locator.click()`, `locator.fill()`, which wait on their own) and check
  through the `BasePage` helpers.
- **`BasePage` stays small.** Add a helper only when a page object needs it now; remove
  helpers nobody uses. No wrappers around actions such as `click` or `fill`: Playwright
  already waits for the element. The `expect_*` checks are the exception, because all
  checks go through them.
- **Locators** (`locators/<name>_locators.py`, class `<Name>Locators`) are the only
  place selectors are written. Each class takes `page` in `__init__` and builds
  attributes with `page.get_by_role(...)`. Fallback order when there is no usable
  role/name: `get_by_label` > `get_by_placeholder` > `get_by_text` >
  `get_by_test_id` > CSS, with a comment explaining why.
- **Config** comes only from `utils/config.py`. Never read `os.environ` elsewhere,
  never hard-code the base URL.
- New page object: import it in `features/environment.py` and attach it in
  `before_scenario` as `context.<name>_page` (alphabetical).
- Checks on the page use Playwright `expect` (via `BasePage.expect_*`), which waits
  until the condition is met. No `time.sleep`, no `wait_for_timeout`.
- Plain `assert` only for values that are already known and cannot change by waiting:
  API responses (exact status code, body fields) and Python values. Always give it a
  message that shows the actual value.

## Test data isolation

Every scenario owns its data. No shared or fixed test accounts, no scenario depends on
another one or on the order they run in.

- **Own user per scenario.** Each scenario creates a fresh user through the API
  (`context.api.create_user(new_user())`). Usernames are unique (`utils/test_data.py`).
- **Logged-in scenarios**: API register, then the step "the user is logged in through the
  API" puts the session cookies in the browser. It comes after every other API setup step,
  because each new API token ends the browser session. The UI is never used for setup.
- **Login scenarios** (valid login, wrong password, wrong username, ...): API register only.
  The login itself is what is being tested, so it happens through the UI.
- **Registration scenarios**: the scenario creates the user itself, as the step under test.
- **Cleanup.** Every user created through `BookStoreApi` is deleted in `after_scenario`,
  also when the scenario fails. Nothing is left on the shared site.
- **Fresh browser context per scenario**: no cookies or storage carry over.

## Known bugs

- A test that fails because of a site bug keeps checking the correct behaviour; it is never
  changed to pass on the wrong one.
- Tag it `@known_bug` (for one case of a Scenario Outline, use a separate tagged `Examples`
  block) with a comment naming the bug ID, and describe the bug in `docs/known-bugs.md`.
- `behave.ini` skips `@known_bug` by default; `behave --tags=@known_bug` runs them.

## Commands

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m playwright install chromium

.venv/Scripts/behave                          # all features
.venv/Scripts/behave features/<name>.feature  # one feature
.venv/Scripts/behave --tags=@<tag>            # by tag
```

## Repo hygiene

- Code, comments, docs and commit messages are in English.
- Never commit `.env` or credentials. There is no `.env.example`: the settings and their
  defaults are listed in the README, and `utils/config.py` works without a `.env`.
