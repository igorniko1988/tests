"""Транспорт API-слоя: единственное место, откуда тесты ходят в сеть по HTTP.

Здесь всё общее для любого запроса: base_url, таймаут, токен, ретраи, лог и Allure.
Сервисы (services/) знают только пути и тела запросов, тесты — только сервисы.
"""

import allure
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from framework.api.reporting import report

# Повторяем только «безопасные» методы: повтор GET или DELETE не создаёт новых данных.
SAFE_RETRY = Retry(total=3, status_forcelist=[502, 503, 504], backoff_factor=0.5, raise_on_status=False)
# POST /orders можно повторять: сервис отбрасывает повтор с тем же Idempotency-Key.
ORDERS_RETRY = SAFE_RETRY.new(allowed_methods=None)


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token: str | None = None
        self.session = Session()
        self.session.headers.update({"Accept": "application/json"})
        # requests выбирает адаптер по самому длинному совпадающему префиксу URL
        self.session.mount("http://", HTTPAdapter(max_retries=SAFE_RETRY))
        self.session.mount("https://", HTTPAdapter(max_retries=SAFE_RETRY))
        self.session.mount(f"{self.base_url}/orders", HTTPAdapter(max_retries=ORDERS_RETRY))

    def request(self, method: str, path: str, **kwargs) -> Response:
        kwargs.setdefault("timeout", self.timeout)
        with allure.step(f"{method} {path}"):
            response = self.session.request(method, self.base_url + path, **kwargs)
            report(response)
        return response

    def get(self, path: str, **kwargs) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs) -> Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self.request("DELETE", path, **kwargs)

    def set_token(self, token: str) -> None:
        self.token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_token(self) -> None:
        self.token = None
        self.session.headers.pop("Authorization", None)

    def close(self) -> None:
        self.session.close()
