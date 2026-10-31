"""Q3 t05 (★ optional, ~25 min). API client with error handling.

Implement:

- ApiError(Exception) with attributes status and body; str: "HTTP <status>: <body>";
- ApiClient(base_url, session, token=None):
  - base_url may end with "/" - do not produce "//" in URLs;
  - request(method, path, **kwargs) calls session.request(method, url, headers=..., **kwargs);
    headers: {"Accept": "application/json"} plus "Authorization": "Bearer <token>" if a token is set;
  - the session returns an object with .status (int) and .body; status >= 400 -> raise ApiError,
    otherwise return body;
  - get(path, **params) -> request("GET", path, params=params);
    post(path, json) -> request("POST", path, json=json);
  - login(email, password): POST /auth/login with {"email", "password"}, stores
    body["access_token"] as the token and returns it.

Follow-up questions:
- Why raise ApiError in the client instead of asserting the status there?

Run (from interview_prep/python_course/week3/q3_class_design): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 6.
"""


class ApiError(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str, session, token: str | None = None) -> None:
        raise NotImplementedError
