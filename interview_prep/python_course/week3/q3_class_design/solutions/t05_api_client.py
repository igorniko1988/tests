class ApiError(Exception):
    def __init__(self, status: int, body) -> None:
        super().__init__(f"HTTP {status}: {body}")
        self.status = status
        self.body = body


class ApiClient:
    def __init__(self, base_url: str, session, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.token = token

    def _headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, method: str, path: str, **kwargs):
        response = self.session.request(method, self.base_url + path, headers=self._headers(), **kwargs)
        if response.status >= 400:
            raise ApiError(response.status, response.body)
        return response.body

    def get(self, path: str, **params):
        return self.request("GET", path, params=params)

    def post(self, path: str, json):
        return self.request("POST", path, json=json)

    def login(self, email: str, password: str) -> str:
        body = self.post("/auth/login", {"email": email, "password": password})
        self.token = body["access_token"]
        return self.token
