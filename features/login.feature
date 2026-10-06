Feature: Login
  Users log in with the username and password they registered with. The user is created
  through the API; the login itself goes through the UI, because that is what is tested.

  Background:
    Given a user that is already registered
    And the login page is open

  # The same message for every case: the page must not reveal whether an account exists.
  Scenario Outline: TC-03 Log in with wrong credentials: <case>
    When the user logs in with "<case>"
    Then the login error "Invalid username or password!" is shown
    And the user stays on the login page

    Examples:
      | case                           |
      | a wrong password               |
      | a username that does not exist |

    # Fails today: the password is not case-sensitive (docs/known-bugs.md, D8).
    @known_bug
    Examples: Known bug D8
      | case                             |
      | the password in a different case |

  # After logging out the session must really be over (the profile no longer opens), and the
  # account must still work (logging out must not break it).
  Scenario: TC-04 Log out, and log in again
    When the user logs in with their username and password
    Then the profile shows the user's username
    When the user logs out
    And the user opens their profile
    Then the profile says the user is not logged in
    When the user opens the login page
    And the user logs in with their username and password
    Then the profile shows the user's username
