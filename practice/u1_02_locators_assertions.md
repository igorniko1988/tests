# U1. Урок 2 — локаторы и проверки подробно

Задания: `practice/tasks/test_u1_02_locators_assertions.py`, решение — `tests/ui/test_u1_02_locators_assertions.py` (создаёшь сам).
В U1.1 был обзор. Здесь — как Playwright на самом деле находит элементы, все приёмы уточнения
(цепочки, filter, and_/or_), работа с таблицами и списками и полный набор `expect`.

---

## 1. Роли и доступное имя — как работает get_by_role

Браузер строит для каждой страницы **дерево доступности** (accessibility tree). Его читают
скринридеры для незрячих пользователей. У каждого узла есть:

- **роль** — что это за элемент: кнопка, поле, заголовок;
- **доступное имя** (accessible name) — как элемент «называется» для пользователя.

`get_by_role` ищет именно по этому дереву, а не по HTML-разметке.

### Неявные роли: тег → роль

Атрибут `role` писать не нужно, у стандартных тегов роль уже есть:

| HTML | Роль |
|---|---|
| `<button>`, `<input type=submit>` | `button` |
| `<a href>` | `link` |
| `<input type=text/email/password>`, `<textarea>` | `textbox` (у password — тоже textbox) |
| `<input type=checkbox>` | `checkbox` |
| `<input type=radio>` | `radio` |
| `<select>` | `combobox` (`listbox`, если `multiple`) |
| `<option>` | `option` |
| `<h1>`–`<h6>` | `heading` (уровень — `level`) |
| `<table>`, `<tr>`, `<td>`, `<th>` | `table`, `row`, `cell`, `columnheader` |
| `<ul>/<ol>`, `<li>` | `list`, `listitem` |
| `<form>` с именем | `form` |
| `<fieldset>` | `group` |
| `<img alt>` | `img` |
| `<dialog>` | `dialog` |

Явная роль из атрибута `role="..."` перекрывает неявную. На стенде у ошибок `role="alert"`,
у тоста — `role="status"`.

### Откуда берётся доступное имя

По порядку приоритета:

1. `aria-labelledby="id"` — текст другого элемента;
2. `aria-label="..."` — у нас: `<input aria-label="Сумма">`;
3. связанный `<label>` — у нас `<label>Email <input></label>` → поле зовётся «Email»;
4. содержимое элемента — у кнопки текст `Войти`;
5. `title`, `placeholder` — запасные варианты.

Поэтому `get_by_role("textbox", name="Email")` и `get_by_label("Email")` находят одно и то же поле.

### Параметры get_by_role

```python
page.get_by_role("button", name="Войти")                  # подстрока, без регистра
page.get_by_role("button", name="Войти", exact=True)      # точное совпадение
page.get_by_role("button", name=re.compile(r"^Войти$"))   # регулярка
page.get_by_role("heading", level=2)                      # только <h2>
page.get_by_role("radio", checked=True)                   # выбранный radio
page.get_by_role("button", disabled=True)                 # отключённые кнопки
page.get_by_role("button", include_hidden=True)           # включая скрытые (по умолчанию — нет)
page.get_by_role("group", name="Сторона")                 # <fieldset> с <legend>Сторона</legend>
```

**Почему это сильнее CSS.** Если разработчик сделает «кнопку» из `<div onclick>`, у неё не будет
роли `button`, и тест упадёт. Это настоящий баг: с клавиатуры и скринридером такая кнопка не работает.
Тест на `get_by_role` ловит проблемы доступности бесплатно.

### Посмотреть дерево доступности

В Chrome: DevTools → Elements → вкладка **Accessibility** (справа): роль и имя выбранного элемента.
Или `uv run playwright codegen` → «Pick locator».

---

## 2. Остальные get_by_*

```python
page.get_by_label("Пароль")                      # по <label>, aria-label, aria-labelledby
page.get_by_placeholder("Сумма")
page.get_by_text("Ордеров пока нет")             # подстрока, регистр и пробелы не важны
page.get_by_text("Вход", exact=True)             # точно, с учётом регистра
page.get_by_text(re.compile(r"пополнен$"))       # регулярка
page.get_by_alt_text("logo")                     # <img alt="logo">
page.get_by_title("Подсказка")                   # атрибут title
page.get_by_test_id("toast")                     # data-testid
```

`get_by_text` находит **самый маленький** элемент с этим текстом. Текст внутри `<button>`
лучше искать ролью: `get_by_role("button", name=...)`.

### Свой атрибут для test id

Если в проекте атрибут называется не `data-testid`, а, например, `data-qa`:

```python
# conftest.py
from playwright.sync_api import Playwright
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_test_id(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-qa")
```

---

## 3. CSS-локаторы — когда без них никак

```python
page.locator("#auth-form")                                   # по id
page.locator(".toast")                                       # по классу
page.locator("button[type=submit]")                          # тег + атрибут
page.locator('[data-testid="balance-row"][data-asset="BTC"]')  # два атрибута сразу
page.locator('[data-testid="order-row"][data-id="42"]')      # строка ордера по id
page.locator("td.status")                                    # тег + класс
```

Псевдоклассы Playwright внутри CSS:

```python
page.locator("button:has-text('Войти')")        # кнопка, содержащая текст
page.locator("tr:has(td:text('BTC'))")           # строка, где есть ячейка с текстом BTC
page.locator("button:visible")                   # только видимые
```

Лучше их заменять `filter(...)` — читается проще (раздел 4).

XPath работает (`page.locator("xpath=//button")`, или просто строка с `//`), но на собесе
ответ один: только если других вариантов нет (например, поиск родителя: `..`).

---

## 4. Уточнение локаторов

### 4.1. Цепочки — поиск внутри элемента

```python
card = page.locator("#order-form")
card.get_by_label("Цена").fill("100")
card.get_by_role("button", name="Разместить ордер").click()
```

Любой метод `get_by_*` / `locator()` можно вызвать от другого локатора — поиск идёт только внутри него.

### 4.2. filter

```python
rows = page.get_by_test_id("order-row")

rows.filter(has_text="SELL")                                   # где есть текст
rows.filter(has_not_text="CANCELED")                           # где нет текста
rows.filter(has_text=re.compile(r"^ETH-USDT"))                 # регулярка
rows.filter(has=page.get_by_role("button", name="Отменить"))   # где есть вложенный элемент
rows.filter(has_not=page.get_by_role("button"))                # где нет кнопок
page.get_by_role("button").filter(visible=True)                # только видимые
```

Важно: локатор внутри `has=` ищется **относительно строки**, хотя пишется от `page`.

Фильтры можно складывать:

```python
rows.filter(has_text="SELL").filter(has_text="NEW")   # строки SELL со статусом NEW
```

### 4.3. Позиция: first, last, nth

```python
rows.first
rows.last
rows.nth(1)        # второй (с нуля)
```

Использовать осторожно: порядок строк может поменяться (сортировка, новые данные).
Надёжнее искать строку по содержимому (`filter`) или по уникальному атрибуту (`data-id`).

### 4.4. and_ и or_

```python
# элемент, подходящий под ОБА условия
page.get_by_role("button").and_(page.get_by_title("Отменить ордер"))

# любой из двух — например, иногда появляется окно с куки, иногда нет
dialog_or_dashboard = page.get_by_role("dialog").or_(page.get_by_test_id("dashboard"))
expect(dialog_or_dashboard.first).to_be_visible()
```

### 4.5. Работа с таблицей: найти строку → действие внутри строки

Главный приём для таблиц и списков:

```python
row = page.get_by_test_id("order-row").filter(has_text="SELL")    # 1. нашли строку
row.get_by_role("button", name="Отменить").click()                # 2. действие внутри
expect(row.get_by_test_id("order-status")).to_have_text("CANCELED")  # 3. проверка внутри
```

Ловушка: строка нашлась по тексту `NEW`, после отмены текста `NEW` в ней нет — локатор
`filter(has_text="NEW")` больше её не найдёт. Ищи строку по признаку, который **не меняется**
после действия (цена, сторона, `data-id`).

### 4.6. Несколько элементов: count, all, all_text_contents

```python
rows.count()                     # сколько СЕЙЧАС (не ждёт!)
rows.all()                       # список локаторов на каждый элемент (не ждёт!)
rows.all_text_contents()         # тексты всех элементов списком

for row in rows.all():
    print(row.get_by_test_id("order-status").text_content())
```

Эти методы снимают состояние «прямо сейчас». Для проверок — `expect(rows).to_have_count(3)`,
он подождёт, пока строк станет три. Перед `all()` сначала дождись нужного количества.

### 4.7. iframe

```python
frame = page.frame_locator("iframe#payment")
frame.get_by_label("Номер карты").fill("4242...")
```

Элементы внутри `<iframe>` не видны локаторам страницы — нужен `frame_locator` (подробно в U2/U3).

---

## 5. Проверки expect — полный набор

### Видимость и состояние

```python
expect(loc).to_be_visible()
expect(loc).to_be_hidden()          # скрыт ИЛИ отсутствует в DOM
expect(loc).to_be_attached()        # есть в DOM (даже скрытый)
expect(loc).to_be_enabled()
expect(loc).to_be_disabled()
expect(loc).to_be_editable()        # можно вводить текст
expect(loc).to_be_checked()         # checkbox / radio
expect(loc).to_be_focused()
expect(loc).to_be_empty()           # поле пустое / в элементе нет текста
expect(loc).to_be_in_viewport()     # в видимой области экрана
```

### Текст

```python
expect(loc).to_have_text("Вход")                         # весь текст (по краям пробелы не важны)
expect(loc).to_have_text(re.compile(r"пополнен$"))
expect(loc).to_have_text("вход", ignore_case=True)
expect(loc).to_contain_text("Invalid")                   # подстрока

# для локатора с несколькими элементами — список, порядок важен
expect(page.get_by_test_id("order-status")).to_have_text(["NEW", "NEW", "CANCELED"])
expect(page.get_by_test_id("order-status")).to_contain_text(["NEW", "CANCELED"])
```

Списком проверяются **все элементы сразу и в порядке**: и количество, и содержимое.

### Значения и атрибуты

```python
expect(loc).to_have_value("0.5")                          # <input>
expect(loc).to_have_values(["BTC", "ETH"])                # <select multiple>
expect(loc).to_have_attribute("type", "password")
expect(loc).to_have_attribute("data-asset", "BTC")
expect(loc).to_have_class(re.compile(r"\bdanger\b"))      # класс через регулярку
expect(loc).to_contain_class("danger")                    # один из классов
expect(loc).to_have_id("auth-form")
expect(loc).to_have_css("display", "none")                # вычисленный стиль
expect(loc).to_have_count(3)
```

### Доступность

```python
expect(loc).to_have_accessible_name("Сумма")
expect(loc).to_have_role("button")
```

### Страница

```python
expect(page).to_have_title("Mini Exchange")
expect(page).to_have_url(re.compile(r"/app/$"))
```

### Отрицания, таймаут, сообщение

```python
expect(loc).not_to_be_visible()
expect(loc).not_to_have_text("NEW")
expect(loc).to_be_visible(timeout=10_000)                     # мс, для одной проверки
expect(loc, "кабинет должен открыться после входа").to_be_visible()  # своё сообщение при падении
```

Таймаут для всех проверок — в `conftest.py`:

```python
from playwright.sync_api import expect
expect.set_options(timeout=7_000)
```

### ARIA snapshot — проверка структуры блока целиком

```python
expect(page.get_by_test_id("auth-page")).to_match_aria_snapshot("""
  - heading "Вход" [level=2]
  - textbox "Email"
  - textbox "Пароль"
  - button "Войти"
  - button "Зарегистрироваться"
""")
```

Проверяет дерево доступности блока одним махом: какие элементы, их роли и имена. Шаблон
удобно получить в codegen (кнопка «Assert snapshot»). Хорош для форм и меню.

### Мгновенные методы — НЕ для проверок

| Ждёт (для проверок) | Не ждёт (для чтения данных) |
|---|---|
| `expect(loc).to_be_visible()` | `loc.is_visible()` |
| `expect(loc).to_have_text(...)` | `loc.text_content()`, `loc.inner_text()` |
| `expect(loc).to_have_count(n)` | `loc.count()` |
| `expect(loc).to_be_checked()` | `loc.is_checked()` |

Правило: проверка → `expect`. Нужно значение для дальнейшей логики (например, прочитать id
созданного ордера) → сначала `expect` дождаться, потом читать.

```python
row = page.get_by_test_id("order-row").first
expect(row).to_be_visible()
order_id = row.get_attribute("data-id")
```

---

## 6. Пример: ордер — от создания до отмены

```python
import re
from uuid import uuid4
from playwright.sync_api import Page, expect


def register(page: Page) -> str:
    email = f"user_{uuid4().hex[:8]}@test.com"
    page.goto("/app/")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Пароль").fill("password123")
    page.get_by_role("button", name="Зарегистрироваться").click()
    expect(page.get_by_test_id("dashboard")).to_be_visible()
    return email


def deposit(page: Page, asset: str, amount: str) -> None:
    form = page.locator("#deposit-form")
    form.get_by_label("Актив").select_option(asset)
    form.get_by_label("Сумма").fill(amount)
    form.get_by_role("button", name="Пополнить").click()
    expect(page.get_by_test_id("toast")).to_have_text(f"Баланс {asset} пополнен")


def test_cancel_order(page: Page):
    register(page)
    deposit(page, "USDT", "1000")

    form = page.locator("#order-form")
    form.get_by_label("Пара").select_option("ETH-USDT")
    form.get_by_label("Купить").check()
    form.get_by_label("Цена").fill("123")
    form.get_by_label("Количество").fill("1")
    form.get_by_role("button", name="Разместить ордер").click()

    row = page.get_by_test_id("order-row").filter(has_text="123")
    expect(row.get_by_test_id("order-status")).to_have_text("NEW")

    row.get_by_role("button", name="Отменить").click()

    expect(row.get_by_test_id("order-status")).to_have_text("CANCELED")
    expect(row.get_by_role("button", name="Отменить")).to_have_count(0)
```

Функции `register` и `deposit` — простые хелперы, чтобы не копировать шаги. В U1.4 сделаем
из этого фикстуры, в U3 — Page Object.

---

## 7. Частые ошибки

- `rows.nth(0)` для «нужной» строки, когда порядок не гарантирован → `filter` по содержимому.
- Строка ищется по тексту, который меняется после действия (`has_text="NEW"`, потом отмена).
- `assert rows.count() == 3` сразу после клика — строки ещё не отрисовались. Нужно `to_have_count`.
- `get_by_text("Войти")` находит и заголовок, и кнопку → strict mode. Используй роль.
- `to_have_text("0.5")` на всю таблицу вместо ячейки — проверяй конкретную ячейку.
- Слишком общий локатор `page.get_by_role("button", name="Отменить")` при нескольких ордерах — ищи внутри строки.
- **Ждать неуникальный признак.** Два ордера подряд: после второго клика тост «Ордер размещён»
  ещё висит от первого, `expect(toast).to_have_text(...)` проходит мгновенно, тест заполняет форму
  для третьего ордера — и тут приходит ответ на второй, фронт делает `form.reset()` и стирает
  введённое. Третий ордер уходит пустым. Ждать надо то, что появляется **только** от этого
  действия: новую строку (`to_have_count(было + 1)`), строку с конкретной ценой, ответ сервера
  (`expect_response`, U2).

---

## Собес: вопросы и ответы

**1. Как работает get_by_role? Что такое accessible name?**
> Playwright ищет по дереву доступности, которое браузер строит для скринридеров. У элемента
> есть роль (кнопка, поле, заголовок), её дают тег или атрибут `role`, и доступное имя — из
> `aria-labelledby`, `aria-label`, связанного `<label>`, текста элемента или `title`/`placeholder`.
> Поэтому `get_by_role` находит элемент так, как его видит пользователь, и ловит проблемы
> доступности: «кнопка» из `div` без роли не найдётся.

**2. Как найти кнопку в нужной строке таблицы?**
> Сначала нахожу строку по уникальному и не меняющемуся содержимому — `filter(has_text=...)`
> или `filter(has=...)`, либо по атрибуту вроде `data-id`. Потом ищу кнопку внутри строки
> цепочкой: `row.get_by_role("button", name="Отменить")`. Индексы `nth` не использую,
> если порядок строк не гарантирован.

**3. Чем отличаются to_have_text и to_contain_text? Как проверить список?**
> `to_have_text` — весь текст элемента целиком (пробелы по краям игнорируются), `to_contain_text` —
> подстрока. Оба принимают регулярку. Для нескольких элементов передаю список: проверяется
> и количество, и текст каждого по порядку.

**4. Почему не `assert loc.is_visible()` / `assert loc.count() == 3`?**
> `is_visible()`, `count()`, `text_content()` возвращают состояние в этот момент и не ждут.
> После действия UI ещё может обновляться, и проверка будет флейковой. `expect(...)`
> повторяет проверку до таймаута. Мгновенные методы использую только чтобы прочитать данные,
> и перед этим дожидаюсь нужного состояния через expect.

**5. Что делать, если у элементов нет ни ролей, ни test-id?**
> Попросить разработчиков добавить `data-testid` или нормальную разметку (это ещё и
> доступность). Пока нет — CSS по стабильным атрибутам (`name`, `id`, `data-*`), поиск внутри
> контейнера и `filter`. XPath — последний вариант, например чтобы подняться к родителю.

**6. Что такое to_be_hidden и чем отличается от not_to_be_visible / to_be_attached?**
> `to_be_hidden` и `not_to_be_visible` — одно и то же: элемента нет в DOM или он невидим.
> `to_be_attached` — элемент есть в DOM, видим он или нет. Отсутствие элемента вообще —
> `to_have_count(0)`.

**7. Как проверить структуру формы целиком?**
> `to_match_aria_snapshot`: описываю дерево доступности блока в YAML (роли и имена), Playwright
> сравнивает. Одна проверка заменяет пять `to_be_visible` и заодно контролирует доступность.
