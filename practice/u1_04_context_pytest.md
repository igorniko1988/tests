# U1. Урок 4 — BrowserContext, ожидания и pytest для UI

Задания: `practice/tasks/test_u1_04_context_pytest.py`, решение — `tests/ui/test_u1_04_context_pytest.py` (создаёшь сам) и `tests/ui/conftest.py`.

План: что именно изолирует context и как этим пользоваться (два пользователя, сохранённый логин);
как Playwright ждёт перед каждым действием; pytest-часть — фикстуры, conftest, parametrize, маркеры
и настройка pytest-playwright под проект.

---

## 1. BrowserContext — что изолирует

Context — это отдельный «профиль браузера», как окно инкогнито. У каждого context свои:

| Что | Пример на стенде |
|---|---|
| cookies | сессия на cookie (у нас её нет, но на большинстве сайтов именно так) |
| localStorage / sessionStorage | **наш JWT-токен** лежит в `localStorage["token"]` |
| IndexedDB, кэш, service workers | |
| разрешения | геолокация, уведомления, буфер обмена |
| настройки | viewport, locale, timezone, user agent, геопозиция, offline, `base_url` |

Все context одного браузера работают в **одном процессе браузера**, поэтому создание context
стоит миллисекунды. Запуск нового браузера — около секунды. Отсюда схема pytest-playwright:
**один браузер на прогон, новый context на каждый тест**.

### Полезное API context

```python
context = browser.new_context(base_url="http://localhost:8080", locale="ru-RU")
page = context.new_page()
context.pages                         # все вкладки этого context

context.cookies()                     # прочитать cookies
context.add_cookies([{"name": "a", "value": "1", "url": "http://localhost:8080"}])
context.clear_cookies()

context.grant_permissions(["geolocation"])
context.set_geolocation({"latitude": 55.75, "longitude": 37.61})
context.set_offline(True)             # пропала сеть

context.storage_state(path="state.json")   # сохранить cookies + localStorage
context.close()
```

### Две вкладки в одном context

Вкладки одного context **делят** cookies и localStorage — как вкладки обычного браузера:

```python
page1 = context.new_page()
page1.goto("/app/")   # залогинились в page1
page2 = context.new_page()
page2.goto("/app/")   # page2 тоже залогинена: тот же localStorage
```

Новая вкладка, которую открыло приложение (`target="_blank"`), ловится так:

```python
with context.expect_page() as new_page_info:
    page.get_by_role("link", name="Открыть отчёт").click()
report = new_page_info.value
```

### Два пользователя — два context

Сценарии «покупатель и продавец», «админ и пользователь», «чат двух людей»:

```python
def test_two_users(browser):
    buyer_ctx = browser.new_context(base_url="http://localhost:8080")
    seller_ctx = browser.new_context(base_url="http://localhost:8080")
    buyer = buyer_ctx.new_page()
    seller = seller_ctx.new_page()
    ...
    buyer_ctx.close()
    seller_ctx.close()
```

Удобнее через фикстуру `new_context` из pytest-playwright: она передаёт в context все настройки
проекта (`base_url`, `--device`, видео) и сама закрывает context после теста:

```python
def test_two_users(new_context):
    buyer = new_context().new_page()
    seller = new_context().new_page()
```

---

## 2. storage_state — не логиниться в каждом тесте

`storage_state` — это JSON со всеми cookies и localStorage context:

```python
context.storage_state(path="auth.json")             # сохранить после логина
browser.new_context(storage_state="auth.json")      # новый context уже залогинен
```

Как это используют: логин делают **один раз** (через UI или, лучше, через API), сохраняют state,
а все тесты стартуют из залогиненного context. Экономия — несколько секунд на каждый тест.

Сохранение можно не писать на диск: `state = context.storage_state()` вернёт словарь, его тоже
можно передать в `new_context(storage_state=state)`.

Минусы, о которых спрашивают:
- тесты с одним пользователем делят его **данные** на сервере (ордера, балансы) — проверки
  должны это учитывать или пользователь должен быть свой;
- токен истекает — state нужно пересоздавать;
- тесты логина и логаута должны идти без сохранённого state.

Подробно (логин через API, state на сессию, на воркер) — в U5.

---

## 3. Как Playwright ждёт перед действием (actionability)

Перед каждым действием Playwright проверяет элемент и **ждёт**, пока все проверки пройдут
(или упадёт по таймауту, по умолчанию 30 с для действий):

| Проверка | Значит | Для каких действий |
|---|---|---|
| **Attached** | элемент есть в DOM | все |
| **Visible** | ненулевой размер, не `display:none` / `visibility:hidden` | click, fill, check, hover… |
| **Stable** | не двигается (анимация закончилась: два кадра подряд на месте) | click, check, hover… |
| **Receives events** | в точке клика именно он, а не оверлей/спиннер сверху | click, check, hover… |
| **Enabled** | нет `disabled` | click, fill, check, select_option |
| **Editable** | enabled и не `readonly` | fill, clear |

Пример на стенде: после клика «Разместить ордер» кнопка становится `disabled` до ответа сервера.
Если сразу кликнуть второй раз, Playwright **дождётся**, пока кнопка снова станет enabled.

Что видно в `DEBUG=pw:api`:

```
waiting for get_by_role("button", name="Войти")
  - locator resolved to <button type="submit" data-testid="login-button">Войти</button>
  - attempting click action
  - waiting for element to be visible, enabled and stable
  - element is visible, enabled and stable
  - scrolling into view if needed
  - performing click action
```

Обходы (использовать осознанно):

```python
loc.click(force=True)       # пропустить проверки (кроме attached) — когда оверлей «ложный»
loc.click(trial=True)       # только проверки, без клика — «можно ли кликнуть»
loc.click(timeout=5_000)    # свой таймаут
```

`force=True` — красный флаг на ревью: обычно маскирует настоящую проблему (кнопка перекрыта для пользователя тоже).

### Таймауты

| Что | По умолчанию | Как поменять |
|---|---|---|
| действия (`click`, `fill`…) | 30 с | `page.set_default_timeout(10_000)` / `context.set_default_timeout` |
| навигация (`goto`, `wait_for_url`) | 30 с | `page.set_default_navigation_timeout(...)` |
| `expect` | 5 с | `expect.set_options(timeout=...)`, `timeout=` в проверке |
| тест целиком | нет | плагин `pytest-timeout` |

### Итог: четыре механизма стабильности

1. **Ленивые локаторы** — элемент ищется заново при каждом действии, нет stale element.
2. **Actionability** — перед действием ждёт видимость, стабильность, enabled, отсутствие перекрытия.
3. **Web-first assertions** — `expect` повторяет проверку до таймаута.
4. **Strict mode** — локатор нашёл несколько элементов → ошибка, а не клик «по первому».

---

## 4. Фикстуры pytest — основа

Фикстура — функция с `@pytest.fixture`; тест получает её результат по имени аргумента.

```python
import pytest

@pytest.fixture
def user_email() -> str:
    return f"user_{uuid4().hex[:8]}@test.com"

def test_something(user_email):     # pytest вызвал user_email() и передал результат
    ...
```

### setup и teardown через yield

```python
@pytest.fixture
def second_page(context):
    page = context.new_page()      # setup — до теста
    yield page                     # тест работает здесь
    page.close()                   # teardown — после теста, даже если тест упал
```

### Scope — сколько живёт фикстура

| scope | создаётся | пример |
|---|---|---|
| `function` (по умолч.) | на каждый тест | `page`, `context` |
| `class` | на класс тестов | |
| `module` | на файл | |
| `session` | один раз на прогон | `browser`, `playwright`, `browser_context_args` |

Правило: фикстура **не может** зависеть от фикстуры с более коротким scope
(session-фикстура не может взять `page`) — будет `ScopeMismatch`.

### Фикстура от фикстуры

```python
@pytest.fixture
def logged_in_page(page, user_email) -> Page:    # берёт встроенную page и свою user_email
    page.goto("/app/")
    page.get_by_label("Email").fill(user_email)
    page.get_by_label("Пароль").fill("password123")
    page.get_by_role("button", name="Зарегистрироваться").click()
    expect(page.get_by_test_id("dashboard")).to_be_visible()
    return page

def test_dashboard(logged_in_page):
    expect(logged_in_page.get_by_text("Ордеров пока нет")).to_be_visible()
```

### Фабрика — когда нужно несколько объектов

```python
@pytest.fixture
def create_user(new_context):
    def _create() -> Page:
        page = new_context().new_page()
        ...                     # регистрация
        return page
    return _create

def test_two_users(create_user):
    buyer = create_user()
    seller = create_user()
```

### autouse

`@pytest.fixture(autouse=True)` — выполняется для каждого теста без указания в аргументах.
Например, выставить таймауты всем страницам:

```python
@pytest.fixture(autouse=True)
def short_timeouts(page):
    page.set_default_timeout(10_000)
```

---

## 5. conftest.py

Файл `conftest.py` — место для общих фикстур. pytest находит его сам, импортировать не надо.
Фикстуры видны всем тестам в этой папке и вложенных:

```
tests/
  conftest.py          ← общее для всех тестов (api и ui)
  ui/
    conftest.py        ← фикстуры только для UI: logged_in_page, create_user
    test_login.py
  api/
    conftest.py
```

Фикстура с тем же именем во вложенном conftest **перекрывает** внешнюю — так и
переопределяются встроенные фикстуры pytest-playwright.

---

## 6. Настройка pytest-playwright под проект

### Фикстуры, которые дал плагин

| Фикстура | scope | Что |
|---|---|---|
| `playwright` | session | объект Playwright (`playwright.devices`, `playwright.request`) |
| `browser_type` | session | `playwright.chromium` / `firefox` / `webkit` |
| `browser` | session | запущенный браузер |
| `browser_type_launch_args` | session | словарь для `launch(...)` |
| `browser_context_args` | session | словарь для `new_context(...)` |
| `new_context` | function | функция-фабрика context с настройками проекта |
| `context` | function | `new_context()` |
| `page` | function | `context.new_page()` |
| `browser_name`, `browser_channel`, `device` | session | значения опций |
| `is_chromium`, `is_firefox`, `is_webkit` | session | True / False |
| `base_url` | session | из `--base-url` или `base_url` в конфиге |
| `output_path` | function | папка артефактов этого теста |

### Переопределить настройки context для всех тестов

```python
# tests/ui/conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):        # берём настройки плагина
    return {
        **browser_context_args,                         # и дополняем, а не затираем
        "locale": "ru-RU",
        "viewport": {"width": 1440, "height": 900},
    }
```

Важно: scope тот же (`session`) и `**browser_context_args` — иначе потеряются `base_url` и видео.

### Только для одного теста — маркер

```python
@pytest.mark.browser_context_args(viewport={"width": 375, "height": 667}, locale="en-US")
def test_mobile_layout(page):
    ...
```

### Параметры запуска браузера

```python
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--start-maximized"]}
```

### base_url в конфиге вместо опции

```toml
# pyproject.toml
[tool.pytest.ini_options]
base_url = "http://localhost:8080"
```

Опция `--base-url` в командной строке перекрывает значение из конфига — так переключают окружение.

---

## 7. parametrize

Один тест — много наборов данных:

```python
@pytest.mark.parametrize("amount", ["0", "-1", "abc", ""])
def test_deposit_rejects_invalid_amount(logged_in_page, amount):
    ...
```

Несколько параметров и читаемые имена в отчёте:

```python
@pytest.mark.parametrize(
    ("email", "password", "error"),
    [
        ("not-an-email", "password123", "email"),
        ("a@test.com", "short", "password"),
    ],
    ids=["bad email", "short password"],
)
def test_register_validation(page, email, password, error):
    ...
```

В отчёте: `test_register_validation[chromium-bad email]`. `chromium` — потому что
pytest-playwright сам параметризует тесты по `--browser`.

`pytest.param` — для отдельной метки на одном наборе:

```python
pytest.param("0.00000001", marks=pytest.mark.xfail(reason="BUG-12"))
```

---

## 8. Маркеры

```python
@pytest.mark.smoke                                   # своя метка
@pytest.mark.skip(reason="фича выключена")
@pytest.mark.skipif(sys.platform == "win32", reason="...")
@pytest.mark.xfail(reason="BUG-42: баланс не обновляется")   # ожидаемо падает
@pytest.mark.skip_browser("webkit")                  # из pytest-playwright
@pytest.mark.only_browser("chromium")
```

У нас в `addopts` стоит `--strict-markers`: свою метку нужно **зарегистрировать**, иначе ошибка.
Это защита от опечаток (`@pytest.mark.smok` молча не сработал бы):

```toml
[tool.pytest.ini_options]
markers = [
    "smoke: быстрые критичные проверки",
    "regression: полный набор",
]
```

Запуск по меткам:

```bash
uv run pytest -m smoke
uv run pytest -m "smoke and not slow"
```

`xfail` — тест на известный баг: прогон зелёный, в отчёте видно `XFAIL`. Когда баг починят,
тест станет `XPASS` — напоминание снять метку. С `strict=True` XPASS считается падением.

---

## 9. Полезные опции pytest

```bash
uv run pytest -v                  # имя каждого теста
uv run pytest -k "deposit and not invalid"   # по подстроке имени
uv run pytest -x                  # остановиться на первом падении
uv run pytest --lf                # перезапустить только упавшие в прошлый раз
uv run pytest -s                  # показывать print
uv run pytest --collect-only -q   # какие тесты будут запущены (с параметрами)
uv run pytest --browser chromium --browser firefox   # два браузера: каждый тест дважды
uv run pytest --device "iPhone 13"                   # профиль устройства для всех context
```

---

## Собес: вопросы и ответы

**1. Что такое BrowserContext и зачем новый context на каждый тест?**
> Это изолированный профиль внутри браузера, как окно инкогнито: свои cookies, localStorage,
> кэш, разрешения, настройки вроде viewport и locale. Все context живут в одном процессе
> браузера, поэтому создаются за миллисекунды, а браузер запускается за секунды. Новый context
> на тест даёт полную изоляцию: тесты не делят логин и состояние, не зависят от порядка
> и могут идти параллельно. Браузер при этом один на весь прогон — это дёшево.

**2. Как в одном тесте сыграть за двух пользователей?**
> Два context — каждый со своим хранилищем, поэтому каждый залогинен под своим пользователем.
> Две вкладки одного context не подойдут: они делят cookies и localStorage. В pytest-playwright
> удобно через фикстуру `new_context` — она применяет настройки проекта и закрывает context сама.

**3. Как не логиниться в каждом тесте?**
> Залогиниться один раз — лучше через API — и сохранить `storage_state`: cookies и localStorage
> в JSON. Новые context создаются с этим state и сразу залогинены. Нужно помнить, что токен
> истекает, что тесты одного пользователя делят его данные, и что тесты логина идут без state.

**4. Что Playwright проверяет перед кликом?**
> Что элемент прикреплён к DOM, видим, стабилен (не анимируется), принимает события — то есть
> в точке клика не оверлей, — и enabled. Для fill ещё editable. Ждёт, пока все проверки пройдут,
> до таймаута действия, по умолчанию 30 секунд. `force=True` пропускает проверки, но это обычно
> маскирует реальную проблему.

**5. Как устроены фикстуры pytest? Что такое scope, yield, conftest?**
> Фикстура — функция, результат которой pytest передаёт в тест по имени аргумента. Код до
> `yield` — setup, после — teardown, он выполнится даже при падении теста. Scope определяет,
> сколько живёт фикстура: function, class, module, session; фикстура не может зависеть от
> фикстуры с более коротким scope. `conftest.py` — место для общих фикстур, они видны тестам
> в этой папке и ниже, вложенный conftest может переопределить фикстуру.

**6. Как настроить pytest-playwright под проект?**
> Переопределить session-фикстуры `browser_context_args` и `browser_type_launch_args` в conftest,
> дополняя, а не затирая словарь плагина. Для одного теста — маркер `browser_context_args`.
> `base_url` — в конфиге, окружение переключаю через `--base-url`. Браузеры — `--browser`,
> устройство — `--device`, артефакты при падении — `--tracing`, `--screenshot`, `--video`.

**7. Зачем `--strict-markers` и что такое xfail?**
> `--strict-markers` требует регистрировать метки в конфиге — опечатка в метке станет ошибкой,
> а не молча пропущенным фильтром. `xfail` — тест на известный баг: прогон зелёный, в отчёте
> XFAIL со ссылкой на баг; когда починят, будет XPASS, и метку надо снять.
> С `strict=True` XPASS считается падением.
