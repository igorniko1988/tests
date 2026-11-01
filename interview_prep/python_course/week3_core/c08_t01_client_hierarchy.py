"""C8 t01 (required, ~20 min). A hierarchy of API clients.

Implement two classes.

BaseClient(base_url, session):
- session is any object with a method request(method, url, **kwargs) (in tests - a fake);
- headers() -> {"Accept": "application/json"};
- request(method, path, **kwargs) calls session.request(method, base_url + path,
  headers=self.headers(), **kwargs) and returns its result.

UsersClient(BaseClient), created as UsersClient(base_url, session, token):
- headers() EXTENDS the parent's headers (call super()) with
  "Authorization": "Bearer <token>";
- get_user(user_id)        -> request("GET", f"/users/{user_id}");
- create_user(**fields)    -> request("POST", "/users", json=fields).

Example:
    session = FakeSession()
    users = UsersClient("http://api", session, token="t1")
    users.get_user(7)
    # session.request("GET", "http://api/users/7",
    #                 headers={"Accept": "application/json", "Authorization": "Bearer t1"})

Follow-up questions:
- What breaks if UsersClient.__init__ forgets super().__init__?
- Where is the polymorphism here?

Run (from interview_prep/python_course/week3_core): uv run pytest -k c08_t01
Теория: THEORY.md в этой папке, раздел 2–3.
"""


class BaseClient:
    def __init__(self, base_url: str, session) -> None:
        self.base_url = base_url
        self.session = session

    def headers(self) -> dict:
        return {"Accept": "application/json"}

    def request(self, method: str, path: str, **kwargs):
        # self.headers() — полиморфизм: у наследника вызовется его версия
        return self.session.request(method, self.base_url + path, headers=self.headers(), **kwargs)


class UsersClient(BaseClient):
    def __init__(self, base_url: str, session, token: str) -> None:
        super().__init__(base_url, session)  # родитель сохранит base_url и session
        self.token = token

    def headers(self) -> dict:
        result = super().headers()  # заголовки родителя + свой
        result["Authorization"] = f"Bearer {self.token}"
        return result

    def get_user(self, user_id):
        return self.request("GET", f"/users/{user_id}")

    def create_user(self, **fields):
        return self.request("POST", "/users", json=fields)
