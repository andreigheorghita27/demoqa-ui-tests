import uuid
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class User:
    username: str
    password: str


def new_user() -> User:
    # A unique user per call, so tests never collide on the shared public site.
    suffix = uuid.uuid4().hex[:10]
    # The password meets the site's rules: upper, lower, digit, special character, 8+ characters.
    return User(username=f"test_{suffix}", password=f"Pw1!{suffix}")


def with_wrong_credentials(user: User, case: str) -> User:
    # Credentials that must not log in as `user`, by the case names used in login.feature.
    cases = {
        # Same username, with a password that meets the rules but is not the user's.
        "a wrong password": lambda: replace(user, password=user.password + "x"),
        # The user's real password, with a username that was never registered.
        "a username that does not exist": lambda: replace(user, username=new_user().username),
        # The user's real password with upper and lower case swapped: Pw1!abc -> pW1!ABC.
        "the password in a different case": lambda: replace(user, password=user.password.swapcase()),
    }
    if case not in cases:
        raise ValueError(f"Unknown wrong-credentials case {case!r}, expected one of {list(cases)}")
    return cases[case]()
