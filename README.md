# demoqa-ui-tests

Tests for the Book Store Application on https://demoqa.com/: UI tests with Behave + Playwright
(Python, Page Object Model) and API checks on the Book Store API.

## Deliverables

| Part | Where |
|---|---|
| Test plan | [docs/test-plan.md](docs/test-plan.md) |
| Test cases (Gherkin) | [docs/test-cases.md](docs/test-cases.md) |
| Automated tests | [features/](features/) (`register.feature`, `login.feature`, `collection.feature`) |
| Bugs found | [docs/known-bugs.md](docs/known-bugs.md) |
| Test strategy for an AI feature | *(to do)* |
| AI usage statement | [below](#ai-usage) |

## Structure

```
.
├── behave.ini            # behave settings; skips @known_bug by default
├── requirements.txt
├── docs/                 # test plan, test cases, known bugs
├── features/
│   ├── environment.py    # hooks: browser, fresh context per scenario, ad blocking, cleanup
│   ├── *.feature
│   └── steps/            # thin steps: one call into a page object
├── pages/                # one page object per screen, on top of base_page.py
├── locators/             # one locator class per page, role-first
└── utils/
    ├── config.py         # settings, read from an optional .env
    ├── api.py            # Book Store API client: users, books, session cookies
    └── test_data.py      # a unique user per scenario
```

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows; Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Optional settings go in a `.env` file in the project root; without it the defaults are used.

| Setting | Default | Meaning |
|---|---|---|
| `BASE_URL` | `https://demoqa.com/` | Site under test |
| `HEADLESS` | `False` | `True` runs the browser without a window |
| `TIMEOUT_MS` | `10000` | How long actions and checks wait before failing |

## Run

```bash
behave                          # all features
behave features/login.feature   # one feature
behave --tags=@known_bug        # only the tests for known bugs
```

Tests that fail because of a bug in [docs/known-bugs.md](docs/known-bugs.md) are tagged
`@known_bug` and skipped by default, so a red run always means something new broke. They keep
checking the correct behaviour and are expected to fail until the site is fixed.

## AI usage

I used Claude (Claude Code) throughout: I made the decisions and checked its work; Claude drafted, coded and double-checked.

- **Exploration:** I explored the site myself (16 checks) and also had Claude explore it; from that I chose the main flow, which became the test cases.
- **Rules:** I wrote `CLAUDE.md` with the project rules (layers, locators, waits, data isolation) and checked the code against them as Claude wrote it.
- **Plan and cases:** I set the scope and risk order and added key cases (data isolation, deleting a book, an invalid ISBN). Claude wrote them up; I had it remove what was out of scope for a short plan.
- **What I cut:** Claude's `BasePage` was too much code to read; I had it cut to the helpers we use, without the `click`/`fill` wrappers, since Playwright already waits.
- **Automation:** I dropped separate register and valid-login tests (every test does both). Claude noticed nothing would check that logout ends the session, so that check moved into the logout test.
- **Review:** from Claude's review of the suite I chose the fixes: cleanup that always runs, a configurable timeout, an ad allowlist.
