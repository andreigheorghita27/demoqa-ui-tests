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
| CI (GitHub Actions) | [.github/workflows/tests.yml](.github/workflows/tests.yml) |
| Test strategy for an AI feature | [docs/ai-test-strategy.md](docs/ai-test-strategy.md) |
| AI usage statement | [below](#ai-usage) |

## Structure

```
.
├── .github/workflows/    # CI: runs the suite on push, on pull requests and weekly
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

Each run writes JUnit results to `reports/junit/` and a screenshot of every failed step to
`reports/screenshots/`.

On GitHub, the suite runs headless on every push to `main`, on pull requests and once a week
(the site is public and can change even when the code does not). The same job audits the
dependencies with `pip-audit`; the reports are kept as a build artifact.

Tests that fail because of a bug in [docs/known-bugs.md](docs/known-bugs.md) are tagged
`@known_bug` and skipped by default, so a red run always means something new broke. They keep
checking the correct behaviour and are expected to fail until the site is fixed.

## AI usage

I used Claude (Claude Code) throughout: I made the decisions and checked its work; Claude drafted, coded and reviewed.
- **Exploration:** I explored the site (16 checks) and also had Claude explore it; I chose the main flow from that.
- **Rules:** I wrote `CLAUDE.md` (layers, locators, waits, data isolation) and checked Claude's code against it.
- **Plan and cases:** I set the scope, risk order and key cases (isolation, delete, invalid ISBN); Claude wrote them up.
- **What I cut:** an oversized `BasePage` (no `click`/`fill` wrappers), out-of-scope plan parts, separate register/login tests.
- **Kept from Claude:** a check that logout ends the session; from its review, always-run cleanup, a configurable timeout, an ad allowlist.
- **AI test strategy:** I set aside Claude's full draft and had it ask me questions on each section; the ideas are my answers:
  one dangerous answer in 10 runs fails the case (a non-IT user trusts it), alerts from the documentation, a person sampling the LLM judge.
- Claude proposed the example cases, recording the model version and an exact lookup before the judge, and fitted it into two pages.
