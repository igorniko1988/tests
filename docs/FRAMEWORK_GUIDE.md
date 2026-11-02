# Фреймворк автотестов «мини-биржи»: пособие

**Смысл темы.** Фреймворк — это код, на котором пишутся тесты: как сходить в API, как открыть страницу,
где взять пользователя, как убрать за собой, как получить отчёт. Тест должен читаться как сценарий
(«зарегистрировался → пополнил → выставил ордер → проверил»), а всё «как» спрятано во фреймворке.
Здесь разобрано, что где лежит, почему так, как проходит один тест от начала до конца, как это
запускается в CI и что про это рассказать на собесе.

Запуск всего: `docker compose up -d`, потом `uv run pytest`.

---

## 1. Общая картина

```text
                     tests/  — ЧТО проверяем (сценарии и проверки)
        ┌────────────┬────────────┬──────────────┬────────────┐
        │ tests/unit │ tests/api  │  tests/ui    │ tests/e2e  │
        └────────────┴─────┬──────┴──────┬───────┴─────┬──────┘
                           │             │             │  (API готовит, UI проверяет)
                     framework/  — КАК (один пакет, два слоя + общее ядро)
        ┌──────────────────┴──┐   ┌──────┴──────────────────┐
        │ framework/api       │   │ framework/ui            │
        │ Api → сервисы →     │   │ Application → страницы →│
        │ ApiClient(requests) │   │ компоненты (Playwright) │
        └──────────┬──────────┘   └───────────┬─────────────┘
        ┌──────────┴──────────────────────────┴─────────────┐
        │ общее: config · data · utils · fixtures · plugins │
        └───────────────────────────────────────────────────┘
                              │
                     стенд: http://localhost:8080
```

- **Один репозиторий, один пакет `framework/`.** Внутри два слоя — API и UI — и общее ядро, которым
  пользуются оба: настройки, данные, ожидания, фикстуры, отчёты. Это самая частая схема в продуктовых
  командах.
- **Тесты отдельно от фреймворка** и разложены по уровням: unit, api, ui, e2e.
- **Правило зависимостей:** тесты → фреймворк → стенд. Фреймворк ничего не знает про тесты; API-слой не
  знает про UI; UI-слой может пользоваться API-слоем (например, в e2e), но не наоборот.

---

## 2. Карта папок

```text
conftest.py                    подключает плагины фреймворка (pytest_plugins) — единственный conftest
pyproject.toml                 зависимости, настройки pytest (маркеры, addopts), ruff
framework/
  config/
    settings.py                Settings + get_settings(): base_url, таймауты, ws_url
    envs/dev.env               localhost:8080 — локальный стенд
    envs/stage.env             localhost:8081 — stage-экземпляр
    envs/k8s.env               localhost:8082 — Kubernetes через port-forward
  api/
    client.py                  ApiClient: Session, Accept, таймаут, токен, ретраи, лог
    reporting.py               строка лога + Allure на каждый запрос, маскирование секретов
    app.py                     Api — фасад: api.auth, api.balances, api.orders
    services/                  по классу на ресурс: AuthService, BalanceService, OrderService
    models/                    pydantic: запросы (CreateOrder) и ответы (Order, Balance, Profile)
    contract.py                assert_matches_schema(): тело ответа против OpenAPI сервиса
  ui/
    application.py             Application — фасад: app.auth_page, app.dashboard_page
    pages/                     BasePage, AuthPage, DashboardPage
    components/                части страниц: формы, таблицы, шапка, тост
  data/
    generators.py              уникальные email, пароли, credentials(), isolated_price()
  utils/
    waiting.py                 wait_until(): ждать условие с таймаутом (polling)
    money.py                   to_decimal(), format_amount()
  fixtures/
    config.py                  settings, base_url
    data.py                    credentials, asset
    api.py                     api, auth_api, funded_user, create_order, make_user
    ui.py                      app, logged_user, new_app, order_factory, login_in_browser
  plugins/
    markers.py                 маркер слоя по папке теста
    reporting.py               шапка прогона, окружение в Allure, артефакты браузера
tests/
  unit/                        без стенда: проверяют сам фреймворк (wait_until, money)
  api/                         HTTP и WebSocket к стенду
  ui/                          браузер
  e2e/                         данные через API, проверка в браузере
.github/
  actions/setup/action.yml     общая подготовка джобы: uv, браузер, стенд
  workflows/                   pr, regression, nightly, manual, allure-report
```

- **Почему `fixtures/` и `plugins/` внутри `framework/`, а не в `tests/conftest.py`.** Фикстуры — часть
  фреймворка: их переиспользуют все папки тестов. Один корневой `conftest.py` только подключает их
  списком `pytest_plugins` (pytest разрешает этот список только в корневом conftest).
- **Почему `data/` и `utils/` общие.** Пользователь, деньги и ожидания одинаковы для API и UI — один
  генератор и один `wait_until` вместо двух копий, которые со временем начинают отличаться.
- **Почему модели в `api/models`.** Это форма запросов и ответов API. UI-тест может брать `CreateOrder`
  как набор данных ордера — это нормально: UI зависит от API-слоя, не наоборот.

**Было → стало** (уроки в `practice/` написаны до объединения и ссылаются на старые пути):

| Было | Стало |
|---|---|
| `framework/transport/api_client.py`, `reporting.py` | `framework/api/client.py`, `framework/api/reporting.py` |
| `framework/app.py`, `services/`, `models/`, `contract.py` | `framework/api/app.py`, `api/services/`, `api/models/`, `api/contract.py` |
| `framework/envs/*.env` | `framework/config/envs/*.env` |
| `framework/waiter.py` | удалён → `framework/utils/waiting.py` (`wait_until`) |
| `ui_framework/application.py`, `pages/`, `components/` | `framework/ui/application.py`, `ui/pages/`, `ui/components/` |
| `ui_framework/config/settings.py` | один `framework/config/settings.py` |
| `ui_framework/data/generators.py`, `utils/` | `framework/data/generators.py`, `framework/utils/` |
| `ui_framework/fixtures/app.py`, `plugins/reporting.py` | `framework/fixtures/ui.py`, `framework/plugins/reporting.py` |
| `ui_framework/api/client.py` (`ExchangeApi`, `create_api`) | удалён → API-слой `framework/api` и фикстура `auth_api` |
| `ui_framework/data/models.py` (`OrderData`) | удалён → `framework/api/models/order.py` (`CreateOrder`, свойство `cost`) |
| `tests/conftest.py`, `tests/ui/conftest.py` | удалены → `framework/fixtures/*`, `framework/plugins/*` |
| `test_browser_logged_in_by_token` в `tests/ui` | `tests/e2e/test_login_by_token.py` |

---

## 3. Путь одного API-теста от начала до конца

```python
# tests/api/test_orders.py
@pytest.mark.smoke
def test_create_order(auth_api):
    auth_api.balances.deposit('USDT', 100)
    order = auth_api.orders.create(CreateOrder())

    assert order.status_code == 201
    Order.model_validate(order.json())
```

Что происходит, когда ты пишешь `uv run pytest -k test_create_order`:

1. **pytest читает `pyproject.toml`**: где тесты (`testpaths`), какие маркеры разрешены, `addopts`.
2. **Корневой `conftest.py`** подключает плагины из `pytest_plugins`: фикстуры и хуки фреймворка.
3. **`plugins/markers.py`** видит, что файл лежит в `tests/api`, и ставит тесту маркер `api`.
4. **pytest строит цепочку фикстур** по аргументам теста: `auth_api` ← `api` + `credentials`,
   `api` ← `settings`.
5. **`settings`** (scope session) → `get_settings()`: читает `ENV`, файл `config/envs/dev.env`,
   переменные окружения. Создаётся один раз на весь прогон.
6. **`api`** создаёт `ApiClient(base_url, timeout)` и фасад `Api`.
7. **`credentials`** генерирует уникальные email и пароль.
8. **`auth_api`** регистрирует и логинит пользователя (`sign_in`), кладёт токен в сессию клиента и отдаёт
   `Api` тесту (`yield`).
9. **Тест** вызывает `auth_api.orders.create(CreateOrder())` → `OrderService.create` собирает тело из
   модели и заголовок `Idempotency-Key` → `ApiClient.post("/orders", ...)` → `ApiClient.request`.
10. **`ApiClient.request`**: подставляет таймаут, открывает шаг Allure `POST /orders`, шлёт запрос через
    `Session` (с `Accept` и `Authorization`), вызывает `report(response)` — строка в лог и вложения в Allure.
11. **Тест проверяет** статус и тело (модель `Order` падает, если поле пропало или поменяло тип).
12. **Teardown `auth_api`** (код после `yield`) отменяет открытые ордера пользователя — даже если тест
    упал. Потом teardown `api` закрывает сессию.

- **Тест не знает ни URL, ни заголовков, ни токена** — только «пополни» и «создай ордер».
- **Уборка — в фикстуре, а не в тесте**: выполнится при любом исходе теста.

---

## 4. Путь UI-теста

```python
# tests/ui/test_user_workflows.py
@pytest.mark.balance(USDT='1000')
def test_place_order_with_enough_balance(logged_user):
    order_data = CreateOrder(price='100.5', quantity='2')
    dashboard = logged_user.dashboard_page

    response = dashboard.order_form.place(order_data.side, order_data.price, order_data.quantity, order_data.symbol)

    assert response.ok, response.text()
    expect(dashboard.balances.locked('USDT')).to_have_text(format_amount(order_data.cost))
```

1. **`page`** — фикстура pytest-playwright: браузер → контекст → вкладка. `base_url` для `page.goto`
   берётся из нашей фикстуры `base_url`.
2. **`app`** (`fixtures/ui.py`) ставит таймаут действий из настроек и создаёт фасад `Application`.
3. **`logged_user`** регистрирует пользователя через форму и ждёт кабинет. Маркер
   `@pytest.mark.balance(USDT='1000')` — пополнить баланс перед тестом.
4. **Тест** работает через страницы и компоненты: `dashboard_page.order_form.place(...)` заполняет форму,
   нажимает кнопку и **возвращает ответ сервера** (`Response`) — статус проверяет тест.
5. **`expect(...)`** ждёт, пока текст в ячейке станет нужным (таймаут — `expect_timeout_ms`).
6. **При падении** `plugins/reporting.py` прикладывает в Allure URL, скриншот, видео и trace.

- **Методы PO не возвращают другие страницы** и не проверяют статус: один метод `place` годится для
  позитива и негатива.
- **Локаторы — по `data-testid` и ролям**, текст кнопок — как видит пользователь.

---

## 5. e2e: API готовит, UI проверяет

```python
# tests/e2e/test_login_by_token.py
def test_api_deposit_visible_in_ui(auth_api, credentials, login_in_browser):
    auth_api.balances.deposit("USDT", "25.5")                 # быстро, через API

    app = login_in_browser(auth_api, credentials["email"])    # браузер сразу залогинен

    expect(app.dashboard_page.balances.available("USDT")).to_have_text("25.5")
```

- **Зачем.** Регистрация и пополнение через форму — 3–5 секунд и лишние шансы упасть не там. Через API —
  доли секунды. В браузере проверяем только то, ради чего тест.
- **Как работает `login_in_browser`.** Фронт стенда хранит токен в `localStorage`. Фикстура создаёт
  контекст браузера с `storage_state`, где уже лежит токен API-клиента (`api.client.token`) — страница
  открывается сразу в кабинете.
- **Это и есть польза одного фреймворка:** e2e-тесту нужны оба слоя сразу.

---

## 6. Настройки и окружения

```python
# framework/config/settings.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENVS_DIR / f"{os.getenv('ENV', 'dev')}.env", extra="ignore")
    base_url: str = "http://localhost:8080"
    timeout: float = 10
    expect_timeout_ms: int = 5_000
    ...

@cache
def get_settings() -> Settings: ...
```

- **Откуда значение (выигрывает верхнее):** переменная окружения процесса (`BASE_URL=... uv run pytest`) →
  файл `config/envs/<ENV>.env` → значение по умолчанию в классе.
- **Другое окружение без правки кода:** `ENV=stage uv run pytest` (stage — `docker compose --profile stage up -d`).
- **`get_settings()` с `@cache`** — объект создаётся при первом обращении и один на весь прогон. Раньше
  настройки создавались при импорте модуля и печатали путь `print`-ом.
- **`ws_url`** вычисляется из `base_url` (`http` → `ws`), поэтому WebSocket-тест работает на любом окружении.
- **Секреты** (пароли, ключи) в env-файлы репозитория не кладут — только через переменные окружения или
  секреты CI.

---

## 7. API-слой подробно

### 7.1 ApiClient — транспорт

```python
class ApiClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.session = Session()
        self.session.headers.update({"Accept": "application/json"})
        self.session.mount("http://", HTTPAdapter(max_retries=SAFE_RETRY))
        self.session.mount(f"{self.base_url}/orders", HTTPAdapter(max_retries=ORDERS_RETRY))

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        with allure.step(f"{method} {path}"):
            response = self.session.request(method, self.base_url + path, **kwargs)
            report(response)
        return response
```

- **Один `request` — единственная точка выхода в сеть.** `get/post/patch/delete` — тонкие обёртки. Хочешь
  добавить замер времени, curl в отчёт или трейс — меняешь одно место.
- **`Session`** держит соединения открытыми (быстрее) и хранит общие заголовки: `Accept` и токен.
- **`timeout` всегда.** У `requests` таймаута по умолчанию нет — зависший сервис подвесил бы прогон.
- **Ретраи только там, где повтор безопасен.** `SAFE_RETRY` повторяет GET, DELETE и другие безопасные
  методы на 502/503/504 (и уважает `Retry-After`). POST по умолчанию не повторяется: в режиме сбоев стенд
  падает уже после обработки запроса, и повтор зачислил бы депозит дважды. Исключение — `POST /orders`:
  у него `Idempotency-Key`, сервис отбросит повтор, поэтому для префикса `/orders` смонтирован
  `ORDERS_RETRY`. `requests` выбирает адаптер по самому длинному совпадающему префиксу URL.
- **Токен:** `set_token()` кладёт `Authorization: Bearer ...` в заголовки сессии и запоминает `client.token`
  (его берёт `login_in_browser`); `clear_token()` — для негативных тестов.

### 7.2 Сервисы и фасад

```python
class OrderService:
    def create(self, order: CreateOrder, exclude=None) -> Response:
        return self.client.post("/orders", json=order.model_dump(exclude=exclude),
                                headers={"Idempotency-Key": str(uuid4())})
```

- **Один класс — один ресурс API, один метод — один эндпоинт.** Знает путь и тело, больше ничего.
- **Возвращает `Response`, не `.json()` и не проверяет статус** — негативный тест пользуется тем же методом.
- **Фасад `Api`** собирает сервисы в один объект: `api.auth`, `api.balances`, `api.orders` — тесту хватает
  одной фикстуры.

### 7.3 Модели и контракт

- **Модели запросов** (`CreateOrder`) — тело с разумными умолчаниями: `CreateOrder(price="7.77")` меняет
  одно поле. `exclude={"price"}` — отправить тело без поля для негативного теста.
- **Модели ответов** (`Order`, `Balance`, `Profile`) — точные типы (UUID, Decimal, datetime, Literal) и
  `extra="forbid"`: тест падает, если API добавил, убрал поле или поменял тип.
- **Деньги — Decimal.** `Balance.available == Decimal("200")`, а не строка и не float.
- **`assert_matches_schema(data, "OrderOut")`** — сверка с OpenAPI самого сервиса: ловит расхождение кода и
  документации.

### 7.4 Отчёт по запросу

- **В лог:** метод, URL, статус, время, `X-Request-ID`. По `request_id` строка ищется в логах стенда:
  `docker compose logs exchange | grep <id>`.
- **В Allure:** шаг `POST /orders`, тело запроса и ответа. Значения `password`, `access_token`,
  `refresh_token`, `secret`, `signature` заменяются на `***`.

---

## 8. UI-слой подробно

```python
class Application:
    def __init__(self, page):
        self.auth_page = AuthPage(page)
        self.dashboard_page = DashboardPage(page)

class DashboardPage(BasePage):
    path = "/app/"
    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)
        self.balances = BalancesTable(page)
        self.deposit_form = DepositForm(page)
        self.order_form = OrderForm(page)
        self.orders = OrdersTable(page)
```

- **`Application`** — фасад: тест работает с `app.dashboard_page`, а не создаёт страницы сам.
- **`BasePage`** — общее для страниц: `path`, `open()`, тост.
- **Страница = композиция компонентов.** Форма ордера, таблица балансов, шапка — отдельные классы; одна и
  та же таблица переиспользуется на разных страницах.
- **Действие, которое шлёт запрос, ждёт ответ сервера** (`page.expect_response`) и возвращает его — так тест
  не гадает, «успел ли UI», и проверяет статус.
- **`Table`** ищет колонку по тексту заголовка — тест не ломается, если колонки поменяли местами.

---

## 9. Данные и изоляция

- **Уникальный пользователь на тест** (`credentials()` → `user_<uuid>@test.io`). Тесты не делят состояние и
  идут параллельно: `uv run pytest -n 4`.
- **Стакан ордеров общий для всех.** Поэтому: уборка открытых ордеров после теста (`auth_api`, `make_user`,
  `order_factory`) и `isolated_price()` — цена из «своего» диапазона, чтобы ордер не исполнился о чужой.
- **Фабрики** (`make_user`, `new_app`, `create_order`, `order_factory`) — когда в тесте нужно несколько
  объектов. Фабрика запоминает всё созданное и убирает за всеми.
- **Подготовка через API, проверка — там, что тестируем.** В UI-тесте депозит можно сделать через форму, а
  можно маркером `balance`; в e2e — через API.

---

## 10. Фикстуры: что есть и когда брать

| Фикстура | Scope | Что даёт | Уборка |
|---|---|---|---|
| `settings`, `base_url` | session | настройки окружения | — |
| `credentials` | function | `{"email", "password"}` нового пользователя | — |
| `api` | function | `Api` без токена: регистрация, логин, негатив авторизации | закрыть сессию |
| `auth_api` | function | `Api` залогиненного пользователя | отменить его открытые ордера |
| `funded_user` | function | `auth_api` + 100 USDT | как у `auth_api` |
| `create_order` | function | фабрика ордеров для `funded_user` | как у `auth_api` |
| `make_user` | function | фабрика отдельных залогиненных пользователей | ордера всех + сессии |
| `app` | function | `Application` на вкладке `page` | браузер закрывает pytest-playwright |
| `logged_user` | function | `app` с зарегистрированным пользователем, маркер `balance` | — |
| `new_app` | function | фабрика пользователей в отдельных контекстах браузера | — |
| `order_factory` | function | фабрика ордеров через форму | отменить созданные ордера |
| `login_in_browser` | function | открыть кабинет по токену `Api` | — |

- **Фикстура готовит состояние, проверку делает тест.** `assert` в фикстуре — только «подготовка не удалась»
  с понятным текстом, чтобы отличать сломанную подготовку от упавшего теста.
- **Код после `yield` — teardown**: выполняется и после упавшего теста.

---

## 11. Плагины и утилиты

- **`plugins/markers.py`** — маркер слоя по папке: файл в `tests/api` получает `api`. Поэтому
  `uv run pytest -m api` работает без ручных маркеров.
- **`plugins/reporting.py`**: шапка прогона (`env dev, base_url ...`), `environment.properties` в Allure,
  глобальный таймаут `expect`, URL и артефакты браузера при падении.
- **`utils/waiting.py` — `wait_until(condition, timeout, interval, message, ignore)`**: ждать, пока условие
  станет истинным (например, ордер исполнится — сопоставление на стенде идёт в фоне). `condition` —
  функция, её вызывают на каждой попытке; `ignore` — исключения, которые значат «ещё нет».
- **`utils/money.py`** — `to_decimal` и `format_amount` (как UI показывает суммы: `100.50` → `100.5`).

---

## 12. Тесты: уровни, маркеры, запуск

- **unit** — без стенда, секунды: проверяют сам фреймворк. **api** — HTTP/WS к стенду. **ui** — браузер.
  **e2e** — оба слоя. **smoke** — несколько ключевых сценариев, гоняются на каждый PR.

```bash
docker compose up -d                       # стенд
uv run pytest                              # всё
uv run pytest -m unit                      # слой
uv run pytest -m "api or e2e"              # несколько слоёв
uv run pytest -m smoke                     # ключевые сценарии
uv run pytest tests/api/test_orders.py -k cancel
uv run pytest -n 4                         # параллельно (pytest-xdist)
ENV=stage uv run pytest -m smoke           # другое окружение
uv run pytest --headed --slowmo 300 -m ui  # смотреть браузер
uv run pytest --alluredir=allure-results && allure serve allure-results
```

---

## 13. CI: проверки по уровням

```text
pr.yml          каждый Pull Request:   lint → unit → api → ui-smoke        (гейт merge)
regression.yml  после merge в main:     unit+api → ui+e2e (Chromium) → Allure-отчёт
nightly.yml     каждую ночь 02:00 UTC:  unit+api ‖ ui+e2e × [chromium, firefox, webkit] → отчёт
manual.yml      кнопка Run workflow:    выбрать suite (smoke/regression), layer, browser
allure-report.yml  переиспользуемый: сливает allure-results всех джоб в один HTML
actions/setup      composite action: uv + зависимости, браузер, стенд (docker compose + /health)
```

- **Пирамида во времени:** чем быстрее проверка, тем раньше она бежит. Линтер — секунды, unit — секунды,
  API — минута, UI — минуты, три браузера — ночью. Падение на раннем шаге останавливает дальнейшие
  (`needs:`), чтобы не тратить время.
- **Гейт PR:** в настройках репозитория (Settings → Branches → main) отметить required checks `lint`,
  `unit`, `api`, `ui-smoke` — без зелёных проверок кнопка merge закрыта.
- **Стенд в CI поднимается из кода этого же коммита** (`docker compose up -d --build`) — тесты проверяют
  ровно то, что мержится.
- **`PYTEST_ADDOPTS: -o addopts=-ra`** — в `pyproject.toml` стоит `--browser-channel chrome` для macOS 12;
  в CI его сбрасываем и берём браузеры Playwright.
- **Артефакты** (`if: always()`): `allure-results`, `test-results` (скриншоты, видео, trace) — они нужнее
  всего, когда тест упал. При падении в лог джобы печатаются логи стенда.
- **`concurrency`** — новый пуш в ту же ветку отменяет старый прогон.
- **`fail-fast: false`** в матрице — упал Firefox, остальные браузеры всё равно доезжают.
- **Composite action vs reusable workflow.** Action — набор шагов внутри джобы (подготовка), reusable
  workflow (`workflow_call`) — целые джобы (отчёт). Оба убирают копипасту.

**Как разбирать красный CI:** открыть джобу → упавший тест в логе pytest → скачать артефакт → trace
(`uv run playwright show-trace trace.zip`) или Allure → `X-Request-ID` из лога клиента → строка в логах
стенда, напечатанных в джобе.

---

## 14. Как добавить новое

- **Новый эндпоинт** (например, `GET /me` уже есть, добавим `PATCH /me`): метод в сервисе
  (`AuthService.update_me(display_name)` → `self.client.patch("/me", json=...)`), модель ответа в
  `api/models`, тест в `tests/api`. Клиент и фикстуры не меняются.
- **Новый ресурс** (`/webhooks`): `api/services/webhooks.py` с классом `WebhookService`, строчка в фасаде
  `Api`, модели, тесты.
- **Новая страница:** класс в `ui/pages` от `BasePage` с `path`, компоненты в `ui/components`, атрибут в
  `Application`.
- **Новое окружение:** файл `config/envs/<name>.env` с `BASE_URL`, запуск `ENV=<name> uv run pytest`.
- **Новый smoke-сценарий:** `@pytest.mark.smoke` на тест — он попадёт в PR-проверку.

---

## 15. Частые ошибки

- `requests.post(...)` или `page.goto("http://...")` прямо в тесте — слой нарушен, URL размножается.
- `assert` статуса внутри сервиса или метода PO — негативный тест невозможен.
- Нет таймаута у HTTP-клиента; ретраи на POST без идемпотентности — задвоенные данные и спрятанные баги.
- Общий пользователь на несколько тестов — тесты влияют друг на друга, параллельный прогон ломается.
- Уборка в конце теста, а не в фикстуре после `yield` — при падении не выполнится.
- Две копии настроек, клиентов или генераторов — со временем расходятся (так было до объединения).
- `time.sleep(3)` вместо `expect(...)` или `wait_until(...)`.
- Секреты в отчёте или в env-файлах репозитория.

---

## 16. Локальная среда: если стенд «тормозит»

На macOS 12 с Docker Desktop запись на диск в контейнере иногда замедляется, и каждый `COMMIT` в Postgres
ждёт секунды (видно в Jaeger: span `COMMIT;` на десятки секунд). Тесты тогда падают с `ReadTimeout` или
не дожидаются кабинета. Лечение для локального стенда:

```bash
docker compose restart db exchange
docker compose exec -T db psql -U exchange -c "ALTER SYSTEM SET synchronous_commit = off;" -c "SELECT pg_reload_conf();"
```

`synchronous_commit = off` — база не ждёт сброса на диск при каждом коммите. Для тестового стенда это
безопасно (при падении контейнера теряются последние доли секунды данных). Настройка живёт до пересоздания
контейнера (`docker compose down`).

---

### Собес

- **Как устроен ваш фреймворк?** Один репозиторий и пакет: ядро (настройки, данные, ожидания, фикстуры,
  отчёты) и два слоя — API на requests (клиент → сервисы → фасад, pydantic-модели) и UI на Playwright
  (Page Object с компонентами и фасадом Application). Тесты по уровням: unit, api, ui, e2e; e2e готовит
  данные через API и проверяет в браузере.
- **Почему API и UI в одном фреймворке?** Общие пользователи, данные, настройки и отчёты пишутся один раз;
  можно делать e2e; один CI и один Allure. Отдельные репозитории — когда разные команды и стек.
- **Где проверяется статус ответа?** В тесте. Клиент и PO возвращают `Response`, поэтому позитив и негатив
  используют одни методы.
- **Как изолированы тесты?** Уникальный пользователь на тест, уборка в фикстурах после `yield`, свой диапазон
  цен для общего стакана, параллельный прогон через xdist.
- **Как работаете с окружениями?** pydantic-settings: env-файл по `ENV` + переменные окружения; один и тот же
  набор идёт на local, stage, CI без правки кода.
- **Как устроены ретраи?** Только безопасные методы на 5xx с `Retry-After`; POST — только с идемпотентным
  ключом. Иначе ретраи прячут баги и задваивают данные.
- **Как устроен CI?** На PR — линтер, unit, API, UI smoke как обязательные проверки; после merge — полная
  регрессия с Allure-отчётом; ночью — UI в трёх браузерах; ручной запуск с выбором набора. Стенд
  поднимается из кода коммита, артефакты сохраняются всегда.
- **Как разбираете падение?** Allure: шаги, тела запросов (секреты замаскированы), скриншот, видео, trace;
  `X-Request-ID` из лога → строка в логах сервиса и трейс в Jaeger.
