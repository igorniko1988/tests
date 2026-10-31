"""C8 t06 (★ optional, ~20 min). Add logging to any client with a mixin.

Below are two ready clients. Implement LoggingMixin so that ANY client gets logging:

- the mixin overrides request(method, path, **kwargs): appends f"{method} {path}" to
  self.request_log BEFORE the call, calls the next request in the MRO via super(),
  appends f"-> {result['status']}" AFTER, and returns the result;
- request_log is created lazily (first request) - the mixin has no __init__.

Then define:
    class LoggedUsersClient(LoggingMixin, UsersClient): pass
    class LoggedOrdersClient(LoggingMixin, OrdersClient): pass

Follow-up questions:
- Why must the mixin be LEFT of the client in the class list?

Run (from interview_prep/python_course/week3/c08_inheritance): uv run pytest -k t06
Теория: THEORY.md в этой папке, раздел 8.
"""


class BaseClient:
    def __init__(self, session) -> None:
        self.session = session

    def request(self, method: str, path: str, **kwargs):
        return self.session.request(method, path, **kwargs)


class UsersClient(BaseClient):
    def get_user(self, user_id):
        return self.request("GET", f"/users/{user_id}")


class OrdersClient(BaseClient):
    def cancel(self, order_id):
        return self.request("DELETE", f"/orders/{order_id}")


class LoggingMixin:
    pass
