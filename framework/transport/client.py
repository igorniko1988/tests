import allure
from httpx import Auth, BaseTransport, Client, Response
from tenacity import Retrying, retry_if_result, stop_after_attempt, wait_exponential

from framework.transport.http_logging import format_request, format_response

RETRY_METHODS = {"GET", "PUT", "DELETE"}
RETRY_STATUSES = {502, 503, 504}


class ApiClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 10,
        transport: BaseTransport | None = None,
        retry_attempts: int = 1,
        retry_backoff: float = 0.5,
        auth: Auth | None = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.transport = transport
        self.retry_attempts = retry_attempts
        self.retry_backoff = retry_backoff
        self._client = Client(
            base_url=self.base_url, timeout=self.timeout, transport=self.transport, auth=auth
        )

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._client.close()

    def close(self):
        self._client.close()

    def request(self, method: str, path: str, **kwargs) -> Response:
        if method.upper() not in RETRY_METHODS:
            return self._send(method, path, **kwargs)

        retrying = Retrying(
            retry=retry_if_result(lambda response: response.status_code in RETRY_STATUSES),
            stop=stop_after_attempt(self.retry_attempts),
            wait=wait_exponential(multiplier=self.retry_backoff),
            retry_error_callback=lambda state: state.outcome.result(),
        )
        return retrying(self._send, method, path, **kwargs)

    def _send(self, method: str, path: str, **kwargs) -> Response:
        # auth=None из сервиса не должен отключать токен, заданный клиенту
        if kwargs.get("auth") is None:
            kwargs.pop("auth", None)
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
