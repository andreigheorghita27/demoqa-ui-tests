from playwright.sync_api import APIRequestContext, APIResponse

from utils.config import BASE_URL
from utils.test_data import User


DELETE_ATTEMPTS = 3


class BookStoreApi:
    # Book Store API calls, used for test data and for API-level checks.
    # Every user created here is remembered and deleted by delete_created_users().

    def __init__(self, request: APIRequestContext) -> None:
        self.request = request
        self.created_users: list[tuple[User, str]] = []  # (user, userID)

    def create_user(self, user: User) -> APIResponse:
        # POST /Account/v1/User: 201 with the new userID, 400 for a weak password.
        response = self.request.post("/Account/v1/User", data={"userName": user.username, "password": user.password})
        if response.status == 201:
            self.created_users.append((user, response.json()["userID"]))
        return response

    def register(self, user: User) -> None:
        # Test setup: a registered user. Fails the scenario with a clear reason if it does not work.
        response = self.create_user(user)
        assert response.status == 201, f"Setup failed, could not create the user: {response.status} {response.text()}"

    def generate_token(self, user: User) -> dict:
        # Returns 200 even for wrong credentials (defect D5): check "status", not the status code.
        # Every new token ends the user's earlier session, also one in the browser: its next
        # request gets "User not authorized!". So a browser session is set up after the API setup.
        return self.request.post(
            "/Account/v1/GenerateToken", data={"userName": user.username, "password": user.password}
        ).json()

    def session_cookies(self, user: User) -> list[dict]:
        # The cookies the site sets on login, built from a new token: puts the user's session
        # in the browser without going through the login page.
        token = self.generate_token(user)
        values = {"userID": self._user_id(user), "userName": user.username, "token": token["token"], "expires": token["expires"]}
        return [{"name": name, "value": value, "url": BASE_URL} for name, value in values.items()]

    def create_user_with_books(self, user: User, titles: list[str]) -> None:
        # Test setup: a registered user with these books in their collection.
        self.register(user)
        self.add_books(user, titles)

    def add_books(self, user: User, titles: list[str]) -> None:
        # Test setup: add books, found by their titles, to the user's collection.
        response = self.add_isbns(user, [self.isbn_of(title) for title in titles])
        assert response.status == 201, f"Setup failed, could not add {titles}: {response.status} {response.text()}"

    def add_isbns(self, user: User, isbns: list[str]) -> APIResponse:
        # POST /BookStore/v1/Books: 201 when the books are added, 400 for an ISBN the store does not have.
        token = self.generate_token(user)["token"]
        return self.request.post(
            "/BookStore/v1/Books",
            headers={"Authorization": f"Bearer {token}"},
            data={"userId": self._user_id(user), "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns]},
        )

    def isbn_of(self, title: str) -> str:
        # GET /BookStore/v1/Books: the books on the site. Looked up by title, so no ISBN is hard-coded.
        books = self.request.get("/BookStore/v1/Books").json()["books"]
        isbns = [book["isbn"] for book in books if book["title"] == title]
        assert isbns, f"No book titled {title!r} in the Book Store"
        return isbns[0]

    def collection_titles(self, user: User) -> list[str]:
        # GET /Account/v1/User/{userID}: the user's account, with the books in their collection.
        token = self.generate_token(user)["token"]
        response = self.request.get(
            f"/Account/v1/User/{self._user_id(user)}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status == 200, f"Could not read the collection: {response.status} {response.text()}"
        return [book["title"] for book in response.json()["books"]]

    def _user_id(self, user: User) -> str:
        for created, user_id in self.created_users:
            if created == user:
                return user_id
        raise ValueError(f"{user.username} was not created through BookStoreApi, so its userID is unknown")

    def delete_user(self, user: User, user_id: str) -> APIResponse:
        token = self.generate_token(user)["token"]
        return self.request.delete(f"/Account/v1/User/{user_id}", headers={"Authorization": f"Bearer {token}"})

    def delete_created_users(self) -> None:
        # Cleanup after each scenario: no test data is left on the shared site.
        # One failed delete does not stop the others; all failures are reported at the end.
        failures = []
        while self.created_users:
            user, user_id = self.created_users.pop()
            error = self._delete_with_retries(user, user_id)
            if error:
                failures.append(f"{user.username}: {error}")
        if failures:
            raise RuntimeError(f"Could not delete test users: {failures}")

    def _delete_with_retries(self, user: User, user_id: str) -> str | None:
        # The shared demo API sometimes fails a request for no reason of ours, so a delete is
        # tried up to DELETE_ATTEMPTS times. Returns None once deleted, else the last error.
        error = None
        for _ in range(DELETE_ATTEMPTS):
            try:
                response = self.delete_user(user, user_id)
                if response.status == 204:
                    return None
                error = f"{response.status} {response.text()}"
            except Exception as exception:
                error = repr(exception)
        return error
