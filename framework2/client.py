import json

import allure
import requests

SECRET_HEADERS = {"authorization", "cookie"}
SECRET_FIELDS = {"password", "access_token"}


class ApiClient(requests.Session):
    """requests.Session с базовым адресом, таймаутом по умолчанию и логом в Allure."""

    def __init__(self, base_url: str, timeout: float = 10):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        response = super().request(method, f"{self.base_url}{path}", **kwargs)
        attach_to_allure(response)
        return response

    def set_token(self, token: str) -> None:
        """После этого все запросы клиента идут с этим токеном."""
        self.headers["Authorization"] = f"Bearer {token}"


def attach_to_allure(response: requests.Response) -> None:
    request = response.request
    with allure.step(f"{request.method} {request.path_url} → {response.status_code}"):
        allure.attach(_describe(request.headers, request.body), "request")
        allure.attach(_describe(response.headers, response.content), "response")


def _describe(headers, body) -> str:
    safe_headers = {k: "***" if k.lower() in SECRET_HEADERS else v for k, v in headers.items()}
    return json.dumps({"headers": safe_headers, "body": _mask(_parse(body))}, indent=2, default=str)


def _parse(body):
    if not body:
        return None
    try:
        return json.loads(body)
    except ValueError:
        return body.decode(errors="replace") if isinstance(body, bytes) else body


def _mask(data):
    if isinstance(data, dict):
        return {k: "***" if k in SECRET_FIELDS else _mask(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_mask(item) for item in data]
    return data
