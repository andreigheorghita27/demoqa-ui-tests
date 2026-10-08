# Known Bugs

Defects found on https://demoqa.com while exploring and testing the Book Store Application.
The site is public, so its behaviour may change: each full report lists the date it was last
reproduced.

Tests for these bugs are tagged `@known_bug`. They check the correct behaviour, so they fail
while the bug is there, and are skipped in a normal run. Run them with
`behave --tags=@known_bug`; when one of them passes, the bug has been fixed.

## Summary

| ID | Area | Finding | Severity | Found |
|---|---|---|---|---|
| D1 | Registration | An existing username can be registered again with a different password | Critical | Exploration, 2026-10-05 |
| D2 | Account deletion | The account is deleted, but the page breaks and still shows the user as logged in | High | Exploration, 2026-10-05 |
| D3 | Search | Spaces are not trimmed; no message when nothing matches | Low | Exploration, 2026-10-05 |
| D4 | Book details | A non-existent ISBN shows an empty page with no message | Low | Exploration, 2026-10-05 |
| D5 | Login (API) | Wrong credentials return `200 OK` instead of `401` | Medium | Exploration, 2026-10-05 |
| D6 | Registration (UI) | A password error disappears too fast and clears all fields; after registering, the user is left on the form | Medium | Exploration, 2026-10-05 |
| D7 | Session | The session token cookie is readable by JavaScript (not `HttpOnly`) | Medium | Exploration, 2026-10-05 |
| D8 | Login | The password is not case-sensitive | High | TC-03, 2026-10-06 |

D1 and D8 have full reports further down, because test cases cover them (TC-02, TC-03). D2 to
D7 are described briefly here:

- **D2.** After confirming "Delete Account", the server deletes the account (`DELETE` → `204`,
  login no longer works). But the page throws a JavaScript error (`Unexpected end of JSON
  input`), the dialog stays open and the profile still shows the user. Once, the first click
  on "Delete Account", right after the profile loaded, did nothing.
- **D3.** "git" finds a book, " git " finds nothing. With no match, the pager shows
  "Page 1 of 0".
- **D4.** A book page's address is `/books?search=<ISBN>`. For example `?search=0000000000000`
  or `?search=3`.
- **D5.** `POST /Account/v1/GenerateToken` returns `200` with `"status":"Failed"`.
  `POST /Account/v1/Authorized` says "User not found!" also for an existing user with a
  wrong password.
- **D6.** Two problems with the registration form. A password that breaks the rules shows an
  error that disappears too fast to read, and all fields are cleared, so the user has to type
  everything again. After a successful registration, a native alert is shown and the user
  stays on the registration page instead of being taken to log in.
- **D7.** If the site had a cross-site scripting (XSS) flaw, a script could steal the session.

## D1. An existing username can be registered again with a different password

| | |
|---|---|
| **Area** | Registration (Book Store API) |
| **Severity** | Critical |
| **Last reproduced** | 2026-10-06 |
| **Test** | TC-02, case "a different password". Fails today. |

**Steps to reproduce**

1. Register a user: `POST /Account/v1/User` with `{"userName": "<name>", "password": "<password A>"}`.
2. Register the same username again with a different password:
   `POST /Account/v1/User` with `{"userName": "<name>", "password": "<password B>"}`.
3. Log in with each password: `POST /Account/v1/GenerateToken`.

**Expected result**

Step 2 is rejected with `406 "User exists!"`, as it is when the password is the same.

**Actual result**

- Step 2 returns `201` and creates a second account with the same username and a
  different `userID`.
- Both passwords log in (`"status": "Success"`), each into its own account.

**Impact**

Usernames are not unique. Two people can share one username, each with their own account and
collection, and anyone can create an account with an existing user's name.

## D8. The password is not case-sensitive

| | |
|---|---|
| **Area** | Login (UI and Book Store API) |
| **Severity** | High |
| **Last reproduced** | 2026-10-06 |
| **Test** | TC-03, case "the password in a different case". Fails today. |

**Steps to reproduce**

1. Register a user with the password `Pw1!0d85cd5c39`.
2. On `/login`, log in with the same username and the password with upper and lower case
   swapped: `pW1!0D85CD5C39`.

**Expected result**

The login is rejected with "Invalid username or password!", as for any other wrong password.

**Actual result**

- The user is logged in and `/profile` shows their username.
- The API behaves the same: `POST /Account/v1/GenerateToken` returns `"status": "Success"`
  for the original password, the swapped one, all lower case and all upper case.

**Impact**

Registration requires an upper case and a lower case letter, but login ignores the
difference, so the password is weaker than the rules suggest. Anyone guessing a password
only has to get the letters right, not their case.
