import httpx

from framework.transport.client import ApiClient


class AuthApi:
    def __init__(self, client: ApiClient):
        self._client = client

    def register(self, user_data: dict) -> httpx.Response:
        return self._client.post("/auth/register", json=user_data)

    def login(self, user_data: dict) -> httpx.Response:
        return self._client.post("/auth/login", json=user_data)

    def me(self, auth: httpx.Auth | None = None) -> httpx.Response:
        return self._client.get("/me", auth=auth)
