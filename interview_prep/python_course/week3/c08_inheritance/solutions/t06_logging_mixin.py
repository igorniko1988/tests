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
    def request(self, method: str, path: str, **kwargs):
        if not hasattr(self, "request_log"):
            self.request_log = []
        self.request_log.append(f"{method} {path}")
        result = super().request(method, path, **kwargs)
        self.request_log.append(f"-> {result['status']}")
        return result


class LoggedUsersClient(LoggingMixin, UsersClient):
    pass


class LoggedOrdersClient(LoggingMixin, OrdersClient):
    pass
