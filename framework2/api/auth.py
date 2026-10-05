from framework2.client import ApiClient


class AuthApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def register(self, email: str, password: str):
        return self.client.post("/auth/register", json={"email": email, "password": password})

    def login(self, email: str, password: str):
        return self.client.post("/auth/login", json={"email": email, "password": password})

    def me(self):
        return self.client.get("/me")
