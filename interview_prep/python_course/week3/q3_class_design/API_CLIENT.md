# Базовый API-клиент: как пишут на проектах

**Смысл темы.** В любом фреймворке API-тестов есть слой, через который тесты ходят в сервис. Плохой
клиент — это `requests.post(...)` прямо в тесте, копия URL и заголовков в каждом файле, `assert`
внутри метода. Хороший клиент — это три слоя: **базовый клиент** (всё общее про HTTP),
**клиенты сервисов** (по одному методу на эндпоинт) и **тест** (данные и проверки). На собесе
AQA просят нарисовать или написать именно это, а на ревью смотрят, где лежат таймауты, токен, логи
и ретраи. Примеры — на стенде «мини-биржа»: `POST /auth/login`, `GET /me`, `POST /orders`.

---

### 1. Слои: кто за что отвечает

```text
tests/test_orders.py        тест: готовит данные, вызывает метод, проверяет статус и тело
        │  orders.create(...)
services/orders.py          OrdersClient(BaseClient): один метод = один эндпоинт, без проверок
        │  self.post("/orders", json=...)
core/base_client.py         BaseClient: Session, base_url, таймаут, заголовки, токен, логи, ретраи
        │  self.session.request(...)
requests.Session            HTTP: соединения, cookies, адаптеры
```

- **Базовый клиент ничего не знает про ордера и пользователей** — только про HTTP.
- **Клиент сервиса ничего не знает про HTTP-детали** — только пути и тела запросов.
- **Тест не знает URL и заголовков** — только «создай ордер с такими данными».
- **Правило ревью:** если в тесте видно `requests.` или `"http://..."`, слой нарушен.

---

### 2. Минимальный профессиональный BaseClient

```python
import requests


class BaseClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)
```

- **Один `request` — единственная точка выхода в сеть.** Логи, ретраи, токен, замер времени
  добавляются в одно место, а `get`/`post` — тонкие обёртки.
- **`requests.Session`** держит соединения открытыми (keep-alive, быстрее), хранит общие заголовки
  и cookies. `requests.get(...)` каждый раз открывает новое соединение.
- **`timeout` всегда.** У `requests` по умолчанию таймаута нет: зависший сервис подвесит весь прогон.
  `setdefault` — тест может передать свой таймаут, иначе берётся общий.
- **`base_url.rstrip("/")` и путь с `/`** — чтобы не получить `http://host//orders` или `http://hostorders`.
- **Возвращает `Response`, а не `.json()`** — тесту нужен статус, заголовки (`X-Request-ID`,
  `Retry-After`) и тело; негативный тест иначе не написать.

---

### 3. Клиент сервиса: один метод — один эндпоинт

```python
class AuthClient(BaseClient):
    def register(self, email: str, password: str) -> requests.Response:
        return self.post("/auth/register", json={"email": email, "password": password})

    def login(self, email: str, password: str) -> requests.Response:
        return self.post("/auth/login", json={"email": email, "password": password})


class OrdersClient(BaseClient):
    def create(self, symbol: str, side: str, type_: str, qty: str, price: str | None = None) -> requests.Response:
        body = {"symbol": symbol, "side": side, "type": type_, "quantity": qty}
        if price is not None:
            body["price"] = price
        return self.post("/orders", json=body)

    def list(self, **params) -> requests.Response:
        return super().get("/orders", params=params)

    def get(self, order_id: str) -> requests.Response:     # id ордера на стенде — UUID строкой
        return super().get(f"/orders/{order_id}")

    def cancel(self, order_id: str) -> requests.Response:
        return self.delete(f"/orders/{order_id}")
```

- **Имена по смыслу домена** (`create`, `cancel`, `login`), а не `post_orders`.
- **Метод не проверяет статус.** Один и тот же `create` нужен и в позитивном тесте (201), и в
  негативном (422, 401) — статус проверяет тест.
- **Суммы — строки** (`"10.50"`): в API стенда деньги — Decimal строкой, float нельзя.
- **`super().get(...)`**, когда имя метода сервиса совпало с методом базы: иначе `self.get` вызовет
  сам себя.

---

### 4. Авторизация: токен один раз в сессию

```python
class BaseClient:
    ...
    def set_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_token(self) -> None:
        self.session.headers.pop("Authorization", None)
```

```python
# фикстура
auth = AuthClient(settings.base_url)
token = auth.login(user.email, user.password).json()["access_token"]
orders = OrdersClient(settings.base_url)
orders.set_token(token)
```

- **Токен кладём в заголовки сессии**, и он уходит с каждым запросом этого клиента — не надо передавать
  его в каждый метод.
- **Вариант через наследование** — `headers()` с `super()`, как в задаче C8 t01: то же самое, только
  заголовки собираются на каждый запрос. Оба способа встречаются; сессия проще.
- **Негативные тесты на авторизацию:** `clear_token()` или отдельный клиент без токена; «чужой» токен —
  второй клиент со своим пользователем.
- **Refresh (стенд: `POST /auth/refresh`):** на проектах иногда ловят 401 в `request`, обновляют токен и
  повторяют запрос один раз. В тестовом клиенте это делают осторожно: тест на «просроченный токен → 401»
  не должен «чиниться» автоматически.

---

### 5. Логирование: чтобы упавший тест можно было разобрать

```python
import logging
import time

log = logging.getLogger("api")


class BaseClient:
    ...
    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}{path}"
        start = time.perf_counter()
        response = self.session.request(method, url, **kwargs)
        ms = (time.perf_counter() - start) * 1000
        log.info("%s %s -> %s (%.0f ms) request_id=%s", method, url, response.status_code, ms,
                 response.headers.get("X-Request-ID"))
        log.debug("request body=%s response body=%s", kwargs.get("json"), response.text[:2000])
        return response
```

- **В лог: метод, URL, статус, время, `X-Request-ID`.** По `request_id` находишь строку в логах стенда:
  `docker compose logs exchange | grep <id>` — это и есть разбор падения.
- **Тела — на уровне DEBUG и с обрезкой**, иначе лог раздувается.
- **Секреты маскируем:** `Authorization`, `password`, `secret` → `***`.
- **В Allure** — то же самое как вложение к шагу (`allure.attach(...)`) или готовый curl запроса:
  разработчик повторит его одной командой.

---

### 6. Ретраи: только там, где сбой — не баг

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(
    total=3,
    backoff_factor=0.5,                       # паузы 0.5, 1, 2 с
    status_forcelist=(502, 503, 504),
    allowed_methods=frozenset({"GET", "DELETE"}),
    respect_retry_after_header=True,          # стенд в режиме сбоев шлёт 503 + Retry-After: 1
)
self.session.mount("http://", HTTPAdapter(max_retries=retry))
self.session.mount("https://", HTTPAdapter(max_retries=retry))
```

- **Повторяем только идемпотентные методы** (GET, DELETE): повтор `POST /orders` может создать второй
  ордер — у стенда половина сбоев случается уже после обработки запроса.
- **Ретраи на 5xx и сетевые ошибки, никогда на 4xx:** 400/422 — это ответ, его и проверяет тест.
- **Ретраи прячут нестабильность.** Логируй каждую попытку; в тестах на сам сбой (`EXCHANGE_CHAOS_RATE`)
  ретраи выключай — отдельный клиент или параметр `retries=0`.

---

### 7. Конфигурация и фикстуры

```python
# conftest.py
@pytest.fixture(scope="session")
def settings():
    return Settings()                          # base_url, timeout из env / .env / envs/<stage>.yaml


@pytest.fixture
def user(settings):
    auth = AuthClient(settings.base_url)
    email = f"user_{uuid.uuid4().hex[:8]}@test.io"
    auth.register(email, "secret-123")
    return SimpleNamespace(email=email, password="secret-123")


@pytest.fixture
def orders(settings, user):
    auth = AuthClient(settings.base_url)
    token = auth.login(user.email, user.password).json()["access_token"]
    client = OrdersClient(settings.base_url)
    client.set_token(token)
    yield client
    for order in client.list().json():         # teardown: стакан общий — убираем свои открытые ордера
        if order["status"] in ("NEW", "PARTIALLY_FILLED"):
            client.cancel(order["id"])
    client.session.close()
```

- **`base_url` не захардкожен** — берётся из настроек; один и тот же тест идёт на local, stage, CI.
- **Уникальный пользователь на тест** — тесты не мешают друг другу и работают параллельно (`xdist`).
- **Teardown в фикстуре после `yield`** — выполнится, даже если тест упал.
- **Фасад по желанию:** `app.orders`, `app.auth` — один объект со всеми клиентами (как `Application`
  в UI-курсе), чтобы тесту хватало одной фикстуры.

---

### 8. Тест поверх клиента

```python
def test_create_limit_order(orders):
    response = orders.create("BTC-USDT", "BUY", "LIMIT", qty="0.01", price="100.00")

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "NEW"
    assert body["price"] == "100.00"


def test_create_order_without_token(settings):
    response = OrdersClient(settings.base_url).create("BTC-USDT", "BUY", "LIMIT", qty="0.01", price="1")
    assert response.status_code == 401
```

- **Тест читается как сценарий**: вызов → статус → поля. Ни URL, ни заголовков.
- **Проверка схемы тела** — следующий слой: модели pydantic (`OrderOut.model_validate(body)`) — так
  ловят пропавшие поля и неверные типы одной строкой.
- **Негатив тем же методом** — поэтому клиент возвращает `Response` и не бросает исключений.

---

### 9. Частые ошибки (их ищут на ревью)

- `requests.post(...)` прямо в тесте, URL и заголовки скопированы по файлам.
- Нет `timeout` — прогон висит часами на одном запросе.
- `assert response.status_code == 200` внутри клиента — негативный тест невозможен.
- Метод возвращает `.json()` — пропали статус и заголовки; на 500 с HTML падает `JSONDecodeError`.
- Токен передаётся аргументом в каждый метод или хранится в глобальной переменной.
- Ретраи на все методы и все статусы — тест «зелёный», баг спрятан, POST задвоился.
- Логов нет или в них пароли и токены открытым текстом.
- Новый `requests.Session()` (или `requests.get`) на каждый запрос.

---

### Собес

- **Как устроен API-клиент в вашем фреймворке?** Три слоя: BaseClient на `requests.Session` с
  base_url, таймаутом, общими заголовками, логированием и ретраями в одном методе `request`; клиенты
  сервисов наследуют его, по методу на эндпоинт, возвращают `Response`; тесты вызывают методы и
  проверяют статус и тело, данные и уборка — в фикстурах.
- **Почему клиент возвращает Response, а не json?** Тесту нужны статус и заголовки, а негативные
  тесты используют те же методы; клиент не решает, что такое «правильный» ответ.
- **Зачем Session?** Переиспользует TCP-соединения, хранит общие заголовки (токен) и cookies.
- **Где проверять статус: в клиенте или в тесте?** В тесте. Допустимый вариант — параметр
  `expected_status` или исключение `ApiError(status, body)` в хелпере для подготовки данных, где
  ошибка значит «сломана подготовка», а не «тест упал».
- **Как авторизуешься?** Логин в фикстуре, токен в заголовки сессии клиента; без токена — отдельный
  клиент для негативных тестов; refresh-логику в тестовый клиент добавляю осторожно.
- **Ретраи в тестовом клиенте — хорошо или плохо?** Только для идемпотентных методов и 5xx/сети,
  с логом каждой попытки; на 4xx и POST — нет, иначе прячем баги и задваиваем данные.
- **Как разбираешь упавший API-тест?** Лог клиента: метод, URL, статус, время, `X-Request-ID` → по нему
  строка в логах сервиса (и трейс в Jaeger); тело запроса и ответа — во вложении Allure.

---

### Практика

1. **C8 t01** (`interview_prep/python_course/week3_core/c08_t01_client_hierarchy.py`) — та же идея в
   миниатюре: `request` в базе, `headers()` через `super()`.
2. **Q3 t05 ★** (`interview_prep/python_course/week3/q3_class_design/t05_api_client.py`) — клиент с
   `ApiError`, фейковой сессией и логином.
3. **Устно за 5 минут:** нарисуй три слоя и расскажи по разделу «Собес».
