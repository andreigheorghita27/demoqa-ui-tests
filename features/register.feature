Feature: Registration
  Users are registered through the Book Store API. The register form is protected by an
  invisible reCAPTCHA that blocks automated browsers, so it is checked manually.
  Registering a new user (TC-01) has no scenario of its own: every scenario does it in its
  setup and fails with "Setup failed" if it breaks.

  @api
  Scenario Outline: TC-02 Register an existing username with <case>
    Given a user that is already registered
    When the same username is registered through the API with <case>
    Then the registration is rejected with "User exists!"

    Examples:
      | case              |
      | the same password |

    # Fails today: a different password creates a second account (docs/known-bugs.md, D1).
    @known_bug
    Examples: Known bug D1
      | case                 |
      | a different password |
