# U4. Урок 1 — Page Object и Application

Задания: `practice/tasks/test_u4_01_page_object.py`, решение — `tests/ui/test_u4_01_page_object.py` (создаёшь сам), код — в `ui_framework/pages/`.
Ревью: `practice/u4_01_review_me.py`.

План: какую проблему решает Page Object; граница «страница — как, тест — что»; как устроить
PO на нашем стенде (SPA: один URL, два экрана); что возвращают методы; можно ли проверки внутри
PO; базовая страница; `Application` — одна точка входа ко всем страницам; антипаттерны;
как PO выглядит на собесе.

Модуль U4 целиком: U4.1 Page Object и Application → U4.2 компоненты → U4.3 фикстуры состояния и конфиг окружений →
U4.4 утилиты, Allure-шаги и структура проекта → U4.5 Screenplay, собес и каркас фреймворка.

---

## 1. Проблема

Так выглядят тесты без слоя страниц:

```python
def test_deposit(page, user_email):
    page.goto("/app/")
    page.get_by_label("Email").fill(user_email)
    page.get_by_label("Пароль").fill("password123")
    page.get_by_role("button", name="Зарегистрироваться").click()
    expect(page.get_by_test_id("dashboard")).to_be_visible()
    page.locator("#deposit-form").get_by_label("Актив").select_option("USDT")
    page.locator("#deposit-form").get_by_placeholder("Сумма").fill("1000")
    page.locator("#deposit-form").get_by_role("button", name="Пополнить").click()
    expect(page.locator('[data-testid="balance-row"][data-asset="USDT"]')
           .get_by_test_id("balance-available")).to_have_text("1000")
```

Что не так:
- **дублирование**: регистрация и пополнение повторяются в десятках тестов;
- **хрупкость**: переименовали кнопку «Пополнить» → правим 40 тестов;
- **читаемость**: за селекторами не видно, что проверяет тест;
- тест знает **устройство DOM**: id формы, `data-asset`, вложенность.

Хелперы-функции (как наши `register`, `deposit` в `helpers.py`) решают часть проблемы. Page Object —
следующий шаг: всё про один экран собрано в одном классе.

---

## 2. Идея

**Page Object** — класс, который описывает экран (страницу или её часть):
- **локаторы** его элементов;
- **действия** на языке пользователя: «войти», «пополнить», «разместить ордер»;
- **доступ к состоянию** для проверок: «доступный баланс USDT», «строка ордера».

Граница:

| Page Object — **как** | Тест — **что** |
|---|---|
| какие поля заполнить, какую кнопку нажать | какой сценарий выполняется |
| где на экране баланс | какой баланс ожидается |
| как дождаться, что экран открылся | какой результат правильный |
| знает DOM | не знает DOM |

Тот же тест с PO:

```python
def test_deposit(app, user_email):
    app.auth.open().register(user_email, PASSWORD)
    app.dashboard.deposit("USDT", "1000")
    expect(app.dashboard.balance_available("USDT")).to_have_text("1000")
```

`app` — объект `Application`, через него тест получает все страницы (раздел 6).

Поменялась кнопка — правим одну строку в `DashboardPage`. Тест читается как сценарий.

---

## 3. PO на нашем стенде

Стенд — SPA: всё живёт на `/app/`, но экранов два — форма входа и кабинет. PO — **на экран**,
а не на URL:

```
ui_framework/
  application.py         # Application: одна точка входа ко всем страницам (раздел 6)
  pages/
    base_page.py         # BasePage: page, open(path), общий тост
    auth_page.py         # AuthPage: вход и регистрация
    dashboard_page.py    # DashboardPage: шапка, балансы, пополнение, ордера
```

### BasePage

```python
from playwright.sync_api import Locator, Page


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page
        self.toast: Locator = page.get_by_test_id("toast")

    def open(self):
        self.page.goto(self.path)
        return self
```

`path` переопределяют наследники. `base_url` уже настроен в pytest-playwright — пишем относительный путь.

### Локаторы в `__init__`

```python
class AuthPage(BasePage):
    path = "/app/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.root = page.get_by_test_id("auth-page")
        self.email = page.get_by_label("Email")
        self.password = page.get_by_label("Пароль")
        self.login_button = page.get_by_role("button", name="Войти")
        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.error = page.get_by_test_id("auth-error")
```

Почему можно создавать локаторы заранее, когда элементов ещё нет: **Locator ленивый** (U2.2) —
это описание поиска, элемент ищется в момент действия. В Selenium так нельзя было делать
с `find_element` — поэтому там `@FindBy` и PageFactory. Здесь — просто атрибуты.

Локаторы с параметром — методы:

```python
def balance_row(self, asset: str) -> Locator:
    return self.page.locator(f'[data-testid="balance-row"][data-asset="{asset}"]')
```

### Действия и переходы

```python
class AuthPage(BasePage):
    ...
    def fill_credentials(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)

    def register(self, email: str, password: str) -> "DashboardPage":
        self.fill_credentials(email, password)
        self.register_button.click()
        return DashboardPage(self.page).wait_loaded()

    def login(self, email: str, password: str) -> "DashboardPage":
        self.fill_credentials(email, password)
        self.login_button.click()
        return DashboardPage(self.page).wait_loaded()

    def login_expecting_error(self, email: str, password: str) -> "AuthPage":
        self.fill_credentials(email, password)
        self.login_button.click()
        return self
```

Метод, после которого пользователь попадает на другой экран, **возвращает PO этого экрана**.
Тест может писать цепочкой: `app.auth.open().login(...).deposit(...)`. Возврат нужен ещё и как
синхронизация: `login` ждёт, что кабинет открылся (`wait_loaded`).

Позитивный и негативный вход — разные методы: `login` обещает кабинет и ждёт его,
`login_expecting_error` остаётся на форме. Один метод `login(..., expect_success=True)` с ветвлением
внутри читается хуже и прячет, что ожидает тест.

### Что возвращать для проверок: Locator, а не строку

```python
# ХОРОШО: тест сам решает, что ожидать, и expect повторяет проверку
def balance_available(self, asset: str) -> Locator:
    return self.balance_row(asset).get_by_test_id("balance-available")

expect(dashboard.balance_available("USDT")).to_have_text("1000")

# ПЛОХО: строка «в моменте» — прощай web-first assertions (U2.1)
def get_balance(self, asset: str) -> str:
    return self.balance_row(asset).get_by_test_id("balance-available").text_content()

assert dashboard.get_balance("USDT") == "1000"     # флейк
```

Строку или число возвращать можно, когда значение нужно **для следующих шагов**
(id ордера из ответа сервера), а не для проверки.

---

## 4. Проверки внутри Page Object

Классическое правило (Мартин Фаулер, Selenium-сообщество): **в PO нет проверок**.
PO описывает экран, проверка — решение теста. Если `deposit()` сам проверяет «баланс 1000», его
нельзя использовать в тесте «пополнение отрицательной суммой отклоняется».

Но есть два вида `expect` внутри PO, которые на практике считаются нормой:

| Что | Пример | Почему можно |
|---|---|---|
| **синхронизация**: экран открылся | `wait_loaded()`: `expect(self.root).to_be_visible()` | это не проверка сценария, а «дождаться, пока можно работать» |
| **предусловие действия** | `deposit()` ждёт ответ сервера и падает, если он не 2xx | метод обещает «пополнить»; если не вышло — дальше идти бессмысленно |

Граница: PO может проверить, что **его собственное действие выполнилось**, но не то, какой
**бизнес-результат** ожидает тест. «Ответ 200 на пополнение» — в PO; «баланс стал 1000» — в тесте.
Для негативных сценариев — отдельный метод без этой проверки (`deposit_expecting_error`).

```python
class DashboardPage(BasePage):
    def wait_loaded(self) -> "DashboardPage":
        expect(self.root).to_be_visible()
        return self
```

На собесе хорошо сказать обе вещи: правило и где ты сознательно его нарушаешь.

---

## 5. Как выглядит DashboardPage

```python
class DashboardPage(BasePage):
    path = "/app/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.root = page.get_by_test_id("dashboard")
        self.user_email = page.get_by_test_id("user-email")
        self.logout_button = page.get_by_role("button", name="Выйти")
        self.deposit_form = page.locator("#deposit-form")
        self.order_form = page.locator("#order-form")
        self.order_rows = page.get_by_test_id("order-row")

    def logout(self) -> "AuthPage": ...
    def deposit(self, asset: str, amount: str) -> dict: ...         # ждёт ответ, возвращает JSON
    def place_order(self, side, price, quantity, symbol="ETH-USDT") -> dict: ...
    def balance_available(self, asset: str) -> Locator: ...
    def balance_locked(self, asset: str) -> Locator: ...
    def order_row(self, order_id: str) -> Locator: ...
    def order_status(self, order_id: str) -> Locator: ...
    def cancel_order(self, order_id: str) -> None: ...
```

Он уже большой: шапка, балансы, две формы, таблица. В U4.2 вынесем куски в **компоненты**
(форма пополнения, таблица ордеров, тост) — PO страницы станет композицией компонентов.

### Циклический импорт

`AuthPage.login()` возвращает `DashboardPage`, `DashboardPage.logout()` — `AuthPage`.
Модули импортируют друг друга. Решения:
- импорт внутри метода: `from ui_framework.pages.dashboard_page import DashboardPage`;
- аннотация строкой (`-> "DashboardPage"`) + `from __future__ import annotations`
  + `if TYPE_CHECKING:` для импорта только для подсказок типов.

---

## 6. Application — одна точка входа

Страниц будет много: вход, кабинет, потом история, настройки, админка. Как отдать их тесту?

**Вариант А — фикстура на каждую страницу:**

```python
@pytest.fixture
def auth_page(page) -> AuthPage:
    return AuthPage(page)

@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    return DashboardPage(page)
# ... и так на каждую страницу
```

Фикстура ничего не делает, кроме `return XxxPage(page)`. Тридцать страниц — тридцать одинаковых
фикстур в conftest. Тест, которому нужны три экрана, перечисляет три аргумента.

**Вариант Б — `Application`**: один класс, который через **композицию** собирает все страницы.
Тест получает одну фикстуру `app` и ходит в страницы через неё.

```python
# ui_framework/application.py
from functools import cached_property

from playwright.sync_api import Page

from ui_framework.pages.auth_page import AuthPage
from ui_framework.pages.dashboard_page import DashboardPage


class Application:
    def __init__(self, page: Page):
        self.page = page

    @cached_property
    def auth(self) -> AuthPage:
        return AuthPage(self.page)

    @cached_property
    def dashboard(self) -> DashboardPage:
        return DashboardPage(self.page)
```

```python
# фикстура
@pytest.fixture
def app(page: Page) -> Application:
    return Application(page)


# тест
def test_logout(app, user_email):
    app.auth.open().register(user_email, PASSWORD)
    app.dashboard.logout()
    expect(app.auth.root).to_be_visible()
```

Мы в курсе используем **вариант Б**.

### Почему `cached_property`, а не атрибуты в `__init__`

`cached_property` создаёт страницу при **первом обращении** и запоминает её. Тест, которому нужен
только кабинет, не создаёт остальные 29 страниц. С атрибутами в `__init__` (`self.auth = AuthPage(page)`)
тоже работает: локаторы ленивые, создать PO дёшево. Но если в `__init__` страницы появится
что-то тяжелее, оно выполнится в каждом тесте для каждой страницы.

### Что даёт Application

- **одна фикстура вместо N**: новая страница — одно свойство в `Application`, фикстура не нужна;
- **автодополнение**: `app.` — IDE показывает все экраны приложения;
- **один `page` на всех**: все страницы работают в одной вкладке, нельзя случайно смешать вкладки;
- **место для общего**: позже сюда естественно встанут общие компоненты (шапка, тост) и API-клиент
  для подготовки данных (U5): `app.api.create_user()`.

### Где граница: Application раздаёт страницы, фикстуры готовят состояние

Application отвечает на вопрос **«как добраться до страницы»**. Он не логинится, не создаёт
данные и не содержит сценариев. Состояние перед тестом — дело **фикстур**:

```python
@pytest.fixture
def logged_in_app(app: Application, user_email: str) -> Application:
    app.auth.open().register(user_email, PASSWORD)
    return app


def test_deposit(logged_in_app):
    logged_in_app.dashboard.deposit("USDT", "1000")
    expect(logged_in_app.dashboard.balance_available("USDT")).to_have_text("1000")
```

Тест просит то, что ему нужно: `app` — приложение «с нуля», `logged_in_app` — пользователь уже в
кабинете. Фикстуры состояния (`logged_in_app` с балансом, с открытым ордером, второй пользователь) —
тема U4.3.

### Переходы и Application не мешают друг другу

`app.auth.register(...)` возвращает `DashboardPage`, а у `app` есть свой `app.dashboard`. Это
**разные объекты** одного экрана на одном `page`. PO без состояния (раздел 7), поэтому неважно,
каким объектом пользоваться. Правило: в цепочке — возвращённый, в остальном тесте — `app.dashboard`.

### Чего не делать с Application

| Плохо | Почему |
|---|---|
| `class Application(AuthPage, DashboardPage)` | наследование вместо композиции: все методы и локаторы в одной куче, конфликты имён |
| `app.register_and_deposit(...)` | сценарии в Application превращают его в God object; сценарии — в фикстурах или хелперах шагов |
| `app.last_order_id` | состояние, как и в PO, — антипаттерн |
| страницы знают об Application | `DashboardPage` не импортирует `Application`, зависимости в одну сторону |

### Когда Application начинает мешать

На сотнях страниц и нескольких продуктах один класс снова становится свалкой, а по сигнатуре
`test_x(app)` не видно, какие экраны трогает тест. Тогда делят по доменам: `app.trading.orders`,
`app.admin.users` — каждый домен свой маленький Application.

---

## 7. Антипаттерны

| Антипаттерн | Пример | Чем плохо |
|---|---|---|
| **God object** | один `ExchangePage` на всё приложение, 80 методов | невозможно найти и поддерживать |
| **Метод на клик** | `click_deposit_button()`, `fill_amount_field()` | PO не добавил смысла — тест всё так же описывает DOM |
| **Метод на тест** | `register_deposit_and_check_balance()` | нельзя переиспользовать, проверки спрятаны |
| **Бизнес-проверки внутри** | `deposit()` делает `expect(balance).to_have_text(...)` | нельзя использовать для негативных сценариев |
| **Возврат строк для проверок** | `get_status() -> str` | проверка в моменте, флейк |
| **Селекторы строками** | `DEPOSIT = "#deposit-form button"` и `page.click(DEPOSIT)` | теряем `get_by_role`, strict, цепочки |
| **Тестовые данные в PO** | `login()` без аргументов с зашитым email | PO знает про тест |
| **Состояние в PO** | `self.last_order_id` | неявная связь шагов, ломается при повторном использовании |
| **`sleep` / `wait_for_timeout`** | «чтобы форма успела» | U2.1 |
| **Наследование ради наследования** | `DashboardPage(AuthPage)` | экраны не являются друг другом; общее — в `BasePage` или компонентах |
| **Application со сценариями** | `app.register_and_deposit()` | Application раздаёт страницы, сценарии — в фикстурах |

---

## 8. Почему PO, а не просто функции-хелперы

| | Функции (`helpers.py`) | Page Object |
|---|---|---|
| Где локаторы | внутри каждой функции, дублируются | в одном месте на экран |
| Навигация | неявная | метод возвращает следующий экран |
| Автодополнение в IDE | список функций модуля | `dashboard.` → всё, что можно на экране |
| Масштаб | хорошо для 10–20 тестов | для сотен тестов и нескольких экранов |

Для маленького набора тестов хелперов хватает. Это нормальный ответ на собесе: «PO — не догма,
выбираю по размеру проекта».

---

## Собес: вопросы и ответы

**1. Что такое Page Object и зачем он нужен?**
> Класс, который описывает экран: его локаторы, действия на языке пользователя и доступ к состоянию
> для проверок. Тест говорит «что» — сценарий и ожидаемый результат, PO знает «как» — какие поля
> и кнопки. Изменения UI правятся в одном месте, тесты читаются как сценарии, нет дублирования.

**2. Где граница между Page Object и тестом? Можно ли проверки внутри PO?**
> Бизнес-проверок в PO нет: какой баланс правильный, решает тест. Иначе метод нельзя
> использовать в негативных сценариях. Внутри PO допускаю синхронизацию — дождаться, что экран
> открылся, — и проверку, что собственное действие метода выполнилось, например ответ сервера 2xx.
> Для негативных сценариев — отдельный метод без этой проверки.

**3. Что возвращают методы PO?**
> Действие, которое ведёт на другой экран, возвращает PO этого экрана — получается цепочка.
> Для проверок возвращаю Locator, чтобы тест делал `expect` с повтором. Строки и числа —
> только если значение нужно для следующих шагов, например id созданного ордера.

**4. Где хранить локаторы? Почему их можно создавать в `__init__`?**
> Атрибутами в `__init__`, параметризованные — методами. Locator в Playwright ленивый: это описание
> поиска, элемент ищется при каждом действии. Поэтому создать его заранее безопасно, в отличие от
> `find_element` в Selenium, где нужен был PageFactory.

**5. Как не превратить Page Object в свалку?**
> PO на экран, а не на приложение. Повторяющиеся части — форма, таблица, тост — выношу в компоненты
> и собираю страницу из них. Методы — действия пользователя, а не «клик по кнопке». Нет тестовых
> данных, нет состояния, нет бизнес-проверок. Общее — в BasePage, без наследования экранов друг от друга.

**6. PO или хелперы-функции?**
> Для небольшого набора тестов хватает хелперов. Когда экранов и тестов много, PO удобнее:
> локаторы в одном месте, навигация через возвращаемые страницы, автодополнение в IDE.
> Выбираю по размеру проекта, PO — не догма.

**7. Как PO в Playwright отличается от PO в Selenium?**
> В Selenium элементы ищутся сразу, поэтому нужен PageFactory или поиск в каждом методе, и есть
> stale element. В Playwright локаторы ленивые: объявляю их атрибутами, они ищутся заново при
> каждом действии. Плюс встроенные ожидания и `expect` — в PO не нужны свои wait-обёртки.

**8. Как тест получает страницы: фикстура на каждую или Application?**
> Использую Application: класс, который через композицию собирает все страницы на одном `page`,
> свойства через `cached_property`, чтобы страница создавалась при первом обращении. Тест получает
> одну фикстуру `app`, новая страница — одно свойство, а не новая фикстура. Application только
> раздаёт страницы, без сценариев и состояния. Состояние перед тестом — залогинен, есть баланс —
> готовят фикстуры: `logged_in_app`. Минус — по сигнатуре теста не видно, какие экраны он трогает,
> и на большом проекте класс разрастается; тогда делю его по доменам.
