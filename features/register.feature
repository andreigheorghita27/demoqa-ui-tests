Feature: Registration
  Users are registered through the Book Store API. The register form is protected by an
  invisible reCAPTCHA that blocks automated browsers, so it is checked manually.
  Registering a new user (TC-01) has no scenario of its own: every scenario does it in its
  setup and fails with "Setup failed" if it breaks.

  @api
  Scenario: TC-02 Register an existing user with the same credentials
    Given a user that is already registered
    When the user is registered through the API
    Then the registration is rejected with "User exists!"
