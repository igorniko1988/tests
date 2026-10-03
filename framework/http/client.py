import allure
from httpx import Client, Response

from framework.http.http_logging import format_request, format_response


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
        response = self._client.request(method, path, **kwargs)
        with allure.step(f"{method} {path} --> {response.status_code}"):
            allure.attach(
                format_request(response.request),
                name="request",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                format_response(response),
                name="response",
                attachment_type=allure.attachment_type.TEXT,
            )
        return response

    def get(self, path: str, **kwargs) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self.request("DELETE", path, **kwargs)
