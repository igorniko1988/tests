class BaseClient:
    def __init__(self, base_url: str, session) -> None:
        self.base_url = base_url
        self.session = session

    def headers(self) -> dict:
        return {"Accept": "application/json"}

    def request(self, method: str, path: str, **kwargs):
        return self.session.request(method, self.base_url + path, headers=self.headers(), **kwargs)


class UsersClient(BaseClient):
    def __init__(self, base_url: str, session, token: str) -> None:
        super().__init__(base_url, session)
        self.token = token

    def headers(self) -> dict:
        return {**super().headers(), "Authorization": f"Bearer {self.token}"}

    def get_user(self, user_id):
        return self.request("GET", f"/users/{user_id}")

    def create_user(self, **fields):
        return self.request("POST", "/users", json=fields)
