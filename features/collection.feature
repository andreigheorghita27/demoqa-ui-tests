Feature: Collection
  Logged-in users add books from the Book Store to their own collection, shown on their profile.
  Users are created through the API; the rest is done through the UI, as a user would, except
  in TC-08, which checks the Book Store API itself.

  # Both users log in in the same browser: nothing from user A may reach user B, either from
  # the server or from anything the browser kept. User A first sees their own book, so there is
  # something that could leak; user B has a book too, so their check also proves the collection
  # has loaded and is not just empty.
  Scenario: TC-05 A user does not see another user's collection after switching accounts
    Given user A has "Git Pocket Guide" in their collection
    And user B has "Learning JavaScript Design Patterns" in their collection
    And the login page is open
    When user A logs in with their username and password
    Then the collection shows only "Git Pocket Guide"
    When user A logs out
    And user B logs in with their username and password
    Then the profile shows user B's username
    And the collection shows only "Learning JavaScript Design Patterns"

  Scenario: TC-06 A user adds a book, and it is still there after logging in again
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

  # Two books, so the check proves the right one was deleted and the collection has loaded:
  # a check for an empty collection could pass while the table is still loading.
  Scenario: TC-07 A user deletes a book from their collection
    Given the user has "Git Pocket Guide" and "Speaking JavaScript" in their collection
    And the user is logged in through the API
    And the profile is open
    When the user deletes "Git Pocket Guide" from their collection
    Then the confirmation "Book deleted." is shown
    And the collection shows only "Speaking JavaScript"
    And the Book Store API has only "Speaking JavaScript" in the user's collection

  # The user already has a book, so the last check also shows that the rejected request did
  # not change the collection: nothing was added and nothing was removed.
  @api
  Scenario: TC-08 A book that is not in the Book Store cannot be added
    Given the user has "Git Pocket Guide" in their collection
    When a book with ISBN "0000000000000" is added through the API
    Then the request is rejected with "ISBN supplied is not available in Books Collection!"
    And the Book Store API has only "Git Pocket Guide" in the user's collection
