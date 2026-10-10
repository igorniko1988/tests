# U5. Урок 1 — API внутри Playwright

Задания: `practice/tasks/test_u5_01_api_in_playwright.py`, решение — `tests/ui/test_u5_01_api_in_playwright.py` (создаёшь сам), код — `ui_framework/api/`.

План: зачем UI-тестам API; `APIRequestContext` — откуда взять и чем отличаются варианты; запросы
и ответы; авторизация на стенде; тонкий API-клиент; подготовка через API → проверка в UI
(как «залогинить» браузер токеном); проверка UI-действия через API; уборка через API; ретраи
с ключом идемпотентности; ловушки.

Модуль U5: U5.1 API внутри Playwright → U5.2 тестовые данные → U5.3 storage_state, роли, изоляция
и параллельный запуск → U5.4 собес.

---

## 1. Зачем UI-тесту API

Тест «отмена ордера» через UI: регистрация (форма), пополнение (форма), ордер (форма), отмена,
проверки. Проверяется только **отмена** — всё остальное подготовка, которая:
- **медленная**: каждый шаг через UI — секунды (задача 5 — замерь сам);
- **хрупкая**: упала форма пополнения — упал тест про отмену, хотя отмена работает;
- **дублирует** тесты, которые уже проверяют регистрацию и пополнение.

Правило: **через UI — то, что тест проверяет; всё остальное — через API**. Плюс уборка через API.

---

## 2. APIRequestContext: три способа получить

| Способ | Что это | Cookies браузера |
|---|---|---|
| `playwright.request.new_context(base_url=...)` | отдельный HTTP-клиент | свои, не связаны с браузером |
| `context.request` / `page.request` | клиент, привязанный к BrowserContext | **общие** с context: логин через API логинит и браузер (если сессия на cookie) |
| (JS) фикстура `request` | в `@playwright/test` для JS | — |

Ловушка Python: в pytest **`request` — это объект pytest** (`FixtureRequest`, U4.3), а не HTTP-клиент.
В pytest-playwright для Python готовой фикстуры API-клиента нет — создаёшь сам из `playwright.request`.

```python
@pytest.fixture(scope="session")
def api_context(playwright, base_url):
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()                      # закрыть соединения
```

Почему не `requests`/`httpx`: можно и так. Плюсы Playwright-клиента — тот же `base_url`, прокси,
сертификаты, что у браузера; `context.request` делит cookies; запросы видны в trace (U7).

---

## 3. Запросы и ответы

```python
r = api.post("/auth/register", data={"email": email, "password": "password123"})
r = api.get("/orders", params={"status": "NEW"}, headers={"Authorization": f"Bearer {token}"})
r = api.delete(f"/orders/{order_id}", headers=auth)
r = api.fetch("/orders", method="POST", data={...})
```

| Параметр | Что |
|---|---|
| `data=` | тело: **dict → JSON** (и `Content-Type: application/json`), строка/bytes — как есть |
| `form=` | `application/x-www-form-urlencoded` |
| `multipart=` | файлы и поля формы |
| `params=` | query-параметры |
| `headers=` | заголовки запроса |
| `timeout=` | мс, по умолчанию 30 000 |
| `fail_on_status_code=True` | бросить исключение на не-2xx/3xx |

Ответ (`APIResponse`): `status`, `ok`, `headers`, `json()`, `text()`, `body()`, `url`.

Заголовки на весь клиент: `playwright.request.new_context(base_url=..., extra_http_headers={...})`.

### Ловушка `base_url` с путём

`base_url="http://host/api"` + `api.get("/orders")` → `http://host/orders`: путь с ведущим `/`
**заменяет** путь из base_url (правила URL). Для base_url с путём — слеш в конце и относительный путь:
`base_url="http://host/api/"`, `api.get("orders")`. У нашего стенда base_url без пути — проблемы нет.

---

## 4. Авторизация на стенде

JWT Bearer, живёт **15 минут** (`access_token_ttl_seconds = 900`):

```python
token = api.post("/auth/login", data={"email": email, "password": pw}).json()["access_token"]
auth = {"Authorization": f"Bearer {token}"}
api.post("/balances/deposit", data={"asset": "USDT", "amount": "1000"}, headers=auth)
```

Без токена: `401 {"error": {"code": "unauthorized", "message": "Missing bearer token"}}`.

**`page.request` тут не поможет**: стенд хранит токен в localStorage, а не в cookie, и `page.request`
его не знает — проверено: `page.request.get("/balances")` в залогиненном браузере даёт 401.
На сайтах с cookie-сессией всё наоборот: `context.request.post("/login")` залогинит и браузер.

---

## 5. Тонкий API-клиент

UI-фреймворку не нужен полноценный API-фреймворк (он будет в части API курса). Достаточно
клиента для подготовки и уборки:

```python
class ExchangeApi:
    def __init__(self, ctx: APIRequestContext, token: str | None = None):
        self.ctx = ctx
        self.token = token

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _check(self, r: APIResponse) -> dict | list:
        if not r.ok:
            raise AssertionError(f"{r.url} → {r.status}: {r.text()}")
        return r.json()

    def register(self, email: str, password: str) -> dict:
        return self._check(self.ctx.post("/auth/register", data={"email": email, "password": password}))

    def login(self, email: str, password: str) -> str:
        self.token = self._check(self.ctx.post("/auth/login", data={...}))["access_token"]
        return self.token

    def deposit(self, asset: str, amount: str) -> dict: ...
    def place_order(self, side, price, quantity, symbol="ETH-USDT") -> dict: ...
    def cancel_order(self, order_id: str) -> dict: ...
    def orders(self, status: str | None = None) -> list[dict]: ...
    def balances(self) -> list[dict]: ...
```

- падает с понятным сообщением на не-2xx (URL, статус, тело) — подготовка не должна молча не сработать;
- для негативных API-проверок — отдельные методы или сырой `ctx` (как `deposit_expecting_error` в U4.1);
- принимает данные из моделей (`OrderData` из U4.4).

---

## 6. Подготовка через API → проверка в UI

Пользователь создан и пополнен через API. Как открыть **браузер** уже залогиненным? Фронтенд
при загрузке читает `localStorage["token"]` и `["email"]` (`app.js`). Значит, нужно положить их
в localStorage **до** загрузки страницы.

### Через storage_state (рекомендуется)

```python
def logged_in_context(new_context, base_url, token, email):
    state = {
        "cookies": [],
        "origins": [{
            "origin": base_url,                              # http://localhost:8080
            "localStorage": [
                {"name": "token", "value": token},
                {"name": "email", "value": email},
            ],
        }],
    }
    return new_context(storage_state=state)


page = logged_in_context(new_context, base_url, api.token, email).new_page()
DashboardPage(page).open().wait_loaded()                     # сразу кабинет, без формы входа
```

`storage_state` — тот же формат, что `context.storage_state()` возвращает (U1.4). Можно собрать его
руками, не логинясь через UI ни разу. `origin` — схема, хост и порт (путь Playwright отбрасывает сам).

Проверено на стенде: с этим state `/app/` сразу открывает кабинет; с мусорным токеном фронт получает 401
на `/balances`, сам разлогинивается и чистит localStorage — так можно тестировать «токен истёк».

### Через add_init_script (хуже)

```python
context.add_init_script(f"localStorage.setItem('token', '{token}')")
```

Скрипт выполняется **при каждой** загрузке страницы. Тест нажал «Выйти», сделал `reload` — и снова
залогинен (проверено на стенде). Тест логаута становится невозможным, поведение неочевидно.

### Через UI-логин (медленно)

Один логин через форму — нормально для теста **логина**. Для остальных — API + storage_state.

### После API-действия UI обновится не сразу

UI опрашивает сервер раз в 2 с (U2.1). Отменил ордер через API, пока страница открыта, — `expect`
дождётся следующего опроса. Либо `page.reload()`, если опроса нет.

---

## 7. Действие в UI → проверка через API

Когда уместно:
- проверить то, чего **нет на экране**: точные значения, поля, которые UI не показывает;
- убедиться, что UI отправил правильные данные **и** сервер их сохранил — `expect_request` (U2.1)
  проверяет только отправку;
- отличить баг фронта от бэка: сервер сохранил верно, а UI показывает не то.

```python
order = dashboard.order_form.place("BUY", "100.50", "0.5")
saved = api.orders()[0]
assert saved["price"] == "100.5"               # сервер нормализует (U4.4)
```

Не заменяй этим проверки экрана: UI-тест проверяет то, что видит пользователь.

---

## 8. Уборка через API

```python
@pytest.fixture
def api_user(api_context, settings):
    users: list[ExchangeApi] = []

    def _create() -> tuple[str, ExchangeApi]:
        email = unique_email()
        client = ExchangeApi(api_context)
        client.register(email, settings.user_password.get_secret_value())
        client.login(email, settings.user_password.get_secret_value())
        users.append(client)
        return email, client

    yield _create
    for client in users:                                       # отменить всё открытое — общий стакан!
        for status in ("NEW", "PARTIALLY_FILLED"):
            for order in client.orders(status):
                client.cancel_order(order["id"])
```

Через API уборка занимает миллисекунды, а не секунды, и не зависит от UI.
Удалить пользователя стенд не позволяет (нет такого API) — убираем то, что мешает другим: открытые ордера.

---

## 9. Ретраи подготовки и ключ идемпотентности

На stage 5% запросов — 503, половина после обработки (U2.4). Подготовка через API тоже может упасть.
- **GET** повторять безопасно;
- **POST** без защиты повторять опасно: ответ потерялся, а ордер создан — повтор создаст второй;
- у стенда `POST /orders` поддерживает заголовок **`Idempotency-Key`**: повтор с тем же ключом
  вернёт **тот же** ордер, а не создаст новый.

```python
key = str(uuid4())
for attempt in range(3):
    r = api.post("/orders", data=order, headers={**auth, "Idempotency-Key": key})
    if r.status != 503:
        break
```

Пополнение (`/balances/deposit`) ключ не поддерживает — его повтор после потерянного ответа задвоит сумму.
Подробно идемпотентность — в части API курса.

---

## 10. Ловушки

| Ловушка | Что будет |
|---|---|
| `request` как HTTP-клиент в Python | это `FixtureRequest` pytest |
| `page.request` на стенде с токеном в localStorage | 401 |
| `add_init_script` для логина | тест логаута не работает |
| забыли `dispose()` | висящие соединения до конца процесса |
| токен в session-фикстуре на долгий прогон | через 15 минут 401 (U5.3) |
| повтор POST без ключа идемпотентности | задвоение данных |
| проверка API вместо проверки UI | UI-баг пройдёт незамеченным |

---

## Собес: вопросы и ответы

**1. Зачем в UI-тестах API?**
> Чтобы через UI делать только то, что тест проверяет. Подготовку — пользователя, баланс, ордера —
> и уборку делаю через API: это в десятки раз быстрее, стабильнее, и тест не падает из-за чужой формы.
> Плюс API помогает проверить то, чего нет на экране, и отличить баг фронта от бэка.

**2. Как сделать API-запрос из Playwright на Python?**
> `playwright.request.new_context(base_url=...)` — отдельный клиент; `page.request` / `context.request` —
> клиент, который делит cookies с браузером. Методы get, post, delete, fetch; `data` со словарём
> отправляется как JSON. Ответ — status, ok, json. Клиент закрываю через `dispose`. Важно: фикстура
> `request` в pytest — это объект pytest, а не HTTP-клиент, как в JS-версии.

**3. Как открыть браузер уже залогиненным, если пользователь создан через API?**
> Зависит от того, где сессия. Если в cookie — логин через `context.request` залогинит и браузер.
> Если токен в localStorage, как у нас, — собираю storage_state с origin и записями localStorage
> и создаю context с ним. `add_init_script` хуже: выполняется при каждой загрузке и ломает логаут.

**4. Когда проверять результат UI-действия через API?**
> Когда значение не видно на экране, когда нужно убедиться, что сервер сохранил то, что отправил UI,
> и чтобы локализовать баг — фронт или бэк. Но проверки экрана остаются: UI-тест про то, что видит пользователь.

**5. Как убираешь тестовые данные?**
> Через API в teardown фикстуры: фабрика запоминает созданное, после yield удаляю или отменяю.
> Уборка защитная — не падает на «уже удалено». Если удалить нельзя, как пользователя на нашем стенде,
> убираю то, что мешает другим тестам: открытые ордера в общем стакане.

**6. Подготовка через API падает на нестабильном стенде. Что делать?**
> Повторять безопасно только идемпотентные запросы: GET и запросы с ключом идемпотентности. POST без
> ключа повторять нельзя — если ответ потерялся после обработки, повтор задвоит данные. Если API
> поддерживает Idempotency-Key — генерирую ключ на операцию и повторяю с ним.
