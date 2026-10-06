# Test Cases: demoqa.com Book Store Application

Nine cases, ordered by priority. Priorities (P1–P5) and the choice of what is automated are
explained in sections 2 and 3 of the [test plan](test-plan.md).

Each case is written in Gherkin: `Given` is the starting state, `When` the user action,
`Then` the result that must be seen. Automated cases use the same steps as their feature file.
Every case starts with its own new users, created through the API and deleted afterwards.
Login goes through the login page only where it is part of what the case tests; otherwise the
user is logged in through the API.

| ID | Test case | Priority | Level | Automated |
|---|---|---|---|---|
| TC-01 | Register a new user | P1 | API | Covered by the setup of every scenario |
| TC-02 | Register an existing username | P1 | API | Yes (API); one case fails today (D1) |
| TC-03 | Log in with wrong credentials | P2 | UI | Yes; one case fails today (D8) |
| TC-04 | Log out, and log in again | P2 | UI | Yes |
| TC-05 | A user does not see another user's collection | P2 | UI | Yes |
| TC-06 | Add a book; it is still there after logging in again | P3 | UI | Yes |
| TC-07 | Delete a book from the collection | P3 | UI | Yes |
| TC-08 | A book that is not in the Book Store cannot be added | P3 | API | Yes (API) |
| TC-09 | Delete the account | P4 | UI | No, fails today (D2) |

## TC-01 Register a new user

**Priority:** P1 · **Level:** API · **Automated:** no scenario of its own. Every automated
scenario registers its users through the API and fails with "Setup failed" if that breaks.

```gherkin
Given a new user with a valid password
When the user is registered through the API
Then the account is created
And the new user can log in
```

## TC-02 Register an existing username

**Priority:** P1 · **Level:** API · **Automated:** the same-password case,
[features/register.feature](../features/register.feature)

```gherkin
Scenario Outline: Register an existing username with <password>
  Given a user that is already registered
  When the same username is registered through the API with <password>
  Then the registration is rejected with "User exists!"

  Examples:
    | password             |
    | the same password    |

  # Fails today: a different password creates a second account (known bug D1).
  Examples: Known bug D1
    | password             |
    | a different password |
```

## TC-03 Log in with wrong credentials

**Priority:** P2 · **Level:** UI · **Automated:** [features/login.feature](../features/login.feature)

The same message for every case: the page must not reveal whether an account exists.

```gherkin
Scenario Outline: Log in with wrong credentials: <case>
  Given a user that is already registered
  And the login page is open
  When the user logs in with "<case>"
  Then the login error "Invalid username or password!" is shown
  And the user stays on the login page

  Examples:
    | case                           |
    | a wrong password               |
    | a username that does not exist |

  # Fails today: the password is not case-sensitive (known bug D8).
  Examples: Known bug D8
    | case                             |
    | the password in a different case |
```

## TC-04 Log out, and log in again

**Priority:** P2 · **Level:** UI · **Automated:** [features/login.feature](../features/login.feature)

After logging out the session must really be over: opening the profile shows the "not logged
in" message, so the next person at the same computer cannot use the account. Then the account
must still work: logging out must not break it (for example, by deleting it). It also covers a
valid login.

```gherkin
Given a user that is already registered
And the login page is open
When the user logs in with their username and password
Then the profile shows the user's username
When the user logs out
And the user opens their profile
Then the profile says the user is not logged in
When the user opens the login page
And the user logs in with their username and password
Then the profile shows the user's username
```

## TC-05 A user does not see another user's collection after switching accounts

**Priority:** P2 · **Level:** UI · **Automated:** [features/collection.feature](../features/collection.feature)

Two users log in one after the other in the same browser. Nothing from the first account may
reach the second: not through the server, and not through anything the browser kept. The books
are added through the API, because what is tested is what the second user sees. User A first
sees their own book, so there is something in the browser that could leak. User B has a book
too, so the check also proves the collection has loaded and is not just empty.

```gherkin
Given user A has "Git Pocket Guide" in their collection
And user B has "Learning JavaScript Design Patterns" in their collection
And the login page is open
When user A logs in with their username and password
Then the collection shows only "Git Pocket Guide"
When user A logs out
And user B logs in with their username and password
Then the profile shows user B's username
And the collection shows only "Learning JavaScript Design Patterns"
```

## TC-06 A user adds a book, and it is still there after logging in again

**Priority:** P3 · **Level:** UI · **Automated:** [features/collection.feature](../features/collection.feature)

The main flow from start to end, as a user does it: log in, add a book, log out and back in.
Only the registration is done through the API, because the form has a reCAPTCHA.
The API check shows that the book was saved on the server, not only shown on the page.
The username check after the first login also makes sure the login has finished before the
user moves on to the Book Store.

```gherkin
Given a user that is already registered
And the login page is open
When the user logs in with their username and password
Then the profile shows the user's username
When the user adds "Git Pocket Guide" from the Book Store
Then the confirmation "Book added to your collection." is shown
When the user opens their profile
Then the collection shows only "Git Pocket Guide"
And the Book Store API has only "Git Pocket Guide" in the user's collection
When the user logs out
And the user logs in with their username and password
Then the collection shows only "Git Pocket Guide"
```

## TC-07 A user deletes a book from their collection

**Priority:** P3 · **Level:** UI · **Automated:** [features/collection.feature](../features/collection.feature)

The books and the login are set up through the API; the deletion, which is what is tested, is
done on the page. The user starts with two books and deletes one: the check that exactly the
other one is left proves the right book was deleted and the collection has loaded (a check for
an empty collection could pass while the table is still loading). The API check shows the book
was deleted on the server, not only removed from the table.

```gherkin
Given the user has "Git Pocket Guide" and "Speaking JavaScript" in their collection
And the user is logged in through the API
And the profile is open
When the user deletes "Git Pocket Guide" from their collection
Then the confirmation "Book deleted." is shown
And the collection shows only "Speaking JavaScript"
And the Book Store API has only "Speaking JavaScript" in the user's collection
```

## TC-08 A book that is not in the Book Store cannot be added

**Priority:** P3 · **Level:** API · **Automated:** [features/collection.feature](../features/collection.feature)

A negative API case. The user already has a book, so the check also shows that the rejected
request did not change the collection (nothing added, nothing removed). Checked by hand on
2026-10-07: the API answers `400` with code `1205`.

```gherkin
Given the user has "Git Pocket Guide" in their collection
When a book with ISBN "0000000000000" is added through the API
Then the request is rejected with "ISBN supplied is not available in Books Collection!"
And the Book Store API has only "Git Pocket Guide" in the user's collection
```

## TC-09 Delete the account

**Priority:** P4 · **Level:** UI · **Automated:** no. It fails today because of known bug D2,
so it was checked manually and the bug is reported in [known-bugs.md](known-bugs.md).

```gherkin
Given a user that is already registered
And the user is logged in through the API
And the profile is open
When the user deletes their account and confirms
Then the account no longer exists
And the user is shown as logged out
```
