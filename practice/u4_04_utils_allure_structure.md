# U4. Урок 4 — утилиты, Allure и структура проекта

Задания: `practice/tasks/test_u4_04_utils_allure.py`, решение — `tests/ui/test_u4_04_utils_allure.py` (создаёшь сам), код — `ui_framework/utils/`, `ui_framework/data/`,
`ui_framework/fixtures/reporting.py`.

План: что такое слой утилит и что в него класть (и что нет); деньги и даты; генераторы и модели
тестовых данных; ожидание произвольного условия; логирование шагов; Allure — шаги, вложения,
метки, скриншот при падении, окружение, просмотр отчёта; итоговая структура UI-фреймворка.

---

## 1. Слой утилит

**Утилита** — функция без знания о страницах и тестах: принимает данные, возвращает данные.
Если функции нужен `page` или PO — это не утилита, а хелпер страницы или компонент.

| Кладём в `utils/` | Не кладём |
|---|---|
| форматирование и разбор денег, дат | «зарегистрировать и пополнить» — это фикстура / PO |
| ожидание условия (polling) | локаторы |
| логирование, Allure-обёртки | проверки бизнес-результата |
| генерация уникальных значений | всё, что знает про конкретный тест |

Признак здорового `utils/`: каждый модуль можно переиспользовать в API-тестах без изменений.
Признак свалки: `utils/helpers.py` на 600 строк.

---

## 2. Деньги

Стенд хранит суммы в `Decimal` и отдаёт строкой без лишних нулей (`exchange/schemas.py`):

```python
def _format_amount(value: Decimal) -> str:
    return format(value.normalize(), "f") if value else "0"
```

`"100.50"` → `"100.5"`, `"1000.000"` → `"1000"`, `0` → `"0"`. Тест, который ожидает `"100.50"`,
упадёт — хотя сумма верная. Утилиты:

```python
from decimal import Decimal


def to_decimal(value: str | int | Decimal) -> Decimal:
    return Decimal(str(value))


def format_amount(value: str | int | Decimal) -> str:
    """Как сервер: без лишних нулей, без экспоненты."""
    d = to_decimal(value)
    return format(d.normalize(), "f") if d else "0"
```

```python
expect(dashboard.balances.available("USDT")).to_have_text(format_amount(Decimal("1000") - Decimal("100.50")))
```

Правила:
- считать в `Decimal`, **никогда** в `float`: `0.1 + 0.2 != 0.3`;
- `Decimal("0.1")`, а не `Decimal(0.1)` — второе тащит ошибку float;
- сравнивать числа как числа (`to_decimal(text) == Decimal("900")`), если формат не важен;
  проверять текст (`format_amount`), если важен именно вид на экране.

### Даты

UI стенда дат не показывает, но в API есть `created_at`. Типичные задачи:

```python
from datetime import datetime, timezone

created = datetime.fromisoformat(order["created_at"])    # ISO 8601 → aware datetime
assert created.tzinfo is not None                         # сервер отдаёт с часовым поясом
assert abs(datetime.now(timezone.utc) - created).total_seconds() < 60
```

Сравнивать — всегда aware с aware (с часовым поясом). Время в тесте — источник флейков (U2.4):
«сейчас», полночь, разные пояса у CI и стенда. Подмена времени в браузере — `page.clock` (U3).

---

## 3. Тестовые данные: генераторы и модели

### Генераторы уникальных значений

```python
from uuid import uuid4


def unique_email(prefix: str = "user") -> str:
    return f"{prefix}_{uuid4().hex[:8]}@test.com"
```

Faker (`faker.email()`) даёт «правдоподобные» данные, но **не гарантирует уникальность** — на сотнях
прогонов будут совпадения. Для ключевых полей (email, имя) — uuid; Faker — для «декоративных».

### Модель данных

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class OrderData:
    side: str = "BUY"
    price: str = "1"
    quantity: str = "1"
    symbol: str = "ETH-USDT"

    @property
    def cost(self) -> Decimal:
        return to_decimal(self.price) * to_decimal(self.quantity)


order = OrderData(price="100.5", quantity="2")
sell = replace(order, side="SELL")                 # копия с изменённым полем
dashboard.order_form.place(**asdict(order))
```

Что даёт:
- значения по умолчанию — тест указывает только то, что важно ему;
- производные значения (`cost`) считаются в одном месте;
- `frozen=True` — нельзя случайно поменять общий объект между тестами.

### Данные, не пересекающиеся с чужими

Урок U1.4: стакан общий. Генератор цены вне диапазона «чужих» ордеров:

```python
def isolated_price(low: int = 300, high: int = 499) -> str:
    return str(random.randint(low, high))
```

Лучше — вообще не зависеть от общего стакана (своё окружение на прогон), но если нельзя —
такие правила фиксируются в одном месте с комментарием почему.

---

## 4. Ожидание условия (polling)

Из U2.1: в Python нет `expect.poll`. Своё ожидание для не-UI условий:

```python
import time
from collections.abc import Callable


def wait_until(
    condition: Callable[[], bool],
    timeout: float = 10,
    interval: float = 0.5,
    message: str = "условие не выполнилось",
) -> None:
    deadline = time.monotonic() + timeout
    while True:
        if condition():
            return
        if time.monotonic() >= deadline:
            raise AssertionError(f"{message} за {timeout} с")
        time.sleep(interval)
```

Детали, которые спрашивают:
- `time.monotonic()`, а не `time.time()` — системное время может прыгнуть;
- последняя проверка **после** дедлайна не теряется — условие проверяется до выхода;
- исключения внутри `condition` — решить: пробрасывать сразу или считать «ещё нет»
  (например, 404 пока ресурс не создан). Часто добавляют параметр `ignore=(SomeError,)`.

Для UI — **всегда `expect`**: он делает то же самое, но знает DOM и даёт хороший лог.

---

## 5. Логирование шагов

```python
import logging

log = logging.getLogger("ui")


class DepositForm(BaseComponent):
    def deposit(self, asset: str, amount: str) -> dict:
        log.info("deposit %s %s", asset, amount)
        ...
```

Видно при запуске с `--log-cli-level=INFO` (вживую) или в отчёте pytest при падении
(секция «Captured log call»). Не логировать секреты: пароль — `SecretStr`, токен — не печатать целиком.

---

## 6. Allure

`allure-pytest` уже стоит. Запуск с отчётом:

```bash
uv run pytest tests/ui -m smoke --alluredir allure-results --clean-alluredir
allure serve allure-results                          # собрать и открыть в браузере
allure generate allure-results -o allure-report --clean   # статический отчёт
```

Allure CLI на машине есть, но ему нужна **Java** (`brew install openjdk`, дальше следовать
подсказке brew про PATH). `allure-results/` и `allure-report/` в `.gitignore`.

### Шаги

```python
import allure


class DepositForm(BaseComponent):
    @allure.step("Пополнить {asset} на {amount}")
    def deposit(self, asset: str, amount: str) -> dict: ...
```

```python
def test_deposit(logged_in_app):
    logged_in_app.dashboard.deposit_form.deposit("USDT", "1000")
    with allure.step("Проверить баланс"):
        expect(logged_in_app.dashboard.balances.available("USDT")).to_have_text("1000")
```

- декоратор на методах PO / компонентов — шаги появляются во **всех** тестах автоматически;
- `{asset}` подставляет аргумент по имени; строки Allure показывает **в кавычках**:
  `Пополнить 'USDT' на '1000'` (проверено на нашей версии);
- вложенные шаги — дерево: `deposit` внутри шага `with allure.step(...)`;
- пароли не попадают в шаги: не делай `@allure.step("Войти {email} / {password}")`.

### Вложения

```python
allure.attach(page.screenshot(full_page=True), name="screenshot", attachment_type=allure.attachment_type.PNG)
allure.attach(json.dumps(order, indent=2), name="order", attachment_type=allure.attachment_type.JSON)
allure.attach.file("test-results/.../trace.zip", name="trace", extension="zip")
```

### Скриншот при падении — хук

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.screenshot(full_page=True), name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(page.url, name="url", attachment_type=allure.attachment_type.TEXT)
```

Хук вызывается для каждой фазы теста (`setup`, `call`, `teardown`). `report.when == "call"` — падение
самого теста. `item.funcargs` — фикстуры теста; `page` там есть, только если тест (или его фикстуры)
её запросили. Хуки можно держать в модуле плагина (`ui_framework/fixtures/reporting.py`) и подключать
через `pytest_plugins` — как фикстуры (U4.3).

Проверено на стенде: упавший тест получает в отчёте шаги и вложения `screenshot` и `url`.

### Метки

```python
@allure.epic("Биржа")
@allure.feature("Баланс")
@allure.story("Пополнение")
@allure.title("Пополнение USDT увеличивает доступный баланс")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://...", name="Требование")
@allure.issue("BUG-12")                   # для xfail на известный баг
def test_deposit(...): ...
```

- `feature` / `story` — группировка на вкладке Behaviors;
- `title` — человекочитаемое имя вместо `test_deposit[chromium]`;
- `allure.dynamic.title(...)` / `allure.dynamic.parameter(...)` — изнутри теста, например для parametrize.

### Окружение в отчёте

Файл `allure-results/environment.properties` — Allure покажет его на главной:

```python
def pytest_sessionstart(session):
    results = session.config.getoption("--alluredir", default=None)
    if results:
        s = Settings()
        Path(results).mkdir(parents=True, exist_ok=True)
        (Path(results) / "environment.properties").write_text(
            f"env={s.env}\nbase_url={s.base_url}\n"
        )
```

---

## 7. Структура UI-фреймворка

```
ui_framework/
  config/
    settings.py          # Settings: окружения, таймауты, секреты (U4.3)
  application.py         # Application: раздаёт страницы (U4.1)
  pages/                 # экраны: BasePage, AuthPage, DashboardPage (U4.1)
  components/            # формы, таблицы, тост, шапка (U4.2)
  fixtures/              # pytest-плагины: app.py, data.py, reporting.py (U4.3–U4.4)
  data/
    models.py            # OrderData и другие модели тестовых данных
    generators.py        # unique_email, isolated_price
  utils/
    money.py             # to_decimal, format_amount
    waiting.py           # wait_until
    logging.py           # настройка логгера (если нужна)
envs/
  ui.docker.env  ui.stage.env  ui.local.env      # в git
  ui.*.local.env                                  # секреты, не в git
tests/
  conftest.py            # pytest_plugins, settings, base_url, хуки
  ui/
    conftest.py          # только UI-специфичное
    test_*.py
```

Почему так:
- **фреймворк отдельно от тестов** — пакет можно переиспользовать и версионировать;
- **зависимости в одну сторону**: tests → fixtures → application → pages → components → utils/data.
  `utils` не импортирует `pages`, компоненты не импортируют страницы (U4.2);
- **конфиг в одном месте** — окружения переключаются без правки кода;
- **данные отдельно от логики** — модели и генераторы переиспользуются в API-тестах.

---

## Собес: вопросы и ответы

**1. Как устроен твой UI-фреймворк целиком?**
> Отдельный пакет. Конфиг на pydantic-settings с окружениями и секретами из переменных окружения.
> Слой страниц — Page Object на экран — собран из компонентов: формы, таблицы, шапка, тост.
> Фикстуры — pytest-плагины в пакете: страницы, данные, отчётность, подключаются в корневом conftest.
> Данные — модели на dataclass и генераторы уникальных значений. Утилиты — деньги, даты, polling,
> логирование. Отчёт — Allure: шаги из декораторов на методах PO, скриншот и URL при падении,
> окружение на главной. Зависимости идут в одну сторону: тесты → фикстуры → страницы → компоненты → утилиты.

**2. Что кладёшь в utils, а что нет?**
> Функции, которые не знают о страницах и тестах: форматирование денег и дат, ожидание условия,
> генерация значений, логирование. Всё, что работает с `page`, — в страницы или компоненты; подготовка
> состояния — в фикстуры; проверки — в тесты. Утилиты должны подходить и для API-тестов.

**3. Как работаешь с деньгами в тестах?**
> Только Decimal, создаю из строки. Сервер отдаёт суммы строкой без лишних нулей — для сравнения
> текста на экране форматирую ожидаемое значение так же, как сервер; если формат не важен — сравниваю
> числа. float не использую: ошибки округления.

**4. Как делаешь шаги и вложения в Allure?**
> Декоратор `@allure.step` на методах PO и компонентов — шаги появляются во всех тестах без дублирования,
> с параметрами в названии. В тесте — `with allure.step` для смысловых блоков проверок. Вложения:
> скриншот и URL при падении через хук `pytest_runtest_makereport`, JSON ответов, trace. Метки feature,
> story, severity, title — для группировки и читаемых имён. Секреты в шаги не попадают.

**5. Как прикрепить скриншот к упавшему тесту?**
> Хук `pytest_runtest_makereport` с `hookwrapper=True`: получаю отчёт, если фаза call и тест упал —
> беру `page` из `item.funcargs` и прикладываю `page.screenshot()` в Allure. Альтернатива без Allure —
> опции pytest-playwright `--screenshot only-on-failure`, `--video`, `--tracing retain-on-failure`.

**6. Зачем модели тестовых данных?**
> Значения по умолчанию — тест задаёт только важное ему. Производные значения считаются в одном месте.
> `frozen` защищает от случайного изменения общего объекта. Данные читаются как предметная область,
> а не как набор строк.
