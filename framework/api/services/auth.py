from requests import Response

from framework.api.client import ApiClient


class AuthService:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def register(self, email: str, password: str) -> Response:
        return self.client.post("/auth/register", json={"email": email, "password": password})

    def login(self, email: str, password: str) -> Response:
        return self.client.post("/auth/login", json={"email": email, "password": password})

    def me(self) -> Response:
        return self.client.get("/me")
