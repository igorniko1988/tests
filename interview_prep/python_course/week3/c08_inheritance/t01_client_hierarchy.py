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

Run (from interview_prep/python_course/week3/c08_inheritance): uv run pytest -k t01
Теория: THEORY.md в этой папке, раздел 2–3.
"""


class BaseClient:
    def __init__(self, base_url: str, session) -> None:
        raise NotImplementedError


class UsersClient(BaseClient):
    pass
