from httpx import Client, Response


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 10):
        self.base_url = base_url
        self.timeout = timeout
        self._client = Client(base_url=self.base_url, timeout=self.timeout)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._client.close()

    def close(self):
        self._client.close()

    def request(self, method: str, path: str, **kwargs) -> Response:
        return self._client.request(method, path, **kwargs)

    def get(self, path: str, **kwargs) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self.request("DELETE", path, **kwargs)



