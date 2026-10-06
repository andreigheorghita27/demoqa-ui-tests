# Test Plan: demoqa.com Book Store Application

## Summary

- **What:** the Book Store Application on https://demoqa.com (public and shared, not under our
  control), tested as a black box: no source code, requirements or designs.
- **Main flow:** register → log in → add and delete books → log out → another user logs in.
- **How:** UI tests (Behave + Playwright, Python, Chromium) and API checks on the Book Store
  API. The API also creates the test data, so every test starts from a known state.
- **Status:** explored on 2026-10-05; 8 bugs found so far (section 5).

## 1. Scope

**In scope:** account creation and username uniqueness; login, logout and the session; data
isolation (each user sees only their own collection, also after switching accounts in the same
browser); adding, keeping and deleting books; account deletion; search (low priority, see P5).

**Out of scope**

| Not tested | Why |
|---|---|
| Registration through the UI form, automated | Protected by reCAPTCHA, which a test should not bypass. Users are created through the API; the form is checked manually. |
| Performance and load | The site is not ours; load-testing it without permission is not appropriate. |
| Content of the book details page, visual design | No reference for the correct data, no designs to compare against. |
| Browsers other than Chromium | Limited time. Adding Firefox or WebKit is a configuration change. |
| Other areas of the site, third-party ads | One functional area was chosen; ads are not part of the product and are blocked in the tests. |

## 2. Risks and priorities

Each step of the flow blocks the next one: no account means no login, no login means no
collection. So priority follows the flow first. Impact says how bad a failure is; likelihood is
based on what exploration found.

| Priority | Risk | Impact | Likelihood | Test cases |
|---|---|---|---|---|
| **P1** | A user cannot create an account, or an existing username can be registered again | High: blocks everything after it; two people can share one username | High: D1 found | TC-01, TC-02 |
| **P2** | A user cannot log in, is not really logged out, or sees another user's data after switching accounts | High: no access, or one user's data shown to another | Medium: D8 found | TC-03 – TC-05 |
| **P3** | A book cannot be added or deleted, the collection is lost, or it accepts a book that does not exist | High: the main purpose of the app | Low: worked during exploration | TC-06 – TC-08 |
| **P4** | Account deletion does not do what the UI shows | Medium: the account is deleted, but the page says otherwise | High: D2 found | TC-09 |
| **P5** | Search gives wrong results or no feedback | Low: does not block the user | High: D3, D4 found | None: reported only |

D5 (wrong credentials return `200`) and D7 (the session cookie is readable by JavaScript) weaken
the session (P2). They are reported, not tested further: a test would only confirm them again.

## 3. Test cases and automation

The 9 test cases, in Gherkin, are in [test-cases.md](test-cases.md).

- **Automated through the UI, 5 cases:** TC-03 (the negative test), TC-04, TC-05, TC-06, TC-07.
  Together they cover every P2 and P3 risk that is tested through the page.
- **Automated API checks:** TC-02 and TC-08.
- **Not automated:** TC-01 runs in the setup of every scenario, so it needs no scenario of its
  own. TC-09 fails today because of D2, so it is checked manually and the bug is reported.

## 4. Test approach

**Test data.** Each test creates its own users (and their books) through the API and deletes
them at the end, also when it fails. Tests do not depend on each other or leave data behind.

**Login.** Login is tested through the login page in TC-03 and TC-04. Where it is not what is
tested, the user is logged in through the API: the session cookies are set in the browser,
which is faster and more stable. A broken login still fails TC-03 and TC-04 with a clear reason.

**Manual checks.** The registration form (validation messages, field behaviour) and TC-09.

**Risks to the testing itself**

| Problem | How the tests handle it |
|---|---|
| The site is public and shared: it can be slow, change or go down | Own data per test, cleanup with retries, a 10 s timeout that can be raised; known bugs are tagged and skipped, so a red run means something new broke |
| Pages load in steps; the profile table is empty before the books appear | Wait for the expected content, never for a fixed time; check an exact list of books, never an empty table |
| Ads load on every page and can cover buttons | Only the site and reCAPTCHA may load; every other host is blocked |
| Adding or deleting a book shows a native `alert` | Accept it and check its text; otherwise the page stays blocked |
| Every new API token ends the user's session in the browser | Set the browser session after all API setup steps |
| Buttons share `id="submit"`; "OK" also matches "Go To B**ook** Store" | Locate by role and exact name (`get_by_role`, `exact=True`) |

## 5. Findings

7 bugs were found while exploring and one more (D8) by the automated tests; D1 (a username can
be registered twice) is critical. The list, with steps to reproduce, is in
[known-bugs.md](known-bugs.md).

Working correctly: a failed login shows the same message for a wrong username and a wrong
password; adding the same book twice is rejected; deleting a book asks for confirmation;
logging out ends the session.

## 6. Done when

- Every P1–P4 risk is covered by at least one test case (automated or manual).
- The suite runs from a clean checkout with the steps in the README.
- Every defect is either covered by a test or listed as a known issue.
