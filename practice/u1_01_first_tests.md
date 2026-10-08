# U1. Урок 1 — первые тесты на Playwright

Задания: `tests/ui/test_u1_01_first_tests.py` (условия в docstring, код пишешь сам).
Все примеры ниже — на нашем стенде, их можно сразу запускать.

---

## 1. Что такое Playwright

Playwright — библиотека от Microsoft для управления браузером из кода. Тест открывает настоящий
Chromium / Firefox / WebKit, кликает, вводит текст и проверяет, что видит пользователь.

Что умеет из коробки:

- три движка браузеров одним API (Chrome/Edge, Firefox, Safari-движок WebKit);
- **автоожидание**: перед кликом сам ждёт, пока элемент появится и станет доступен — `sleep` не нужен;
- **web-first проверки** `expect(...)`: повторяют проверку, пока она не станет верной;
- изоляция тестов через `BrowserContext` (чистый профиль на каждый тест);
- перехват сети, мок ответов, API-запросы, трейсы, видео, скриншоты;
- языки: Python, JS/TS, Java, C#.

На Python есть два API: **sync** (обычный код, его и используем) и **async** (`async/await`).
Подробно про устройство — урок U1.3.

---

## 2. Установка и запуск

```bash
uv add playwright pytest-playwright   # у нас уже стоит (группа tests в pyproject.toml)
uv run playwright install chromium    # скачать браузер (у нас на macOS 12 не ставится — см. ниже)
```

У нас в `pyproject.toml` в `addopts` стоит `--browser-channel chrome`: вместо скачанного Chromium
используется установленный у тебя Google Chrome.

`pytest-playwright` — плагин pytest. Он добавляет фикстуры (`page`, `context`, `browser`…) и опции
командной строки:

| Опция | Что делает |
|---|---|
| `--headed` | показать окно браузера (по умолчанию headless — без окна) |
| `--slowmo 500` | пауза 500 мс после каждого действия — удобно смотреть глазами |
| `--browser firefox` | движок: `chromium` (по умолч.), `firefox`, `webkit`; можно несколько раз |
| `--browser-channel chrome` | взять установленный Chrome / Edge вместо Chromium |
| `--base-url http://localhost:8080` | база для относительных путей в `page.goto("/app/")` |
| `--tracing retain-on-failure` | записать трейс упавшего теста |
| `--screenshot only-on-failure` | скриншот упавшего теста |
| `--video retain-on-failure` | видео упавшего теста |

Результаты (трейсы, скриншоты) кладутся в `test-results/`.

```bash
uv run pytest tests/ui --base-url http://localhost:8080 --headed --slowmo 500
uv run pytest tests/ui -k deposit                 # только тесты с "deposit" в имени
```

### base_url — зачем

```python
page.goto("http://localhost:8080/app/")   # плохо: адрес зашит в каждый тест
page.goto("/app/")                        # хорошо: адрес приходит из --base-url
```

С `base_url` тот же тест запускается на stage (`--base-url http://localhost:8081`) без правки кода.
Чтобы не писать опцию каждый раз, её можно добавить в `addopts` в `pyproject.toml`.

---

## 3. Фикстуры pytest-playwright

Фикстура — это то, что pytest создаёт и передаёт в тест по имени аргумента.

```python
from playwright.sync_api import Page, expect

def test_open(page: Page):     # pytest видит аргумент page и сам создаёт вкладку
    page.goto("/app/")
```

Иерархия объектов:

```
browser   — запущенный браузер. Один на весь прогон (запуск дорогой, ~1 с).
 └ context — «профиль»: свои cookies, localStorage, кэш. Новый на КАЖДЫЙ тест (создаётся за мс).
    └ page — вкладка внутри context. Новая на каждый тест.
```

| Фикстура | Область | Что это |
|---|---|---|
| `browser` | сессия (весь прогон) | объект `Browser` |
| `context` | тест | новый `BrowserContext` |
| `page` | тест | новая вкладка в этом context |
| `browser_name` | сессия | строка `"chromium"` / `"firefox"` / `"webkit"` |
| `base_url` | сессия | значение `--base-url` |

Почему это важно: в нашем фронтенде токен лежит в `localStorage`. Раз context новый на каждый тест,
тест 2 **не видит** логин из теста 1 — тесты не зависят друг от друга и могут идти в любом порядке.

---

## 4. Навигация и действия

```python
page.goto("/app/")                     # открыть страницу, ждёт событие load
page.reload()
page.go_back()

locator.click()                        # клик
locator.dblclick()
locator.fill("text")                   # очистить поле и вставить текст целиком
locator.clear()                        # очистить поле
locator.press("Enter")                 # нажать клавишу в элементе
locator.press_sequentially("abc", delay=100)   # печатать по символу (если сайт ловит каждое нажатие)
locator.check() / locator.uncheck()    # checkbox, radio
locator.select_option("BTC")           # <select>: по value или по тексту
locator.select_option(label="BTC")     # явно по видимому тексту
locator.hover()
locator.text_content() / inner_text()  # прочитать текст (без ожидания! для проверок — expect)
locator.input_value()                  # значение поля
```

Пример на стенде — вход по Enter вместо кнопки:

```python
page.goto("/app/")
page.get_by_label("Email").fill("user@test.com")
page.get_by_label("Пароль").fill("password123")
page.get_by_label("Пароль").press("Enter")
```

`fill` vs `press_sequentially`: `fill` вставляет значение сразу (быстро, в 99% случаев), а
`press_sequentially` печатает посимвольно — нужен для автокомплитов и масок ввода.

---

## 5. Локаторы — как найти элемент

**Локатор** — это «описание, как найти элемент», а не сам элемент.

```python
button = page.get_by_role("button", name="Войти")   # ещё ничего не искали
button.click()                                       # поиск происходит здесь
```

Локатор **ленивый**: элемент ищется заново при каждом действии и каждой проверке. Поэтому если
страница перерисовалась, локатор просто найдёт новый элемент. В Selenium в такой ситуации падает
`StaleElementReferenceException`, в Playwright такой ошибки нет.

### 5.1. get_by_role — основной способ

Ищет элемент по **роли** (что это: кнопка, поле, заголовок) и **доступному имени** (что на нём
написано или какой у него label). Так элемент видит пользователь и скринридер.

```python
page.get_by_role("button", name="Войти")
page.get_by_role("heading", name="Вход")           # <h1>…<h6>
page.get_by_role("textbox", name="Email")          # <input type=email> с label "Email"
page.get_by_role("radio", name="Продать")
page.get_by_role("combobox", name="Пара")          # <select>
page.get_by_role("row")                            # <tr>
page.get_by_role("cell", name="BTC")               # <td>
page.get_by_role("alert")                          # элемент с role="alert" (у нас ошибки)
```

Основные роли: `button`, `link`, `textbox`, `checkbox`, `radio`, `combobox`, `heading`,
`table`, `row`, `cell`, `alert`, `status`, `dialog`, `listitem`.

`name` по умолчанию ищет **подстроку без учёта регистра**. Точное совпадение — `exact=True`:

```python
page.get_by_role("button", name="Войти", exact=True)
```

### 5.2. get_by_label, get_by_placeholder, get_by_text

```python
page.get_by_label("Email")              # поле, связанное с <label>Email</label> или aria-label
page.get_by_label("Сумма")              # у нас: <input aria-label="Сумма">
page.get_by_placeholder("Сумма")        # по placeholder
page.get_by_text("Ордеров пока нет")    # по видимому тексту (подстрока)
page.get_by_text("Вход", exact=True)    # точный текст
```

`get_by_text` — для текста, на который не кликают (сообщения, подписи). Для кнопок лучше
`get_by_role("button", name=...)`: он проверяет и текст, и то, что это действительно кнопка.

### 5.3. get_by_test_id

```python
page.get_by_test_id("deposit-button")   # ищет атрибут data-testid="deposit-button"
```

`data-testid` разработчики ставят специально для тестов. Он не меняется при смене текста или
вёрстки. Минус — пользователь его не видит, поэтому тест не проверяет, что кнопка подписана правильно.

### 5.4. CSS и XPath

```python
page.locator("#auth-form button[type=submit]")                    # CSS
page.locator('[data-testid="balance-row"][data-asset="BTC"]')     # CSS по атрибутам
page.locator("//form[@id='auth-form']//button[1]")                # XPath — избегаем
```

### 5.5. Приоритет локаторов

1. `get_by_role` — проверяет то же, что видит пользователь, и заодно доступность.
2. `get_by_label` / `get_by_placeholder` / `get_by_text` — тоже «пользовательские».
3. `get_by_test_id` — стабильный контракт с разработчиками, когда ролей и текстов нет.
4. CSS по атрибутам — если ничего выше не подходит.
5. XPath и длинные цепочки CSS (`div > div:nth-child(3) > span`) — нет: любая правка вёрстки их ломает.

### 5.6. Уточнение: цепочки и filter

Локаторы можно вызывать от другого локатора — поиск идёт внутри него:

```python
form = page.locator("#deposit-form")
form.get_by_role("button", name="Пополнить").click()

btc_row = page.get_by_test_id("balance-row").filter(has_text="BTC")   # строка, где есть "BTC"
btc_row.get_by_test_id("balance-available")                           # ячейка внутри строки
```

`filter(has_text=...)` оставляет элементы, где есть текст; `filter(has=локатор)` — где есть
вложенный элемент. Подробно — U2.

### 5.7. Strict mode

Если локатор при действии находит **больше одного** элемента, Playwright падает с ошибкой
`strict mode violation`, а не кликает по первому попавшемуся. Это защита от клика «не туда».

```python
page.get_by_role("button").click()          # на странице много кнопок → ошибка strict mode
page.get_by_test_id("order-row").first      # явно первый
page.get_by_test_id("order-row").nth(2)     # третий (с нуля)
```

### 5.8. Как подобрать локатор быстро

```bash
uv run playwright codegen http://localhost:8080/app/
```

Откроется браузер и окно с кодом: кликаешь по странице — Playwright пишет действия и предлагает
локатор. Кнопка «Pick locator» показывает локатор для любого элемента. Результат — черновик:
переписываешь его руками в нормальный тест.

---

## 6. Проверки expect

```python
from playwright.sync_api import expect
```

### Проверки элемента

```python
expect(loc).to_be_visible()                  # виден
expect(loc).to_be_hidden()                   # скрыт или его нет
expect(loc).to_be_enabled() / to_be_disabled()
expect(loc).to_be_checked()                  # checkbox / radio
expect(loc).to_have_text("Вход")             # текст целиком (пробелы по краям игнорируются)
expect(loc).to_contain_text("Invalid")       # подстрока
expect(loc).to_have_value("0.5")             # значение <input>
expect(loc).to_have_count(3)                 # сколько элементов нашёл локатор
expect(loc).to_have_attribute("type", "email")
expect(loc).to_have_class("toast")
```

### Проверки страницы

```python
expect(page).to_have_title("Mini Exchange")      # <title> вкладки
expect(page).to_have_url("http://localhost:8080/app/")
expect(page).to_have_url(re.compile(r".*/app/$"))  # регулярка, если адрес меняется
```

### Отрицание и таймаут

```python
expect(page.get_by_test_id("dashboard")).not_to_be_visible()
expect(page.get_by_test_id("toast")).to_have_text("Аккаунт создан", timeout=10_000)  # мс
```

Таймаут по умолчанию — 5 секунд.

### Почему expect, а не assert

```python
# assert: прочитал текст ОДИН раз. Если ответ сервера ещё не пришёл — текст пустой, тест падает.
assert page.get_by_test_id("auth-error").text_content() == "Invalid email or password"

# expect: проверяет снова и снова до 5 секунд, пока текст не совпадёт.
expect(page.get_by_test_id("auth-error")).to_have_text("Invalid email or password")
```

В UI всё асинхронно: после клика запрос уходит на сервер, ответ приходит через 50–500 мс, потом
страница перерисовывается. `assert` попадает «между» и даёт **флейки** — тесты, которые то
проходят, то падают. `expect` (web-first assertion) ждёт сам. `assert` оставляем для обычных
данных: ответов API, значений из БД, переменных.

---

## 7. Тестовые данные: уникальный пользователь

База стенда живёт между запусками. Если email повторится — регистрация вернёт
`User with this email already exists`, и тест упадёт.

```python
from uuid import uuid4

email = f"user_{uuid4().hex[:8]}@test.com"   # гарантированно уникальный
password = "password123"
```

`Faker().email()` выдаёт случайные, но **не уникальные** адреса из ограниченного набора имён.
На сотнях прогонов совпадения будут. Если используешь Faker — добавляй uuid или `faker.unique.email()`
(уникален только в пределах одного запуска).

---

## 8. Отладка упавшего теста

```bash
uv run pytest tests/ui -k deposit --headed --slowmo 1000      # посмотреть глазами
PWDEBUG=1 uv run pytest tests/ui -k deposit                   # Inspector: пошаговое выполнение
uv run pytest tests/ui --tracing retain-on-failure            # трейс при падении
uv run playwright show-trace test-results/<папка>/trace.zip   # открыть трейс
```

`page.pause()` в коде — остановка теста и открытие Inspector в этом месте.

**Трейс** — запись теста: каждое действие, снимок DOM до и после, сеть, консоль. Главный
инструмент разбора падений, особенно в CI, где окна нет.

---

## 9. Полный пример: тест логина

```python
from uuid import uuid4
from playwright.sync_api import Page, expect


def test_login_existing_user(page: Page):
    email = f"user_{uuid4().hex[:8]}@test.com"
    password = "password123"

    # регистрация — сразу логинит
    page.goto("/app/")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Пароль").fill(password)
    page.get_by_role("button", name="Зарегистрироваться").click()
    expect(page.get_by_test_id("dashboard")).to_be_visible()

    # выход
    page.get_by_role("button", name="Выйти").click()
    expect(page.get_by_test_id("auth-page")).to_be_visible()

    # вход
    page.get_by_label("Email").fill(email)
    page.get_by_label("Пароль").fill(password)
    page.get_by_role("button", name="Войти").click()

    expect(page.get_by_test_id("dashboard")).to_be_visible()
    expect(page.get_by_test_id("user-email")).to_have_text(email)
```

Структура любого UI-теста — **Arrange / Act / Assert**: подготовить данные → сделать действие →
проверить результат. Проверка в конце обязательна: тест без `expect` ничего не тестирует.

---

## 10. Частые ошибки новичка

- `time.sleep(2)` «чтобы успело» — нет: Playwright ждёт сам, а sleep делает тесты медленными и всё равно флейкает.
- `assert loc.is_visible()` — `is_visible()` не ждёт, проверяет мгновенно. Нужно `expect(loc).to_be_visible()`.
- Полный URL в `goto` вместо `base_url`.
- Тест без проверки в конце (только действия).
- Один и тот же email во всех запусках.
- Тест зависит от другого теста («сначала запусти регистрацию»). Каждый тест готовит данные сам.
- XPath, скопированный из DevTools: `/html/body/main/section[2]/div/div[1]/form/button`.

---

## Собес: вопросы и ответы

**1. Какие локаторы выбираешь и почему не XPath?**
> В первую очередь `get_by_role` с именем — он ищет элемент так, как его видит пользователь,
> и заодно проверяет доступность: если кнопка не размечена как кнопка, тест это покажет.
> Дальше `get_by_label`, `get_by_placeholder`, `get_by_text`. Если ролей и текстов нет или текст
> часто меняется (локализация) — `data-testid` по договорённости с разработчиками. XPath и длинные
> CSS-цепочки не использую: они повторяют структуру вёрстки, и любая правка вроде лишнего `div`
> ломает тест, хотя для пользователя ничего не изменилось. Ещё их тяжело читать.

**2. Почему expect, а не assert?**
> `expect` — web-first assertion: он повторяет проверку, пока она не пройдёт или не выйдет
> таймаут (по умолчанию 5 с). UI асинхронный: после клика идёт запрос на сервер и перерисовка,
> и `assert` может проверить состояние до того, как оно обновилось — получится флейк. `expect`
> это ожидание берёт на себя, поэтому не нужны `sleep` и ручные ожидания. `assert` использую для
> данных, которые уже получены: ответ API, запись из БД.

**3. Чем отличаются фикстуры browser, context и page?**
> `browser` — запущенный процесс браузера, в pytest-playwright он один на весь прогон, потому что
> запуск дорогой. `context` — изолированный профиль внутри браузера: свои cookies, localStorage,
> кэш, разрешения; создаётся за миллисекунды, и плагин даёт новый на каждый тест. `page` —
> вкладка внутри context. За счёт нового context на тест тесты не делят логин и данные сессии,
> их можно гонять в любом порядке и параллельно. Если в одном тесте нужны два пользователя — беру
> два context: каждый будет залогинен под своим.

**4. Что такое ленивый локатор? Почему в Playwright нет StaleElementReferenceException?**
> Локатор — это описание поиска, а не ссылка на найденный элемент. Playwright ищет элемент
> заново при каждом действии или проверке. Если DOM перерисовался, локатор найдёт новый элемент.
> В Selenium `find_element` возвращает ссылку на конкретный узел DOM, и после перерисовки она
> «протухает».

**5. Что такое strict mode?**
> Если локатор для действия нашёл несколько элементов, Playwright падает, а не берёт первый.
> Это защита от клика не по тому элементу. Нужен конкретный — уточняю локатор
> (`filter`, роль с именем, поиск внутри родителя) или явно пишу `.first` / `.nth(i)`.

**6. Как отлаживаешь упавший UI-тест?**
> Локально — `--headed --slowmo`, `PWDEBUG=1` или `page.pause()` для пошагового прохода в Inspector.
> В CI — трейс (`--tracing retain-on-failure`), открываю его в `playwright show-trace`: там каждое
> действие, снимок DOM до и после, сетевые запросы и консоль. Плюс скриншот и видео при падении.

**7. Как запустить тесты в другом браузере или на другом окружении?**
> Браузер — опцией `--browser firefox` / `webkit` (можно несколько сразу). Окружение — через
> `--base-url`: в тестах только относительные пути, `page.goto("/app/")`.
