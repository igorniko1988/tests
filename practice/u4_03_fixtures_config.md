# U4. Урок 3 — фикстуры страниц и конфиг окружений

Задания: `tests/ui/test_u4_03_fixtures_config.py`, код — `ui_framework/config/`, `ui_framework/fixtures/`.

Основы фикстур (scope, yield, conftest, `browser_context_args`) были в U1.4. Здесь — то, из чего
собирают фреймворк: фикстуры страниц, фабрики с уборкой, `request` и маркеры с данными,
параметризованные фикстуры, фикстуры в пакете фреймворка (`pytest_plugins`), конфиг окружений
на pydantic-settings, секреты, наборы тестов по маркерам.

---

## 1. Фикстуры страниц

```python
@pytest.fixture
def auth_page(page: Page) -> AuthPage:
    return AuthPage(page)


@pytest.fixture
def dashboard(auth_page: AuthPage, user_email: str, settings: Settings) -> DashboardPage:
    return auth_page.open().register(user_email, settings.user_password)
```

Тест просит **состояние**, а не шаги: `dashboard` — «я в кабинете нового пользователя».
Цепочка фикстур: `page` (плагин) → `auth_page` → `dashboard`. pytest сам выстроит порядок.

### Фабрика страниц

Когда в тесте нужно несколько пользователей (U1.4, `create_user`) — фабрика, возвращающая PO:

```python
@pytest.fixture
def new_dashboard(new_context, settings) -> Callable[[], DashboardPage]:
    def _create() -> DashboardPage:
        page = new_context().new_page()
        return AuthPage(page).open().register(unique_email(), settings.user_password)
    return _create
```

`new_context` из pytest-playwright сам закроет все созданные context после теста.

---

## 2. Уборка: yield, финализаторы, фабрики

```python
@pytest.fixture
def open_order(dashboard):
    dashboard.deposit_form.deposit("USDT", "100")
    order = dashboard.order_form.place("BUY", "1", "1")
    yield order                                        # тест работает здесь
    row = dashboard.orders.row(order["id"])            # teardown — даже если тест упал
    if row.cancel_button.count():                      # уже отменён тестом — пропускаем
        row.cancel()
```

Порядок: setup фикстур — от зависимостей к зависимым; teardown — **в обратном** порядке.
`dashboard` (и `page`) ещё живы в teardown `open_order`, потому что `open_order` от них зависит.

Здесь `count()` в `if` — нормально: это не проверка, а ветвление в уборке (U2.1).

### Фабрика с уборкой

```python
@pytest.fixture
def order_factory(dashboard):
    created: list[str] = []

    def _create(side="BUY", price="1", quantity="1") -> dict:
        order = dashboard.order_form.place(side, price, quantity)
        created.append(order["id"])
        return order

    yield _create
    for order_id in created:                           # убрать всё, что создали
        row = dashboard.orders.row(order_id)
        if row.cancel_button.count():
            row.cancel()
```

### Что если teardown упал

Тест прошёл, а уборка упала — pytest покажет **ERROR at teardown** (не FAILED). Если упали оба —
увидишь и FAILED, и ERROR. Уборку пишут защитно: не падать, если «уже убрано».

`request.addfinalizer(func)` — то же, что код после `yield`, но можно зарегистрировать
несколько функций по ходу. С `yield` читается проще — используй его.

### Зачем убирать, если пользователь каждый раз новый

Пользователь новый, но **стакан общий** (U1.4: наш SELL исполнился об чужой BUY).
Открытые ордера, оставленные тестами, мешают другим. Отменить свои — дешёвая гигиена.
Через UI это медленно; в U5 научимся убирать через API (`page.request`).

---

## 3. `request`: что знает фикстура о тесте

```python
@pytest.fixture
def dashboard(request, auth_page, user_email, settings):
    dash = auth_page.open().register(user_email, settings.user_password)
    marker = request.node.get_closest_marker("balance")      # @pytest.mark.balance(USDT="1000")
    if marker:
        for asset, amount in marker.kwargs.items():
            dash.deposit_form.deposit(asset, amount)
    return dash


@pytest.mark.balance(USDT="1000", ETH="2")
def test_buy(dashboard): ...
```

Маркер с данными — способ сказать фикстуре «подготовь вот так», не плодя `dashboard_with_usdt`,
`dashboard_with_eth`... Маркер `balance` нужно зарегистрировать (`--strict-markers`).

Полезное в `request`:

| | Что |
|---|---|
| `request.node` | текущий тест: `.name`, `.get_closest_marker(...)`, `.nodeid` |
| `request.param` | значение для параметризованной фикстуры |
| `request.config` | конфиг pytest: `.getoption("--headed")`, `.getini(...)` |
| `request.getfixturevalue("name")` | получить фикстуру по имени динамически |
| `request.addfinalizer(f)` | уборка |

---

## 4. Параметризованные фикстуры

```python
@pytest.fixture(params=["USDT", "BTC", "ETH"])
def asset(request) -> str:
    return request.param


def test_deposit(dashboard, asset):              # запустится 3 раза
    dashboard.deposit_form.deposit(asset, "1")
    expect(dashboard.balances.available(asset)).to_have_text("1")
```

Отличие от `@pytest.mark.parametrize`: параметр живёт в **фикстуре** — любой тест, который её
попросит, автоматически прогонится по всем значениям.

### `indirect=True` — параметр в фикстуру из теста

```python
@pytest.fixture
def funded_dashboard(request, dashboard):
    for asset, amount in request.param.items():
        dashboard.deposit_form.deposit(asset, amount)
    return dashboard


@pytest.mark.parametrize("funded_dashboard", [{"USDT": "1000"}, {"ETH": "5"}], indirect=True)
def test_something(funded_dashboard): ...
```

---

## 5. autouse — когда можно

`autouse=True` — фикстура выполняется для каждого теста в области видимости, без упоминания.

Нормально:
- **настройка окружения**, нужная всем: таймауты, `expect.set_options`, логирование, артефакты;
- **уборка общего состояния**, без которой тесты ломают друг друга.

Плохо:
- подготовка **данных** (логин, ордера): тесту, которому не нужно, — лишние секунды; читателю теста
  не видно, откуда состояние;
- autouse-фикстура, которая берёт `page`, — **каждый** тест в папке, даже API-тест, поднимет браузер.

```python
@pytest.fixture(autouse=True)
def _timeouts(page, settings):                    # у нас все тесты в tests/ui — UI, можно
    page.set_default_timeout(settings.action_timeout_ms)
```

---

## 6. Где живут фикстуры: иерархия conftest и `pytest_plugins`

```
tests/
  conftest.py              # общее для всех: settings, report header, pytest_plugins
  ui/
    conftest.py            # UI-специфичное, переопределения для UI
  api/
    conftest.py
ui_framework/
  fixtures/
    pages.py               # фикстуры страниц: auth_page, dashboard, new_dashboard
    data.py                # user_email, фабрики данных
```

Фикстуры фреймворка лежат **в пакете**, а не в conftest тестов: их можно переиспользовать
в другом репозитории. Подключение — в корневом `tests/conftest.py`:

```python
pytest_plugins = ["ui_framework.fixtures.pages", "ui_framework.fixtures.data"]
```

Правила:
- `pytest_plugins` — **только в корневом** conftest (во вложенных pytest запрещает);
- хуки `pytest_addoption`, `pytest_configure`, `pytest_report_header` — в корневом conftest или плагине;
- фикстура во вложенном conftest с тем же именем **перекрывает** внешнюю.

---

## 7. Конфиг окружений на pydantic-settings

Окружения стенда:

| ENV | Адрес | Что |
|---|---|---|
| `local` | http://localhost:8000 | `uvicorn --reload` без Docker |
| `docker` | http://localhost:8080 | `docker compose up` (по умолчанию) |
| `stage` | http://localhost:8081 | stage-профиль: своя база, 5% сбоев |

```python
# ui_framework/config/settings.py
import os
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENVS_DIR = Path(__file__).resolve().parents[2] / "envs"
ENV = os.getenv("ENV", "docker")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UI_",
        env_file=(ENVS_DIR / f"ui.{ENV}.env", ENVS_DIR / f"ui.{ENV}.local.env"),
        extra="ignore",
    )

    env: str = ENV
    base_url: str = "http://localhost:8080"
    user_password: SecretStr = SecretStr("password123")
    expect_timeout_ms: int = 5_000
    action_timeout_ms: int = 15_000
    matching_timeout_ms: int = 15_000
```

```
# envs/ui.stage.env                         — в git
UI_BASE_URL=http://localhost:8081
UI_EXPECT_TIMEOUT_MS=10000

# envs/ui.stage.local.env                   — НЕ в git (envs/*.local.env в .gitignore)
UI_USER_PASSWORD=...
```

Приоритет (от сильного к слабому): **переменная окружения** → `.local.env` → `.env` файл окружения →
значение по умолчанию в классе. Запуск:

```bash
uv run pytest tests/ui                      # docker
ENV=stage uv run pytest tests/ui -m smoke   # stage
UI_EXPECT_TIMEOUT_MS=20000 ENV=stage uv run pytest ...   # точечно перекрыть одно значение
```

### Связать с pytest-playwright

```python
@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def base_url(pytestconfig, settings) -> str:          # перекрываем фикстуру плагина pytest-base-url
    return pytestconfig.getoption("base_url") or settings.base_url
```

`--base-url` из командной строки всё ещё главнее — удобно для разового запуска. Строку
`base_url = ...` из `pyproject.toml` теперь можно убрать: адрес живёт в конфиге окружения.

Глобальный таймаут `expect`:

```python
def pytest_configure(config):
    expect.set_options(timeout=Settings().expect_timeout_ms)
```

В шапке отчёта — какое окружение:

```python
def pytest_report_header(config):
    s = Settings()
    return f"env: {s.env}, base_url: {s.base_url}"
```

### Секреты

- в коде и в git — **никогда**: пароли, токены, ключи;
- в CI — переменные окружения / secrets CI (`UI_USER_PASSWORD`);
- локально — `envs/*.local.env` (в `.gitignore`) или `.env`;
- `SecretStr`: в логах и `repr` печатается `**********`, значение — `.get_secret_value()`;
- не печатать секреты в Allure-шагах и логах.

---

## 8. Наборы тестов

```toml
[tool.pytest.ini_options]
addopts = "-ra --strict-markers --browser-channel chrome"
markers = [
    "smoke: быстрые критичные проверки, на каждый PR",
    "regression: полный набор, ночью",
    "slow: дольше 10 секунд",
    "balance(**assets): начальный баланс для фикстуры dashboard",
]
```

```bash
uv run pytest -m smoke
uv run pytest -m "regression and not slow"
```

Пометить целую папку или файл: `pytestmark = pytest.mark.regression` в начале модуля.
Опции по умолчанию — в `addopts`, но **не** клади туда `-m smoke`: кто-нибудь запустит
`pytest` и удивится, куда делись тесты.

---

## 9. Частые ошибки

| Ошибка | Чем плохо |
|---|---|
| адрес стенда в коде или в PO | не переключить окружение |
| пароль в `settings.py` / в env-файле в git | утечка секрета |
| session-фикстура зависит от `page` | `ScopeMismatch` (U1.4) |
| autouse-фикстура логинится | все тесты медленнее, состояние неочевидно |
| уборка падает, если «уже убрано» | ERROR at teardown на зелёном тесте |
| `pytest_plugins` во вложенном conftest | ошибка сборки |
| фикстура `dashboard_with_usdt_1000_and_eth_2` | взрыв числа фикстур — маркер с данными или indirect |
| `Settings()` создаётся в каждом тесте | лишняя работа; session-фикстура |

---

## Собес: вопросы и ответы

**1. Какие scope у фикстур и что когда используешь?**
> function — по умолчанию, для всего, что меняется: страница, пользователь, данные. class и module —
> для дорогой подготовки, общей для группы тестов, если тесты её не меняют. session — для того,
> что живёт весь прогон: браузер, конфиг, API-клиент, токен. Фикстура не может зависеть от фикстуры
> с более коротким scope. Чем шире scope, тем выше риск, что тесты начнут зависеть друг от друга.

**2. Как выполняется cleanup в фикстурах?**
> Код после `yield` — teardown, выполняется даже если тест упал. Teardown идёт в обратном порядке
> setup, поэтому зависимости ещё живы. Если упала уборка — pytest покажет ERROR at teardown.
> Уборку пишу защитно: не падать, если ресурс уже удалён. Для фабрик копим созданное в список
> и убираем всё после yield.

**3. Как запустить одни и те же UI-тесты на разных окружениях?**
> Конфиг на pydantic-settings: класс с настройками, значения из переменных окружения и env-файла
> окружения, выбранного переменной `ENV`. Фикстура `base_url` берёт адрес из конфига, `--base-url`
> из командной строки перекрывает. Таймауты тоже в конфиге — на медленном stage они больше.
> Запуск: `ENV=stage pytest -m smoke`.

**4. Где хранишь секреты?**
> Не в коде и не в git. В CI — секреты CI в переменных окружения. Локально — в `.local.env`
> или `.env`, которые в `.gitignore`. В конфиге — `SecretStr`, чтобы не печатался в логах и отчётах.

**5. Когда используешь autouse?**
> Для настройки, нужной всем тестам области: таймауты, логирование, сбор артефактов. Не для
> подготовки данных и не для логина — это делает тесты медленнее и прячет, откуда состояние.
> И осторожно с autouse, который берёт `page`: браузер поднимется даже в тестах, где он не нужен.

**6. Как передать фикстуре параметры из теста?**
> Маркер с данными — фикстура читает `request.node.get_closest_marker(...)`. Или `indirect=True`
> в parametrize — значение приходит в `request.param`. Так не нужно плодить фикстуры на каждую
> комбинацию данных.

**7. Где лежат фикстуры в твоём фреймворке?**
> Фикстуры фреймворка — страниц, данных, клиентов — в пакете фреймворка (`fixtures/`), подключаются
> через `pytest_plugins` в корневом conftest. Специфичное для набора тестов — в conftest этой папки.
> Так фреймворк можно переиспользовать, а conftest тестов остаётся маленьким.
