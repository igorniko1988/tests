# Курс «UI-автоматизация на Playwright + Python», все уроки

Собрано скриптом `practice/build_ui_course.py` из файлов уроков — **не править руками**, править уроки и пересобирать.

Каждый урок: теория → задания (условия; решения пишутся в файле заданий) → файл для ревью, если есть.

Стенд: `docker compose up -d --build` → http://localhost:8080/app/ (кабинет), http://localhost:8080/app/lab.html (лаборатория).

## Оглавление

- **U1. Основы и устройство Playwright**
  - [U1.1 Первые тесты на Playwright](#u1-1)
  - [U1.2 Локаторы и проверки подробно](#u1-2)
  - [U1.3 Как устроен Playwright](#u1-3)
  - [U1.4 BrowserContext, ожидания и pytest для UI](#u1-4)
  - [U1.5 Собеседование по модулю U1](#u1-5)
- **U2. Ожидания и устойчивые тесты**
  - [U2.1 Web-first assertions и асинхронный UI](#u2-1)
  - [U2.2 Цепочки, фильтры и strict mode](#u2-2)
  - [U2.3 Codegen и Inspector](#u2-3)
  - [U2.4 Флейки и собес по модулю U2](#u2-4)
- **U3. Сложные элементы и сценарии**
  - [U3.1 Вкладки, всплывающие окна и iframe](#u3-1)
  - [U3.2 Диалоги браузера, загрузка и скачивание файлов](#u3-2)
  - [U3.3 Мышь, клавиатура, скролл и бесконечные списки](#u3-3)
  - [U3.4 Shadow DOM, таблицы, cookies и localStorage; собес по модулю U3](#u3-4)
- **U4. Page Object и архитектура**
  - [U4.1 Page Object](#u4-1)
  - [U4.2 Компоненты](#u4-2)
  - [U4.3 Фикстуры страниц и конфиг окружений](#u4-3)
  - [U4.4 Утилиты, Allure и структура проекта](#u4-4)
  - [U4.5 Screenplay, собес по модулю U4 и каркас фреймворка](#u4-5)
- **U5. Данные, авторизация и API внутри Playwright**
  - [U5.1 API внутри Playwright](#u5-1)
  - [U5.2 Тестовые данные](#u5-2)
  - [U5.3 Storage_state, роли, изоляция и параллельный запуск](#u5-3)
  - [U5.4 Собес по модулю U5](#u5-4)
- **U6. Сеть и окружение браузера**
  - [U6.1 Перехват сети: page.route и моки](#u6-1)
  - [U6.2 HAR и page.clock](#u6-2)
  - [U6.3 Окружение браузера и собес по модулю U6](#u6-3)
- **U7. Отладка и отчёты**
  - [U7.1 Trace Viewer, скриншоты, видео и отчёт](#u7-1)
  - [U7.2 Отладка и «в CI падает, локально проходит»; собес по модулю U7](#u7-2)
- **U8. Качество: визуал, доступность, производительность**
  - [U8.1 Визуальная регрессия](#u8-1)
  - [U8.2 Доступность и производительность фронта; собес по модулю U8](#u8-2)
- **U9. Масштаб и CI**
  - [U9.1 Параллель, шардирование и кросс-браузерность](#u9-1)
  - [U9.2 Docker-образ Playwright, CI, артефакты и стабильность; собес по модулю U9](#u9-2)
- **U10. Senior и собеседования**
  - [U10.1 Стратегия UI-автоматизации и гибридные тесты](#u10-1)
  - [U10.2 Ревью UI-тестов и Selenium на уровне собеседования](#u10-2)
  - [U10.3 Итоговый собес по UI-части и лайвкодинг](#u10-3)


---

# U1. Основы и устройство Playwright

<a id="u1-1"></a>

## U1.1 Первые тесты на Playwright

*Теория: `practice/u1_01_first_tests.md`*

Задания: `tests/ui/test_u1_01_first_tests.py` (условия в docstring, код пишешь сам).
Все примеры ниже — на нашем стенде, их можно сразу запускать.

---

#### 1. Что такое Playwright

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

#### 2. Установка и запуск

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

##### base_url — зачем

```python
page.goto("http://localhost:8080/app/")   # плохо: адрес зашит в каждый тест
page.goto("/app/")                        # хорошо: адрес приходит из --base-url
```

С `base_url` тот же тест запускается на stage (`--base-url http://localhost:8081`) без правки кода.
Чтобы не писать опцию каждый раз, её можно добавить в `addopts` в `pyproject.toml`.

---

#### 3. Фикстуры pytest-playwright

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

#### 4. Навигация и действия

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

#### 5. Локаторы — как найти элемент

**Локатор** — это «описание, как найти элемент», а не сам элемент.

```python
button = page.get_by_role("button", name="Войти")   # ещё ничего не искали
button.click()                                       # поиск происходит здесь
```

Локатор **ленивый**: элемент ищется заново при каждом действии и каждой проверке. Поэтому если
страница перерисовалась, локатор просто найдёт новый элемент. В Selenium в такой ситуации падает
`StaleElementReferenceException`, в Playwright такой ошибки нет.

##### 5.1. get_by_role — основной способ

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

##### 5.2. get_by_label, get_by_placeholder, get_by_text

```python
page.get_by_label("Email")              # поле, связанное с <label>Email</label> или aria-label
page.get_by_label("Сумма")              # у нас: <input aria-label="Сумма">
page.get_by_placeholder("Сумма")        # по placeholder
page.get_by_text("Ордеров пока нет")    # по видимому тексту (подстрока)
page.get_by_text("Вход", exact=True)    # точный текст
```

`get_by_text` — для текста, на который не кликают (сообщения, подписи). Для кнопок лучше
`get_by_role("button", name=...)`: он проверяет и текст, и то, что это действительно кнопка.

##### 5.3. get_by_test_id

```python
page.get_by_test_id("deposit-button")   # ищет атрибут data-testid="deposit-button"
```

`data-testid` разработчики ставят специально для тестов. Он не меняется при смене текста или
вёрстки. Минус — пользователь его не видит, поэтому тест не проверяет, что кнопка подписана правильно.

##### 5.4. CSS и XPath

```python
page.locator("#auth-form button[type=submit]")                    # CSS
page.locator('[data-testid="balance-row"][data-asset="BTC"]')     # CSS по атрибутам
page.locator("//form[@id='auth-form']//button[1]")                # XPath — избегаем
```

##### 5.5. Приоритет локаторов

1. `get_by_role` — проверяет то же, что видит пользователь, и заодно доступность.
2. `get_by_label` / `get_by_placeholder` / `get_by_text` — тоже «пользовательские».
3. `get_by_test_id` — стабильный контракт с разработчиками, когда ролей и текстов нет.
4. CSS по атрибутам — если ничего выше не подходит.
5. XPath и длинные цепочки CSS (`div > div:nth-child(3) > span`) — нет: любая правка вёрстки их ломает.

##### 5.6. Уточнение: цепочки и filter

Локаторы можно вызывать от другого локатора — поиск идёт внутри него:

```python
form = page.locator("#deposit-form")
form.get_by_role("button", name="Пополнить").click()

btc_row = page.get_by_test_id("balance-row").filter(has_text="BTC")   # строка, где есть "BTC"
btc_row.get_by_test_id("balance-available")                           # ячейка внутри строки
```

`filter(has_text=...)` оставляет элементы, где есть текст; `filter(has=локатор)` — где есть
вложенный элемент. Подробно — U2.

##### 5.7. Strict mode

Если локатор при действии находит **больше одного** элемента, Playwright падает с ошибкой
`strict mode violation`, а не кликает по первому попавшемуся. Это защита от клика «не туда».

```python
page.get_by_role("button").click()          # на странице много кнопок → ошибка strict mode
page.get_by_test_id("order-row").first      # явно первый
page.get_by_test_id("order-row").nth(2)     # третий (с нуля)
```

##### 5.8. Как подобрать локатор быстро

```bash
uv run playwright codegen http://localhost:8080/app/
```

Откроется браузер и окно с кодом: кликаешь по странице — Playwright пишет действия и предлагает
локатор. Кнопка «Pick locator» показывает локатор для любого элемента. Результат — черновик:
переписываешь его руками в нормальный тест.

---

#### 6. Проверки expect

```python
from playwright.sync_api import expect
```

##### Проверки элемента

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

##### Проверки страницы

```python
expect(page).to_have_title("Mini Exchange")      # <title> вкладки
expect(page).to_have_url("http://localhost:8080/app/")
expect(page).to_have_url(re.compile(r".*/app/$"))  # регулярка, если адрес меняется
```

##### Отрицание и таймаут

```python
expect(page.get_by_test_id("dashboard")).not_to_be_visible()
expect(page.get_by_test_id("toast")).to_have_text("Аккаунт создан", timeout=10_000)  # мс
```

Таймаут по умолчанию — 5 секунд.

##### Почему expect, а не assert

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

#### 7. Тестовые данные: уникальный пользователь

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

#### 8. Отладка упавшего теста

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

#### 9. Полный пример: тест логина

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

#### 10. Частые ошибки новичка

- `time.sleep(2)` «чтобы успело» — нет: Playwright ждёт сам, а sleep делает тесты медленными и всё равно флейкает.
- `assert loc.is_visible()` — `is_visible()` не ждёт, проверяет мгновенно. Нужно `expect(loc).to_be_visible()`.
- Полный URL в `goto` вместо `base_url`.
- Тест без проверки в конце (только действия).
- Один и тот же email во всех запусках.
- Тест зависит от другого теста («сначала запусти регистрацию»). Каждый тест готовит данные сам.
- XPath, скопированный из DevTools: `/html/body/main/section[2]/div/div[1]/form/button`.

---

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u1_01_first_tests.py`

```text
U1. Урок 1 — первые тесты на Playwright.

Теория: practice/u1_01_first_tests.md
Стенд: docker compose up -d --build  →  http://localhost:8080/app/
Запуск:
    uv run pytest tests/ui/test_u1_01_first_tests.py --base-url http://localhost:8080 --headed

Задача 1. Страница входа открывается.
    Открой /app/. Проверь: заголовок вкладки "Mini Exchange", поля Email и Пароль видны,
    кнопка "Войти" видна. Локаторы — get_by_label и get_by_role.

Задача 2. Регистрация нового пользователя.
    Уникальный email (подсказка: uuid4), пароль от 8 символов.
    Заполни поля, нажми "Зарегистрироваться".
    Проверь: кабинет (test-id "dashboard") виден, в шапке (test-id "user-email") твой email,
    тост (test-id "toast") с текстом "Аккаунт создан".

Задача 3. Вход с неверным паролем.
    Зарегистрируй пользователя, выйди (кнопка "Выйти"), войди с неправильным паролем.
    Проверь: ошибка (test-id "auth-error") с текстом "Invalid email or password",
    кабинет не виден (to_be_hidden).

Задача 4. Пополнение баланса.
    Зарегистрируйся. В блоке "Пополнить" выбери актив BTC (select_option),
    введи сумму 0.5 (get_by_placeholder), нажми "Пополнить".
    Проверь: в таблице балансов строка BTC, в колонке "Доступно" — 0.5.
    Подсказка: строка — page.locator('[data-testid="balance-row"][data-asset="BTC"]'),
    ячейка внутри — .get_by_test_id("balance-available").

Задача 5 (со звёздочкой). Ордер на продажу.
    После пополнения BTC выбери пару BTC-USDT, сторону "Продать" (check),
    цена 100, количество 0.1, нажми "Разместить ордер".
    Проверь: в таблице "Мои ордера" одна строка (to_have_count), статус NEW.

Вопросы собеса (ответь устно или в секции «Ответы»):
    1. Какие локаторы выбираешь и почему не XPath? - im usually start from page_get_by_role becaouse its also tests accessabilty, the data test ids and so on
    2. Почему expect, а не assert? because its web first assertions and it has by default waiting 5se and frontend is asyncronius
    3. Чем отличаются фикстуры browser, context и page? browser - one instance on sesion, context its like browser in incognito mode has own cash/cookie/ page ist like tab for context
```

<a id="u1-2"></a>

## U1.2 Локаторы и проверки подробно

*Теория: `practice/u1_02_locators_assertions.md`*

Задания: `tests/ui/test_u1_02_locators_assertions.py`.
В U1.1 был обзор. Здесь — как Playwright на самом деле находит элементы, все приёмы уточнения
(цепочки, filter, and_/or_), работа с таблицами и списками и полный набор `expect`.

---

#### 1. Роли и доступное имя — как работает get_by_role

Браузер строит для каждой страницы **дерево доступности** (accessibility tree). Его читают
скринридеры для незрячих пользователей. У каждого узла есть:

- **роль** — что это за элемент: кнопка, поле, заголовок;
- **доступное имя** (accessible name) — как элемент «называется» для пользователя.

`get_by_role` ищет именно по этому дереву, а не по HTML-разметке.

##### Неявные роли: тег → роль

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

##### Откуда берётся доступное имя

По порядку приоритета:

1. `aria-labelledby="id"` — текст другого элемента;
2. `aria-label="..."` — у нас: `<input aria-label="Сумма">`;
3. связанный `<label>` — у нас `<label>Email <input></label>` → поле зовётся «Email»;
4. содержимое элемента — у кнопки текст `Войти`;
5. `title`, `placeholder` — запасные варианты.

Поэтому `get_by_role("textbox", name="Email")` и `get_by_label("Email")` находят одно и то же поле.

##### Параметры get_by_role

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

##### Посмотреть дерево доступности

В Chrome: DevTools → Elements → вкладка **Accessibility** (справа): роль и имя выбранного элемента.
Или `uv run playwright codegen` → «Pick locator».

---

#### 2. Остальные get_by_*

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

##### Свой атрибут для test id

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

#### 3. CSS-локаторы — когда без них никак

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

#### 4. Уточнение локаторов

##### 4.1. Цепочки — поиск внутри элемента

```python
card = page.locator("#order-form")
card.get_by_label("Цена").fill("100")
card.get_by_role("button", name="Разместить ордер").click()
```

Любой метод `get_by_*` / `locator()` можно вызвать от другого локатора — поиск идёт только внутри него.

##### 4.2. filter

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

##### 4.3. Позиция: first, last, nth

```python
rows.first
rows.last
rows.nth(1)        # второй (с нуля)
```

Использовать осторожно: порядок строк может поменяться (сортировка, новые данные).
Надёжнее искать строку по содержимому (`filter`) или по уникальному атрибуту (`data-id`).

##### 4.4. and_ и or_

```python
# элемент, подходящий под ОБА условия
page.get_by_role("button").and_(page.get_by_title("Отменить ордер"))

# любой из двух — например, иногда появляется окно с куки, иногда нет
dialog_or_dashboard = page.get_by_role("dialog").or_(page.get_by_test_id("dashboard"))
expect(dialog_or_dashboard.first).to_be_visible()
```

##### 4.5. Работа с таблицей: найти строку → действие внутри строки

Главный приём для таблиц и списков:

```python
row = page.get_by_test_id("order-row").filter(has_text="SELL")    # 1. нашли строку
row.get_by_role("button", name="Отменить").click()                # 2. действие внутри
expect(row.get_by_test_id("order-status")).to_have_text("CANCELED")  # 3. проверка внутри
```

Ловушка: строка нашлась по тексту `NEW`, после отмены текста `NEW` в ней нет — локатор
`filter(has_text="NEW")` больше её не найдёт. Ищи строку по признаку, который **не меняется**
после действия (цена, сторона, `data-id`).

##### 4.6. Несколько элементов: count, all, all_text_contents

```python
rows.count()                     # сколько СЕЙЧАС (не ждёт!)
rows.all()                       # список локаторов на каждый элемент (не ждёт!)
rows.all_text_contents()         # тексты всех элементов списком

for row in rows.all():
    print(row.get_by_test_id("order-status").text_content())
```

Эти методы снимают состояние «прямо сейчас». Для проверок — `expect(rows).to_have_count(3)`,
он подождёт, пока строк станет три. Перед `all()` сначала дождись нужного количества.

##### 4.7. iframe

```python
frame = page.frame_locator("iframe#payment")
frame.get_by_label("Номер карты").fill("4242...")
```

Элементы внутри `<iframe>` не видны локаторам страницы — нужен `frame_locator` (подробно в U2/U3).

---

#### 5. Проверки expect — полный набор

##### Видимость и состояние

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

##### Текст

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

##### Значения и атрибуты

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

##### Доступность

```python
expect(loc).to_have_accessible_name("Сумма")
expect(loc).to_have_role("button")
```

##### Страница

```python
expect(page).to_have_title("Mini Exchange")
expect(page).to_have_url(re.compile(r"/app/$"))
```

##### Отрицания, таймаут, сообщение

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

##### ARIA snapshot — проверка структуры блока целиком

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

##### Мгновенные методы — НЕ для проверок

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

#### 6. Пример: ордер — от создания до отмены

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

#### 7. Частые ошибки

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

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u1_02_locators_assertions.py`

```text
U1. Урок 2 — локаторы и проверки подробно.

Теория: practice/u1_02_locators_assertions.md
Запуск:
    uv run pytest tests/ui/test_u1_02_locators_assertions.py --base-url http://localhost:8080 --headed

Правила для всех задач:
    - только page.goto("/app/") (без полного адреса);
    - уникальный email через uuid4;
    - локаторы по приоритету: роль → label/placeholder/text → test-id → CSS. XPath нельзя;
    - никаких sleep, is_visible() и count() в проверках — только expect.

Задача 0. Хелперы.
    Напиши функции register(page) -> str (регистрирует нового пользователя и ждёт кабинет)
    и deposit(page, asset, amount) (пополняет и ждёт тост "Баланс <asset> пополнен").
    Используй их в задачах ниже.

Задача 1. Форма входа целиком.
    Открой /app/. Одной проверкой to_match_aria_snapshot проверь блок auth-page:
    заголовок "Вход" уровня 2, поля Email и Пароль, кнопки "Войти" и "Зарегистрироваться".
    Отдельно: у поля Пароль атрибут type="password", у поля Email — type="email".

Задача 2. Пустой список ордеров.
    Новый пользователь: виден текст "Ордеров пока нет", строк ордеров 0 (to_have_count).

Задача 3. Три ордера и фильтры локаторов.
    Пополни USDT 1000 и ETH 10. Размести три ордера на ETH-USDT:
        BUY  цена 100 кол-во 1
        BUY  цена 101 кол-во 1
        SELL цена 500 кол-во 2
    Сторону выбирай через get_by_label("Купить"/"Продать").check().
    Проверь:
        - строк ордеров 3;
        - строк с SELL ровно 1 (filter(has_text=...));
        - у всех статус NEW — ОДНОЙ проверкой списком (to_have_text([...]));
        - у строки SELL в колонке "Исполнено" 0 (get_by_test_id("order-filled") внутри строки).

Задача 4. Отмена конкретного ордера.
    Создай два BUY-ордера с ценами 100 и 200. Отмени тот, что с ценой 200:
    найди строку по цене (не через nth!), нажми "Отменить" внутри строки.
    Проверь:
        - у этой строки статус CANCELED, кнопки "Отменить" в ней больше нет (to_have_count(0));
        - у ордера с ценой 100 статус по-прежнему NEW и кнопка есть;
        - выбери фильтр "Статус" = CANCELED: в таблице одна строка, и в ней цена 200.

Задача 5. Ошибка валидации ордера.
    Нажми "Разместить ордер" с пустыми ценой и количеством.
    Проверь: ошибка (role="alert" внутри формы ордера) видна и содержит "price" и "quantity"
    (to_contain_text или регулярка). Тост не появился.

Задача 6. Блокировка средств.
    Пополни USDT 1000, размести BUY ETH-USDT цена 100 кол-во 2.
    Проверь в строке USDT таблицы балансов: "Доступно" 800, "Заблокировано" 200.
    Отмени ордер — снова 1000 и 0.
    Подсказка: числа могут прийти как "800" или "800.00" — подумай, какую проверку выбрать
    (to_have_text с регуляркой?). Если результат не совпадает с ожидаемым — это повод
    разобраться, а не подгонять тест.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в секции «Ответы»):
    1. Как работает get_by_role? Что такое accessible name? So how does it works browser build accesability tree in the dom tree and playwright looking for the element with role
    2. Как найти кнопку в нужной строке таблицы? find string in the table for example using has-text and than in founded element finds needed element
    3. Чем отличаются to_have_text и to_contain_text? Как проверить список? to have text checking the whole text, and containing only the part
    4. Почему не assert loc.is_visible() / assert loc.count() == 3? is visible works without timing , count with timeot may be
    5. Что делать, если у элементов нет ни ролей, ни test-id? asks for developers to add ids
    6. Чем отличаются to_be_hidden, not_to_be_visible, to_be_attached, to_have_count(0)? to be hidden - may be with disable state, no to be visible - disable state, to be attached may be only in the dom tree
    , count can be not visible may be but exists in the dom tree
    7. Как проверить структуру формы целиком? using aria snapshow in the yaml format, codegen suits very good with it
```

<a id="u1-3"></a>

## U1.3 Как устроен Playwright

*Теория: `practice/u1_03_architecture.md`*

Задания: `practice/u1_03_architecture.py` (скрипты без pytest — так видно, что делают фикстуры).

Этот урок почти целиком про собеседование: «чем Playwright отличается от Selenium и Cypress»
спрашивают практически всегда, и ответ «он быстрее» засчитывают слабо. Нужно объяснить **почему**.

---

#### 1. Три процесса

Когда ты запускаешь тест, работают три отдельные программы:

```
┌──────────────────┐   pipe / JSON    ┌──────────────────┐   CDP / свой протокол   ┌───────────┐
│ Python-клиент    │ ───────────────► │ Driver (Node.js) │ ──────────────────────► │  Браузер  │
│ твой тест,       │ ◄─────────────── │ вся логика       │ ◄────────────────────── │ Chrome /  │
│ пакет playwright │   события        │ Playwright       │   события               │ FF / WK   │
└──────────────────┘                  └──────────────────┘                         └───────────┘
```

1. **Python-клиент** — пакет `playwright`, который ты импортируешь. Он тонкий: превращает вызов
   `page.click(...)` в JSON-сообщение и отправляет его драйверу.
2. **Driver** — процесс на Node.js, он лежит внутри pip-пакета (`playwright/driver/`). Здесь вся
   логика Playwright: ожидания, actionability-проверки, поиск локаторов, retry в `expect`, трейсы.
   Один и тот же драйвер работает для Python, Java, .NET — поэтому API во всех языках одинаковый.
3. **Браузер** — отдельный процесс. Драйвер общается с ним по протоколу отладки браузера.

Клиент и драйвер общаются через **pipe** (stdin/stdout процесса) — сообщения в JSON, соединение
одно на всё время работы.

##### Одно постоянное соединение и события

Соединение с браузером держится открытым весь прогон. Это двусторонний канал:

- тест отправляет команды (кликни, введи текст);
- браузер **сам** присылает события: страница загрузилась, пришёл ответ сети, в консоли ошибка,
  открылась новая вкладка, появился диалог.

Поэтому Playwright может, например, ждать ответ сервера (`expect_response`), слушать консоль
(`page.on("console", ...)`), перехватывать запросы — ему не надо опрашивать браузер «ну что, уже?».

##### Посмотреть своими глазами

```bash
DEBUG=pw:api      uv run python script.py   # какие команды Playwright выполняет и что ждёт
DEBUG=pw:protocol uv run python script.py   # сырые сообщения между драйвером и браузером
```

Вывод `pw:protocol` для Chrome выглядит так:

```
pw:protocol SEND ► {"id":3,"method":"Target.createBrowserContext","params":{"disposeOnDetach":true}}
pw:protocol ◀ RECV {"id":3,"result":{"browserContextId":"0DB7FB8E..."}}
```

Это и есть CDP: JSON с методом и параметрами, ответ приходит с тем же `id`.

---

#### 2. Протоколы браузеров

**CDP (Chrome DevTools Protocol)** — протокол, через который работает вкладка DevTools в Chrome.
Он умеет всё: DOM, сеть, консоль, эмуляция устройств, производительность. Playwright управляет
Chromium, Chrome и Edge через CDP.

**Firefox и WebKit** не поддерживают CDP в нужном объёме. Команда Playwright **собирает свои
версии** этих браузеров с патчами, добавляющими протокол управления (для Firefox он называется
Juggler). Поэтому `playwright install firefox` скачивает не обычный Firefox, а специальную сборку.
И поэтому WebKit в Playwright — это движок Safari, но не сам Safari.

##### Как это у Selenium: W3C WebDriver

```
Тест ──HTTP-запрос──► chromedriver ──CDP──► Chrome
     ◄──HTTP-ответ───
```

- **WebDriver** — стандарт W3C. Каждая команда — **отдельный HTTP-запрос** к драйверу браузера
  (`chromedriver`, `geckodriver`, `safaridriver`), каждый браузер поставляет свой драйвер.
- Протокол **запрос-ответ**: браузер не может сам сообщить о событии. Чтобы узнать, появился ли
  элемент, тест опрашивает его снова и снова (polling).
- Плюс: стандарт, работают **настоящие** браузеры всех вендоров, включая Safari; огромная
  экосистема и Selenium Grid.
- Новый стандарт **WebDriver BiDi** добавляет двусторонний канал и события — Selenium и Playwright
  постепенно на него переходят. Знать на уровне «есть такое» достаточно.

##### Как это у Cypress: внутри браузера

- Тест-код Cypress **выполняется внутри браузера**, в той же вкладке, что и приложение.
  Плюсы: прямой доступ к приложению, отличный интерактивный раннер, удобная отладка.
- Минусы — следствия той же архитектуры:
  - только **JavaScript / TypeScript**;
  - **одна вкладка**: нельзя открыть вторую вкладку или окно;
  - переходы между доменами ограничены (нужен `cy.origin`);
  - нет WebKit в полноценном виде, параллельность — через платный Cypress Cloud или сторонние решения.

##### Сравнение

| | Playwright | Selenium | Cypress |
|---|---|---|---|
| Где работает тест | отдельный процесс | отдельный процесс | внутри браузера |
| Связь с браузером | одно постоянное соединение, CDP / свои протоколы | HTTP-запрос на каждую команду (W3C WebDriver) | изнутри страницы |
| События от браузера | да, приходят сами | нет (BiDi — в процессе) | да |
| Ожидания | авто: actionability + retry `expect` | вручную: явные / неявные ожидания | авто, retry команд |
| Браузеры | Chromium, Firefox, WebKit (свои сборки) | все настоящие, включая Safari | Chromium, Firefox, (WebKit экспериментально) |
| Языки | Python, JS/TS, Java, C# | почти все | только JS/TS |
| Вкладки, окна, домены | без ограничений | без ограничений | одна вкладка, домены ограничены |
| Изоляция тестов | BrowserContext за мс | обычно новый браузер (секунды) | очистка состояния между тестами |
| Сеть: мок, перехват | встроено | только через прокси / CDP / BiDi | встроено |
| Отладка | Inspector, Trace Viewer | логи, скриншоты | интерактивный раннер, time travel |

---

#### 3. Почему Playwright быстрее и стабильнее — по пунктам

1. **Нет HTTP на каждую команду.** Одно соединение, сообщения идут без накладных расходов на запрос.
2. **Ожидания внутри драйвера.** Selenium-тест сам опрашивает браузер по сети, Playwright ждёт
   рядом с браузером и реагирует на события.
3. **BrowserContext вместо нового браузера.** Изоляция теста стоит миллисекунды, а не секунды.
4. **Actionability-проверки** перед каждым действием убирают целый класс флейков
   («кликнули по кнопке, пока её перекрывал спиннер»).

Честная оговорка: на скорость теста гораздо сильнее влияет **само приложение** и подготовка
данных (через UI или через API), чем выбор инструмента.

---

#### 4. Browser, BrowserContext, Page — без фикстур

То, что фикстуры pytest-playwright делают за тебя:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:                         # запускает драйвер
    browser = p.chromium.launch(channel="chrome")    # запускает браузер (дорого, ~1 с)
    context = browser.new_context()                  # чистый профиль (дёшево, мс)
    page = context.new_page()                        # вкладка
    page.goto("http://localhost:8080/app/")
    print(page.title())
    context.close()
    browser.close()
```

Полезные параметры:

```python
p.chromium.launch(headless=False, slow_mo=500, channel="chrome")
browser.new_context(
    base_url="http://localhost:8080",
    viewport={"width": 1280, "height": 720},
    locale="ru-RU",
    timezone_id="Europe/Moscow",
    record_video_dir="videos/",
)
p.devices["iPhone 13"]          # готовые профили устройств: browser.new_context(**p.devices["iPhone 13"])
```

Подробно про context (cookies, storage_state, два пользователя) — U1.4.

---

#### 5. sync и async API

У Playwright для Python два API с одинаковыми методами:

```python
# sync
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page()
    page.goto("http://localhost:8080/app/")
```

```python
# async
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page()
        await page.goto("http://localhost:8080/app/")

asyncio.run(main())
```

**Как они связаны.** Внутри Playwright for Python асинхронный. Sync API — это обёртка: каждый
вызов запускает асинхронную операцию и ждёт её результата (через библиотеку `greenlet`).
Поэтому функционально они одинаковые.

**Какой выбирать:**

- **sync** — для тестов на pytest. Проще читать, `pytest-playwright` даёт sync-фикстуры. Это стандарт.
- **async** — когда весь проект на asyncio (парсеры, сервисы, боты), или нужно управлять многими
  страницами одновременно в одном процессе (`asyncio.gather`). Для pytest нужен плагин
  `pytest-asyncio` и свои фикстуры.

**Ограничение:** sync API нельзя вызывать внутри работающего event loop — будет ошибка
`It looks like you are using Playwright Sync API inside the asyncio loop`. Внутри `async def`
используй async API.

##### asyncio.gather — параллельно не значит быстрее

```python
async def open_page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("http://localhost:8080/app/")
    await context.close()

await asyncio.gather(*(open_page(browser) for _ in range(5)))   # 5 страниц «одновременно»
```

На нашем стенде 5 лёгких страниц через `gather` открываются **не быстрее**, чем по очереди:
страница грузится за десятки миллисекунд, а параллельная работа добавляет нагрузку на браузер
и машину. `async` выигрывает, когда много **ожидания** (медленная сеть, долгие ответы сервера).
Для ускорения тестов используют не async, а параллельный запуск тестов (`pytest-xdist`, U7).

---

#### 6. CDP-сессия напрямую

Для Chromium можно отправить в браузер любую команду CDP, даже если в API Playwright её нет:

```python
cdp = context.new_cdp_session(page)
cdp.send("Performance.enable")
metrics = cdp.send("Performance.getMetrics")["metrics"]
# [{'name': 'Nodes', 'value': 314}, {'name': 'JSHeapUsedSize', 'value': 1417236}, ...]

cdp.send("Network.enable")
cdp.send("Network.emulateNetworkConditions", {          # медленная сеть
    "offline": False, "latency": 500,
    "downloadThroughput": 50 * 1024, "uploadThroughput": 50 * 1024,
})
```

Работает только в Chromium — для Firefox и WebKit CDP нет. Это и есть ответ на вопрос
«что делать, если в Playwright нет нужной возможности».

---

#### 7. Установка браузеров и версии

- Каждая версия pip-пакета `playwright` привязана к **конкретным версиям** браузеров.
  После обновления пакета — снова `playwright install`.
- Браузеры лежат в кэше (`~/Library/Caches/ms-playwright` на macOS), а не в проекте.
- `channel="chrome"` / `--browser-channel chrome` — взять установленный Chrome. Плюс: настоящий
  браузер пользователя. Минус: версия не зафиксирована, может обновиться сам.
- В CI используют официальный Docker-образ `mcr.microsoft.com/playwright/python` — там уже всё
  установлено (U7).

---

#### Собес: вопросы и ответы

**1. Чем Playwright отличается от Selenium?**
> Архитектурой. Selenium работает по стандарту W3C WebDriver: каждая команда — отдельный HTTP-запрос
> к драйверу браузера, протокол запрос-ответ, событий от браузера нет, поэтому ожидания делаются
> опросом, и пишешь их сам — явные ожидания. Playwright держит одно постоянное соединение с браузером
> через CDP для Chromium и собственные протоколы в патченных сборках Firefox и WebKit; браузер сам
> присылает события. Отсюда автоожидания и web-first assertions из коробки, перехват сети,
> несколько вкладок и контекстов, изоляция через BrowserContext за миллисекунды. Плюсы Selenium:
> это стандарт, работают настоящие браузеры всех вендоров, включая Safari, большая экосистема и Grid.

**2. Чем Playwright отличается от Cypress?**
> Cypress выполняет тесты внутри браузера, в одной вкладке с приложением. Это даёт удобную отладку,
> но ограничивает: только JS/TS, одна вкладка, сложности с переходом между доменами. Playwright
> управляет браузером снаружи: любые вкладки, окна, домены, несколько пользователей в одном тесте,
> три движка браузера и языки Python, Java, C#, JS.

**3. Как устроен Playwright внутри?**
> Три процесса. Python-клиент — тонкая обёртка, он отправляет команды в JSON. Драйвер на Node.js —
> там вся логика: ожидания, локаторы, retry в expect; общий для всех языков. Браузер — с ним драйвер
> общается по CDP или по своему протоколу. Соединения постоянные, браузер сам присылает события:
> сеть, консоль, новые вкладки.

**4. Почему Playwright не может работать с обычным Firefox или Safari?**
> Ему нужен протокол управления с событиями. У Chromium есть CDP. Для Firefox и WebKit команда
> Playwright собирает свои версии с патчами, которые добавляют такой протокол. Поэтому WebKit
> в Playwright — это движок Safari, но не сам Safari; поведение очень близкое, но не 100%.

**5. sync или async API — что выбираешь и почему?**
> Для тестов — sync: проще читать, pytest-playwright даёт sync-фикстуры. Sync — это обёртка над
> async, функционально они одинаковые. Async беру, если весь проект на asyncio или нужно управлять
> многими страницами одновременно в одном процессе. Тесты ускоряю не через async, а через
> параллельный запуск — pytest-xdist.

**6. Что делать, если нужной возможности нет в API Playwright?**
> Для Chromium — CDP-сессия: `context.new_cdp_session(page)` и любые команды протокола, например
> эмуляция медленной сети или метрики производительности. Ограничение — только Chromium.
> Иначе — `page.evaluate` с JavaScript на странице.

**7. Почему тесты на Playwright стабильнее?**
> Перед действием драйвер проверяет, что элемент видим, стабилен, включён и не перекрыт;
> `expect` повторяет проверку до таймаута; локаторы ищут элемент заново каждый раз. Это убирает
> основные источники флейков — гонки с отрисовкой и устаревшие ссылки на элементы.

### Задания — `practice/u1_03_architecture.py`

```text
U1. Урок 3 — как устроен Playwright.

Теория: practice/u1_03_architecture.md
Здесь не pytest, а обычные скрипты: без фикстур видно, что они делают за тебя.
Запуск:  uv run python practice/u1_03_architecture.py
Каждую задачу оформи функцией task_N() и вызывай нужную внизу в if __name__ == "__main__".
Браузер везде: p.chromium.launch(channel="chrome").

Задача 1. Sync без pytest.
    sync_playwright → browser (headless=False, slow_mo=300) → context (base_url="http://localhost:8080")
    → page. Открой "/app/", зарегистрируй нового пользователя, выведи print'ом текст user-email.
    Закрой context и browser.

Задача 2. То же на async API.
    async_playwright, все вызовы с await, запуск через asyncio.run(...).

Задача 3. Заглянуть внутрь.
    Запусти задачу 1 с DEBUG=pw:api, затем с DEBUG=pw:protocol (в терминале, перед командой).
    Запиши в «Ответы»:
        - какие проверки Playwright делал перед кликом по "Зарегистрироваться" (pw:api);
        - названия CDP-методов: создание context, переход по адресу, клик мышью (pw:protocol;
          ищи grep'ом "method").

Задача 4. Профиль устройства.
    Создай context из p.devices["iPhone 13"], открой /app/, сделай скриншот
    page.screenshot(path="iphone.png"). Выведи page.viewport_size.

Задача 5. CDP-сессия.
    а) Выведи метрики Nodes и JSHeapUsedSize для /app/ (Performance.getMetrics).
    б) Замерь время page.goto("/app/") (time.perf_counter) обычно и с эмуляцией медленной сети
       (Network.emulateNetworkConditions, latency 500). Выведи оба числа.

Задача 6. gather против очереди.
    async: функция открывает новый context, страницу /app/, закрывает context.
    Замерь 5 вызовов через asyncio.gather и 5 вызовов по очереди. Сделай один «прогревочный»
    вызов перед замерами. Запиши результат в «Ответы» и объясни, почему он такой.

Задача 7. Ошибка sync внутри async.
    Внутри async def вызови sync_playwright(). Запиши текст ошибки и объясни, почему так.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Чем Playwright отличается от Selenium? instead of sending http requests every time, playwright holds one connection and waiting for the event from the browser, its based on cdp protocol and works thwo websockets with autowaiting

    2. Чем Playwright отличается от Cypress?
    3. Как устроен Playwright внутри? it has 3 layers , python client - send json commands to the node js driver (here is all logics ) via cdp into browser
    4. Почему Playwright не может работать с обычным Firefox или Safari? firefox and safari have no cdp, only patching aproaches
    5. sync или async API — что выбираешь и почему? sync it gives the same speed
    6. Что делать, если нужной возможности нет в API Playwright? make own helpers and utilz
    7. Почему тесты на Playwright стабильнее? have autowaitings
```

<a id="u1-4"></a>

## U1.4 BrowserContext, ожидания и pytest для UI

*Теория: `practice/u1_04_context_pytest.md`*

Задания: `tests/ui/test_u1_04_context_pytest.py` и `tests/ui/conftest.py`.

План: что именно изолирует context и как этим пользоваться (два пользователя, сохранённый логин);
как Playwright ждёт перед каждым действием; pytest-часть — фикстуры, conftest, parametrize, маркеры
и настройка pytest-playwright под проект.

---

#### 1. BrowserContext — что изолирует

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

##### Полезное API context

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

##### Две вкладки в одном context

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

##### Два пользователя — два context

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

#### 2. storage_state — не логиниться в каждом тесте

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

#### 3. Как Playwright ждёт перед действием (actionability)

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

##### Таймауты

| Что | По умолчанию | Как поменять |
|---|---|---|
| действия (`click`, `fill`…) | 30 с | `page.set_default_timeout(10_000)` / `context.set_default_timeout` |
| навигация (`goto`, `wait_for_url`) | 30 с | `page.set_default_navigation_timeout(...)` |
| `expect` | 5 с | `expect.set_options(timeout=...)`, `timeout=` в проверке |
| тест целиком | нет | плагин `pytest-timeout` |

##### Итог: четыре механизма стабильности

1. **Ленивые локаторы** — элемент ищется заново при каждом действии, нет stale element.
2. **Actionability** — перед действием ждёт видимость, стабильность, enabled, отсутствие перекрытия.
3. **Web-first assertions** — `expect` повторяет проверку до таймаута.
4. **Strict mode** — локатор нашёл несколько элементов → ошибка, а не клик «по первому».

---

#### 4. Фикстуры pytest — основа

Фикстура — функция с `@pytest.fixture`; тест получает её результат по имени аргумента.

```python
import pytest

@pytest.fixture
def user_email() -> str:
    return f"user_{uuid4().hex[:8]}@test.com"

def test_something(user_email):     # pytest вызвал user_email() и передал результат
    ...
```

##### setup и teardown через yield

```python
@pytest.fixture
def second_page(context):
    page = context.new_page()      # setup — до теста
    yield page                     # тест работает здесь
    page.close()                   # teardown — после теста, даже если тест упал
```

##### Scope — сколько живёт фикстура

| scope | создаётся | пример |
|---|---|---|
| `function` (по умолч.) | на каждый тест | `page`, `context` |
| `class` | на класс тестов | |
| `module` | на файл | |
| `session` | один раз на прогон | `browser`, `playwright`, `browser_context_args` |

Правило: фикстура **не может** зависеть от фикстуры с более коротким scope
(session-фикстура не может взять `page`) — будет `ScopeMismatch`.

##### Фикстура от фикстуры

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

##### Фабрика — когда нужно несколько объектов

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

##### autouse

`@pytest.fixture(autouse=True)` — выполняется для каждого теста без указания в аргументах.
Например, выставить таймауты всем страницам:

```python
@pytest.fixture(autouse=True)
def short_timeouts(page):
    page.set_default_timeout(10_000)
```

---

#### 5. conftest.py

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

#### 6. Настройка pytest-playwright под проект

##### Фикстуры, которые дал плагин

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

##### Переопределить настройки context для всех тестов

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

##### Только для одного теста — маркер

```python
@pytest.mark.browser_context_args(viewport={"width": 375, "height": 667}, locale="en-US")
def test_mobile_layout(page):
    ...
```

##### Параметры запуска браузера

```python
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--start-maximized"]}
```

##### base_url в конфиге вместо опции

```toml
# pyproject.toml
[tool.pytest.ini_options]
base_url = "http://localhost:8080"
```

Опция `--base-url` в командной строке перекрывает значение из конфига — так переключают окружение.

---

#### 7. parametrize

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

#### 8. Маркеры

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

#### 9. Полезные опции pytest

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

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u1_04_context_pytest.py`

```text
U1. Урок 4 — BrowserContext, ожидания и pytest для UI.

Теория: practice/u1_04_context_pytest.md
Запуск:
    uv run pytest tests/ui/test_u1_04_context_pytest.py -v

Задача 1. Настройка проекта (pyproject.toml и tests/ui/conftest.py).
    а) В pyproject.toml в [tool.pytest.ini_options] добавь base_url = "http://localhost:8080".
       Проверь, что тесты U1.2 запускаются без --base-url.
    б) В conftest.py переопредели browser_context_args: locale "ru-RU",
       viewport 1440x900. Не потеряй настройки плагина.
    в) Зарегистрируй маркер smoke в pyproject.toml.

Задача 2. Фикстуры в conftest.py.
    - user_email — уникальный email (uuid4).
    - logged_in_page — берёт page и user_email, регистрирует пользователя, ждёт кабинет,
      возвращает page.
    - create_user — фабрика: каждый вызов создаёт НОВЫЙ context (через фикстуру new_context),
      регистрирует в нём нового пользователя и возвращает page.
    - deposit-хелпер оставь обычной функцией (как в U1.2) — где его держать, реши сам.

Задача 3. Изоляция context.
    test_logged_in: через logged_in_page проверь, что в localStorage есть токен:
        page.evaluate("localStorage.getItem('token')") не None.
    test_fresh_context: с обычной page открой /app/ — видна форма входа, токена нет.
    Запусти оба теста вместе — объясни в «Ответах»,
    почему второй не видит логина первого.

Задача 4. Две вкладки одного context.
    Через logged_in_page открой вторую вкладку в ТОМ ЖЕ context (page.context.new_page()),
    перейди на /app/ — проверь, что там тоже кабинет и тот же email.
    Нажми «Выйти» во второй вкладке, перезагрузи первую (reload) — что увидишь и почему?

Задача 5. Два пользователя: продавец и покупатель.
    create_user() дважды. Продавец пополняет ETH 1 и выставляет SELL ETH-USDT цена 100 кол-во 1.
    Покупатель пополняет USDT 1000 и выставляет BUY ETH-USDT цена 100 кол-во 1.
    Проверь у обоих: ордер исполнился (статус FILLED). Сопоставление идёт в фоне, таблица
    обновляется раз в 2 с — подумай про timeout у expect.
    Затем проверь балансы: у продавца USDT 100 доступно, у покупателя ETH 1 и USDT 900.
    Если что-то не совпало — сначала убедись, что тест прав, потом разбирайся со стендом.

Задача 6. storage_state.
    Создай пользователя через create_user, сохрани state: page.context.storage_state().
    Новый context с этим state (new_context(storage_state=...)) → /app/ сразу кабинет без логина.
    Выйди в новом context. Первый context после reload — всё ещё залогинен? Почему?

Задача 7. parametrize: неверные суммы пополнения.
    Через logged_in_page пополни USDT суммами: "0", "-5", "abc", "" — один тест, четыре набора,
    читаемые ids. Проверь: тост НЕ «Баланс USDT пополнен» (to_have_text с not_ или регулярка),
    доступный USDT остался 0.

Задача 8. Маркеры.
    Пометь задачи 3 и 5 как smoke. Запусти: uv run pytest -m smoke -v (должно быть 3 теста).
    Убедись, что опечатка @pytest.mark.smok даёт ошибку, и объясни почему.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое BrowserContext и зачем новый context на каждый тест?
    2. Как в одном тесте сыграть за двух пользователей?
    3. Как не логиниться в каждом тесте?
    4. Что Playwright проверяет перед кликом?
    5. Как устроены фикстуры pytest? Что такое scope, yield, conftest?
    6. Как настроить pytest-playwright под проект?
    7. Зачем --strict-markers и что такое xfail?
```

<a id="u1-5"></a>

## U1.5 Собеседование по модулю U1

*Теория: `practice/u1_05_interview.md`*

Задания:
- `practice/u1_05_review_me.py` — ревью чужого плохого теста (частое задание на собесе);
- `tests/ui/test_u1_05_livecoding.py` — лайвкодинг на время.

Урок закрывает модуль: шпаргалка на одну страницу, банк вопросов с ответами (включая те,
что были в U1.1–U1.4, и новые), как вести себя на лайвкодинге и ревью.

---

#### 1. Шпаргалка по модулю

##### Архитектура
- Python-клиент → (pipe, JSON) → driver на Node.js (вся логика) → (CDP / свой протокол) → браузер.
- Одно постоянное соединение, браузер сам присылает события.
- Chromium — CDP; Firefox, WebKit — патченные сборки со своим протоколом.
- Selenium — W3C WebDriver, HTTP на команду, без событий (BiDi — в процессе). Cypress — внутри браузера, JS, одна вкладка.

##### Объекты
- `browser` — процесс, один на прогон. `context` — изолированный профиль, новый на тест (мс). `page` — вкладка.
- Изолирует context: cookies, localStorage/sessionStorage, кэш, разрешения, настройки.
- Два пользователя = два context. Вкладки одного context делят логин.
- `storage_state` — сохранённые cookies + localStorage, чтобы не логиниться каждый раз.

##### Локаторы
- Приоритет: `get_by_role` (+name) → `get_by_label` / `placeholder` / `text` → `get_by_test_id` → CSS по атрибутам → XPath (почти никогда).
- Ленивые: ищутся заново при каждом действии → нет stale element.
- Strict mode: нашёл несколько для действия → ошибка.
- Уточнение: цепочки, `filter(has_text / has / has_not_text / has_not / visible)`, `first/last/nth`, `and_/or_`.
- Таблица: найти строку по неизменному признаку → действие и проверка внутри строки.

##### Ожидания
- Actionability перед действием: attached, visible, stable, receives events, enabled (editable для fill). Таймаут действия 30 с.
- `expect` повторяет проверку до 5 с. `is_visible()`, `count()`, `text_content()` — мгновенные, не для проверок.
- Ждать признак, уникальный для этого действия (не тост, оставшийся от прошлого).
- `sleep` — никогда.

##### pytest
- Фикстуры: scope, `yield` для teardown, фикстура от фикстуры, фабрики, `autouse`, `conftest.py` по папкам.
- pytest-playwright: `page`, `context`, `new_context`, `browser`, `browser_context_args`, `browser_type_launch_args`, `base_url`.
- `parametrize` с `ids`, маркеры (`--strict-markers`), `xfail` для известных багов.
- Опции: `--headed`, `--slowmo`, `--browser`, `--browser-channel`, `--device`, `--base-url`, `--tracing/--screenshot/--video retain-on-failure`.

##### Отладка
- `--headed --slowmo`, `PWDEBUG=1`, `page.pause()`, `codegen`, `DEBUG=pw:api`, Trace Viewer.

---

#### 2. Банк вопросов

Отвечай вслух, по структуре: **что это → как работает → зачем / пример из практики**.
40–90 секунд на ответ. Пример из практики («на прошлом проекте...» / «на моём стенде...»)
сильно повышает оценку.

##### Инструмент и архитектура

**1. Почему Playwright, а не Selenium?**
> Архитектура: одно постоянное соединение с событиями вместо HTTP на каждую команду; отсюда
> автоожидания и web-first assertions — меньше флейков и кода ожиданий. Context за миллисекунды
> вместо нового браузера — быстрая изоляция. Из коробки перехват сети, трейсы, несколько вкладок
> и пользователей, API-клиент. Selenium выберу, если нужен настоящий Safari или уже есть
> инфраструктура на Grid и большой набор тестов.

**2. Чем Playwright отличается от Cypress?**
> Cypress выполняется внутри браузера: удобная отладка, но только JS/TS, одна вкладка,
> ограничения на домены. Playwright управляет браузером снаружи: любые вкладки и домены,
> несколько пользователей, три движка, Python/Java/C#/JS.

**3. Как устроен Playwright?**
> Три процесса: тонкий клиент на твоём языке, драйвер на Node.js с логикой ожиданий и локаторов,
> браузер. Клиент с драйвером — через pipe в JSON, драйвер с браузером — CDP для Chromium,
> свои протоколы для патченных Firefox и WebKit. Соединения постоянные, события приходят сами.

**4. Тесты проходят в Chromium, падают в WebKit. Что делаешь?**
> Сначала смотрю трейс упавшего теста — где именно расходится. Частые причины: разная отрисовка
> и шрифты (элемент перекрыт, другой размер), даты и локаль, поддержка API браузера, поведение
> фокуса и клавиатуры. Проверяю вручную в настоящем Safari: если баг воспроизводится — это баг
> продукта. Если только в WebKit Playwright — учитываю, что это не 100% Safari, и при
> необходимости помечаю `skip_browser` с объяснением.

**5. sync или async?**
> Для тестов sync: проще, pytest-playwright даёт sync-фикстуры. Sync — обёртка над async,
> возможности одинаковые. Async — если проект на asyncio. Ускоряю тесты параллельным запуском,
> а не async.

**6. Headless и headed — есть ли разница в поведении?**
> Движок тот же, но бывают отличия: размер окна по умолчанию, отсутствие GPU, иногда разная
> отрисовка и тайминги. Поэтому viewport задаю явно в настройках context, а в CI использую
> тот же режим и образ, что и при отладке, и разбираю падения по трейсу.

##### Локаторы

**7. Какие локаторы выбираешь и почему не XPath?**
> `get_by_role` с именем — как видит пользователь, плюс проверка доступности. Дальше label,
> placeholder, text. `data-testid` — когда ролей нет или текст меняется (локализация). XPath и
> длинный CSS привязаны к структуре вёрстки: лишний `div` — и тест упал, хотя для пользователя
> ничего не изменилось.

**8. Как работает get_by_role? Что такое accessible name?**
> Поиск по дереву доступности, которое браузер строит для скринридеров. Роль — от тега или
> атрибута `role`. Имя — из `aria-labelledby`, `aria-label`, `<label>`, текста, `title`.
> Ловит проблемы доступности: «кнопка» из div не найдётся.

**9. Как найти кнопку в нужной строке таблицы?**
> Нахожу строку по уникальному и неизменному признаку — `filter(has_text=...)` или `has=` с точной
> ячейкой, или по `data-id`. Кнопку ищу внутри строки цепочкой. `nth` — только если порядок
> гарантирован.

**10. Что такое strict mode и ленивые локаторы?**
> Локатор — описание поиска, а не ссылка на элемент; ищется заново при каждом действии, поэтому
> нет StaleElementReference. Strict mode — если для действия нашлось больше одного элемента,
> ошибка, а не клик по первому.

**11. Разработчики не ставят test-id и роли. Что делаешь?**
> Договариваюсь: `data-testid` или нормальная семантическая разметка — это ещё и доступность,
> аргумент для продукта. Пока нет — CSS по стабильным атрибутам, поиск внутри контейнера, filter.
> XPath — последний вариант.

##### Ожидания и стабильность

**12. Почему expect, а не assert?**
> `expect` — web-first: повторяет проверку до таймаута. UI асинхронный, `assert` проверяет один
> раз и ловит промежуточное состояние → флейк. `assert` — для уже полученных данных: API, БД.

**13. Что Playwright проверяет перед кликом?**
> Attached, visible, stable, receives events (не перекрыт), enabled; для fill — editable.
> Ждёт до таймаута действия. `force=True` пропускает проверки — почти всегда маскирует проблему.

**14. Тест флейкает. Как ищешь причину?**
> Воспроизвожу: прогоняю много раз (`--count` из pytest-repeat или цикл), смотрю трейсы упавших
> прогонов — на каком шаге и что было на странице. Типичные причины: ожидание неуникального
> признака (тост от прошлого действия), `is_visible`/`count` вместо `expect`, зависимость от
> порядка или общих данных, гонка с фоновым обновлением, неустойчивый локатор (`nth`). Чиню
> причину, а не увеличиваю таймауты и не добавляю `sleep`.

**15. Почему нельзя `time.sleep`?**
> Либо мало — тест флейкает, либо много — тест медленный, обычно и то и другое. Playwright ждёт
> по событиям сам; если нужно дождаться чего-то особого — `expect` на результат,
> `expect_response`, `wait_for_url`.

##### Изоляция, данные, pytest

**16. Что такое BrowserContext и зачем новый на каждый тест?**
> Изолированный профиль: cookies, storage, кэш, разрешения. Создаётся за миллисекунды в том же
> процессе браузера. Новый на тест — тесты независимы, порядок не важен, можно параллелить.

**17. Как в одном тесте два пользователя?**
> Два context. Вкладки одного context делят cookies и localStorage, поэтому не подходят.
> В pytest-playwright — фикстура `new_context` или своя фабрика.

**18. Как не логиниться в каждом тесте?**
> Логин один раз (лучше через API), `storage_state` в JSON, context создаю с ним. Учитываю
> истечение токена, общие данные пользователя, тесты логина — без state.

**19. Как готовишь тестовые данные?**
> Уникальные данные на каждый тест (uuid в email), подготовку — через API, а не через UI,
> если UI-часть не предмет теста. Тест не зависит от других тестов и от того, что осталось
> в базе. Faker — для правдоподобных данных, но не для уникальности.

**20. Как устроены фикстуры? scope, yield, conftest.**
> Функция, результат которой pytest передаёт по имени аргумента. До `yield` — setup, после —
> teardown (выполнится и при падении). Scope: function, class, module, session; нельзя зависеть
> от более короткого. `conftest.py` — общие фикстуры для папки и вложенных, можно переопределять.

**21. Как запустить тесты на другом окружении / в другом браузере?**
> `--base-url` (в тестах только относительные пути, значение по умолчанию — в конфиге),
> `--browser firefox`, `--device "iPhone 13"`. Секреты — в переменных окружения, не в коде.

**22. Как отлаживаешь упавший тест?**
> Локально — `--headed --slowmo`, `PWDEBUG=1`, `page.pause()`. В CI — трейс
> (`--tracing retain-on-failure`): действия, DOM до и после, сеть, консоль. Плюс скриншоты
> и видео при падении, и логи сервиса по request id.

---

#### 3. Ключевые ответы на английском

На собесах в международные компании те же вопросы задают по-английски.

**Why Playwright over Selenium?**
> Architecture. Selenium uses W3C WebDriver: an HTTP request per command, no events, so you write
> waits yourself. Playwright keeps one persistent connection — CDP for Chromium, its own protocols
> for patched Firefox and WebKit — and the browser pushes events. That gives auto-waiting,
> web-first assertions, network interception, cheap isolated contexts. Selenium still wins when
> you need real Safari or already have a large Grid setup.

**Which locators do you use?**
> Role-based locators with an accessible name first — they match what the user sees and check
> accessibility. Then label, placeholder, text. Test ids when there's no good role or the text
> changes. I avoid XPath and long CSS chains — they're coupled to the DOM structure and break
> on harmless markup changes.

**What is a BrowserContext?**
> An isolated browser profile, like an incognito window: its own cookies, storage, cache and
> permissions. It's created in milliseconds inside one browser process, so we get a fresh context
> per test — full isolation at almost no cost. Two users in one test means two contexts.

**How do you deal with flaky tests?**
> Reproduce by running the test many times, then read the traces of failed runs. Usual causes:
> waiting for a non-unique signal, instant checks instead of `expect`, shared data or test order,
> fragile locators. I fix the cause — never by adding sleeps or just raising timeouts.

---

#### 4. Лайвкодинг: как себя вести

1. **Уточни задачу** (30 с): что проверяем, какие данные, есть ли готовый пользователь.
2. **Скажи план вслух**: «зарегистрирую пользователя, пополню, размещу ордер, проверю строку».
3. **Пиши от простого**: сначала рабочий тест в лоб, потом вынеси повторы в хелпер / фикстуру.
4. **Говори, почему**: «беру `get_by_role`, потому что...», «`expect`, а не `assert`, потому что...».
5. **Запускай часто** с `--headed`: интервьюер видит, что ты проверяешь, а не гадаешь.
6. **Упало — читай ошибку вслух**: Playwright пишет, что ждал и что нашёл. Это тоже оценивают.
7. **Не успел** — скажи, что бы доделал: проверки, негативные случаи, вынос в фикстуры.

Типичные задачи: логин (позитив + негатив), форма с валидацией (`parametrize`), таблица
(найти строку, действие, проверка), модалка/тост, два пользователя.

---

#### 5. Ревью чужого теста: на что смотреть

Чек-лист — пройди по нему в задаче `practice/u1_05_review_me.py`:

| Проблема | Почему плохо | Как правильно |
|---|---|---|
| `time.sleep` | медленно и всё равно флейкает | `expect` на результат |
| `assert loc.is_visible()` / `count()` / `text_content()` | мгновенная проверка | `expect(loc).to_...` |
| XPath / длинный CSS | ломается от вёрстки | роль, label, test-id |
| `nth(0)` для «нужной» строки | порядок не гарантирован | `filter` по признаку |
| полный URL в `goto` | не переключить окружение | относительный путь + `base_url` |
| один и тот же email | тест падает на втором прогоне | uuid |
| тест зависит от другого теста | порядок, параллельность | каждый тест готовит данные сам |
| нет проверки в конце | тест ничего не проверяет | `expect` результата |
| проверка не того | «тост появился» вместо «баланс изменился» | проверять бизнес-результат |
| ждать неуникальный признак | гонка с прошлым действием | признак именно этого действия |
| копипаста шагов | тяжело поддерживать | хелпер / фикстура |
| `force=True` без причины | маскирует перекрытие | разобраться, что перекрывает |
| `try/except` вокруг проверки | тест никогда не падает | убрать |
| пароли и адреса в коде | секреты в git, нет гибкости | конфиг, переменные окружения |

### Задания — `tests/ui/test_u1_05_livecoding.py`

```text
U1. Урок 5 — лайвкодинг на время.

Теория и банк вопросов: practice/u1_05_interview.md
Запуск:
    uv run pytest tests/ui/test_u1_05_livecoding.py -v --headed

Правила как на собесе:
    - засекай время, укладывайся в лимит; не успел — запиши в «Ответы», что бы доделал;
    - говори вслух (можно себе под нос): план, почему этот локатор, почему expect;
    - НЕ подглядывай в свои решения U1.1–U1.4 и в теорию, пока не закончишь задачу.
      Можно: документация Playwright (playwright.dev/python) — на собесе её обычно разрешают;
    - фикстуры из conftest.py (logged_in_page, create_user) использовать можно, если они готовы.
      Если ещё нет — пиши всё в тесте, потом вынеси.

Задача 1. Логин — 10 минут.
    Зарегистрируй пользователя, выйди. Затем:
        - вход с верными данными → кабинет и email в шапке;
        - вход с неверным паролем → ошибка "Invalid email or password", кабинет скрыт;
        - вход с несуществующим email → та же ошибка.
    Подсказка по структуре: один тест на позитив, один с parametrize на два негатива.

Задача 2. Форма с валидацией — 15 минут.
    Форма ордера. parametrize с ids, минимум 5 наборов:
        пустая цена, отрицательная цена, цена "abc", нулевое количество, пустое количество.
    Для каждого: ошибка формы видна и содержит имя нужного поля (price / quantity),
    ордер не создан (строк 0), баланс не заблокирован.

Задача 3. Таблица — 15 минут.
    Создай 3 BUY-ордера с разными ценами. Отмени средний по цене.
    Проверь: у отменённого CANCELED и нет кнопки, у двух других NEW и кнопка есть,
    фильтр «Статус» = NEW показывает ровно 2 строки с нужными ценами (to_have_text списком —
    подумай о порядке строк).

Задача 4. Переписать плохие тесты — 20 минут.
    Сначала сделай ревью practice/u1_05_review_me.py (ответы — в том файле).
    Потом перепиши здесь test_2_deposit, test_3_order и test_4_cancel правильно:
    независимые тесты, свои данные, нормальные локаторы, expect, проверка бизнес-результата.

Задача 5. Два пользователя — 15 минут.
    Продавец: SELL BTC-USDT цена 50000 кол-во 0.1. Покупатель: BUY BTC-USDT цена 50000 кол-во 0.05.
    Проверь: у покупателя FILLED, у продавца PARTIALLY_FILLED и исполнено 0.05,
    у продавца в балансе BTC заблокировано 0.05.
    Затем продавец отменяет ордер: статус CANCELED, BTC заблокировано 0.

Задача 6. Устный собес — 20 минут.
    Включи диктофон и ответь вслух на 10 случайных вопросов из банка (раздел 2 теории),
    40–90 секунд на каждый, без подглядывания. Потом прослушай и сверь с ответами.
    Запиши в «Ответы» номера вопросов, на которых «поплыл», — их повторим.
```

### Файл для ревью — `practice/u1_05_review_me.py`

```python
"""U1. Урок 5 — ревью чужого теста.

Задание как на собесе: «Вот тест коллеги, проведи ревью».
Найди все проблемы (их больше 12) — используй чек-лист из раздела 5 теории
practice/u1_05_interview.md. Для каждой запиши в «Ответы»: строка — что не так — почему — как правильно.

Потом перепиши тесты правильно в tests/ui/test_u1_05_livecoding.py (задача 4).

Файл лежит в practice/, а не в tests/, — чтобы pytest его не запускал.
"""

import time

from playwright.sync_api import Page, expect

EMAIL = "qa_user@test.com"
PASSWORD = "password123"


def test_1_register(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("//form[@id='auth-form']/div/button[2]").click()
    time.sleep(2)
    assert page.locator("#dashboard").is_visible()


def test_2_deposit(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("#auth-form button[type=submit]").click()
    time.sleep(2)
    page.locator("#deposit-form select").select_option("USDT")
    page.locator("#deposit-form input").fill("1000")
    page.locator("#deposit-form button").click(force=True)
    time.sleep(1)
    assert page.locator(".toast").text_content() != ""


def test_3_order(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("#auth-form button[type=submit]").click()
    time.sleep(2)
    page.locator("input[name=price]").fill("100")
    page.locator("input[name=quantity]").fill("1")
    page.locator("#order-form button").click()
    time.sleep(3)
    try:
        assert page.locator("table").nth(1).locator("tr").nth(1).locator("td").nth(5).inner_text() == "NEW"
    except AssertionError:
        print("статус не NEW, но это иногда бывает")


def test_4_cancel(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("#auth-form button[type=submit]").click()
    time.sleep(2)
    page.locator("button.danger").first.click()
    time.sleep(2)
    assert page.locator("table").nth(1).locator("tr").count() > 0


# Ответы
"""
строка — что не так — почему — как правильно

"""
```


---

# U2. Ожидания и устойчивые тесты

<a id="u2-1"></a>

## U2.1 Web-first assertions и асинхронный UI

*Теория: `practice/u2_01_waiting_async_ui.md`*

Задания: `tests/ui/test_u2_01_waiting_async_ui.py`.

План: почему `expect` ждёт, а `assert` нет, и какие методы Locator «не ждут»; полный набор
проверок `expect`; как устроен асинхронный UI нашего стенда (автообновление, тосты, disabled-кнопки)
и где в нём ловушки; как ждать ответ сервера (`expect_response` / `expect_request`), URL, состояние
страницы и произвольное условие; как воспроизвести флейк медленной сетью; антипаттерны ожидания.

В U1.4 было про ожидание **перед действием** (actionability). Этот урок — про ожидание
**результата**: «после клика в таблице появилась строка», «баланс стал 1000».

---

#### 1. Два вида ожидания

| | Действие (`click`, `fill`…) | Проверка (`expect(...)`) |
|---|---|---|
| Чего ждёт | элемент готов к действию: видим, стабилен, enabled, не перекрыт | состояние стало ожидаемым: текст, количество, видимость |
| Таймаут по умолчанию | 30 с | 5 с |
| Что при таймауте | `TimeoutError` | `AssertionError` с логом попыток |

Действие ничего не проверяет о **результате**. `click()` вернулся — значит, клик случился,
а не «ордер создан». Результат подтверждает только проверка после действия.

---

#### 2. Почему `expect`, а не `assert`

UI асинхронный: после клика браузер отправляет запрос, ждёт ответ, перерисовывает DOM.
Тест на Python в это время уже идёт дальше.

```python
page.get_by_role("button", name="Пополнить").click()

# ПЛОХО: прочитали текст ОДИН раз — в этот момент таблица ещё старая
assert balance.text_content() == "1000"

# ХОРОШО: Playwright повторяет проверку, пока текст не станет "1000" (или 5 с)
expect(balance).to_have_text("1000")
```

Как `expect` повторяет: проверка выполняется на стороне драйвера, при неудаче — пауза
и снова (примерно 100 мс, 250 мс, 500 мс, дальше раз в секунду) до таймаута. Локатор ищется
заново на каждой попытке, поэтому перерисовка таблицы не мешает. Отсюда название
**web-first assertions** — проверки, которые знают, что веб асинхронный.

##### Методы Locator, которые НЕ ждут

Они возвращают значение **в моменте**. Для проверок их не используют:

| Метод | Чем заменить в проверке |
|---|---|
| `is_visible()`, `is_hidden()` | `to_be_visible()`, `to_be_hidden()` |
| `is_enabled()`, `is_disabled()`, `is_checked()`, `is_editable()` | `to_be_enabled()`, `to_be_disabled()`, `to_be_checked()`, `to_be_editable()` |
| `count()` | `to_have_count(n)` |
| `text_content()`, `inner_text()`, `all_text_contents()` | `to_have_text()`, `to_contain_text()` |
| `input_value()` | `to_have_value()` |
| `get_attribute()` | `to_have_attribute()` |

Важная деталь: `text_content()` / `input_value()` / `get_attribute()` **ждут, пока элемент
появится** (как действие), но значение не ждут — берут то, что есть сейчас. `is_visible()`
и `count()` не ждут вообще ничего.

Когда методы «в моменте» нужны: чтобы **взять значение** для дальнейших шагов (запомнить
id ордера, текущий баланс), или для ветвления в хелпере. Но не для проверки.

##### Почему «у меня проходит»

Локально стенд отвечает за миллисекунды, и `assert balance.text_content() == "1000"` часто
успевает. В CI под нагрузкой ответ идёт дольше — и тест падает «иногда». Это и есть флейк.
В задании 1 ты воспроизведёшь его медленной сетью (раздел 9).

---

#### 3. Полный набор проверок

##### Locator

| Проверка | Что проверяет | Пример на стенде |
|---|---|---|
| `to_be_visible()` / `to_be_hidden()` | видим / не видим (или нет в DOM) | кабинет после входа |
| `to_be_attached()` | есть в DOM (видимость не важна) | |
| `to_be_enabled()` / `to_be_disabled()` | нет / есть `disabled` | кнопка «Пополнить» во время запроса |
| `to_be_editable()` | можно вводить | поле «Цена» |
| `to_be_checked()` / `to_be_checked(checked=False)` | radio/checkbox | «Купить» выбран по умолчанию |
| `to_be_focused()` | в фокусе | |
| `to_be_empty()` | пустой input или элемент без текста | поле «Сумма» после пополнения |
| `to_be_in_viewport()` | в видимой области экрана | |
| `to_have_text(x)` | текст целиком (строка, регулярка или **список**) | статус `FILLED` |
| `to_contain_text(x)` | подстрока | ошибка содержит `price` |
| `to_have_value(x)` / `to_have_values([...])` | значение input / multi-select | пара `ETH-USDT` |
| `to_have_count(n)` | сколько элементов нашёл локатор | строк ордеров 3 |
| `to_have_attribute(name, value)` | атрибут | `type="password"` |
| `to_have_class(x)` / `to_contain_class(x)` | класс целиком / один из классов | ячейка `class="status"` |
| `to_have_css(name, value)` | вычисленный CSS | |
| `to_have_id(x)`, `to_have_role(x)` | id, ARIA-роль | тост — `status` |
| `to_have_accessible_name(x)` | доступное имя | |
| `to_have_js_property(name, value)` | свойство DOM-объекта | `disabled` = True |
| `to_match_aria_snapshot(yaml)` | структура блока | форма входа (U1.2) |

##### Page

| Проверка | Пример |
|---|---|
| `to_have_url(x)` | `expect(page).to_have_url(re.compile(r"/app/$"))` |
| `to_have_title(x)` | `expect(page).to_have_title("Mini Exchange")` |

##### Опции и приёмы

```python
expect(loc).to_have_text("FILLED", timeout=15_000)        # свой таймаут для одной проверки
expect(loc).to_have_text(re.compile(r"^100(\.0+)?$"))     # регулярка
expect(loc).to_have_text("filled", ignore_case=True)
expect(loc).to_have_text("...", use_inner_text=True)      # innerText вместо textContent
expect(loc).not_to_be_visible()                            # отрицание: not_to_...

expect(loc, "ордер не исполнился за 15 с").to_have_text("FILLED", timeout=15_000)  # своё сообщение
expect.set_options(timeout=10_000)                         # таймаут expect для всего прогона
```

`to_have_text` со **списком** проверяет все элементы локатора по порядку одной проверкой:

```python
expect(page.get_by_test_id("order-status")).to_have_text(["NEW", "NEW", "CANCELED"])
```

##### Мягкие проверки — `expect.soft`

Обычная проверка останавливает тест на первой ошибке. Мягкая — запоминает ошибку
и идёт дальше; в конце теста pytest-playwright падает со списком всех ошибок:

```python
expect.soft(balance_row(page, "USDT").get_by_test_id("balance-available")).to_have_text("0")
expect.soft(balance_row(page, "BTC").get_by_test_id("balance-available")).to_have_text("0")
expect.soft(balance_row(page, "ETH").get_by_test_id("balance-available")).to_have_text("0")
# если упали две — в отчёте ExceptionGroup с двумя AssertionError
```

Когда уместно: много **независимых** проверок одного экрана (все балансы, все поля карточки) —
за один прогон видно все расхождения. Когда нет: если следующий шаг зависит от проверки
(«кабинет открылся» → дальше работаем в кабинете) — тут нужна обычная проверка.

---

#### 4. Асинхронный UI нашего стенда

Что происходит во фронтенде (`exchange/web/app.js`) — это нужно знать, чтобы правильно ждать:

| Событие | Что делает UI | Что это значит для теста |
|---|---|---|
| Вход / регистрация | показывает кабинет **сразу**, балансы и ордера грузит **отдельными** запросами | кабинет виден, а таблицы ещё пустые |
| Опрос | раз в **2 с** перезапрашивает ордера и балансы | исполнение ордера (матчинг в фоне раз в 1 с) появится через 1–3 с — `timeout` |
| Пополнение | кнопка `disabled` до ответа; при успехе — тост, сброс формы, потом запрос балансов | тост виден раньше, чем новый баланс в таблице |
| Ордер | так же: `disabled`, тост, потом перезапрос таблиц | |
| Тост | один элемент на всё, исчезает через **2,5 с**, новый текст заменяет старый | проверять сразу после действия; одинаковый текст двух тостов подряд неразличим |
| Ответ 401 | разлогин | |

##### Ловушка 1: «проверка прошла слишком рано»

```python
register(page, email)
expect(page.get_by_test_id("order-row")).to_have_count(0)   # проходит МГНОВЕННО
```

Сразу после входа таблица ещё не загружена — строк 0 **всегда**, даже если бы сервер
вернул ордера. Проверка ничего не доказала. То же с `not_to_...`, `to_be_hidden()`,
`to_have_count(0)`: «ничего нет» верно и до загрузки.

Защита: сначала дождаться **положительного признака**, что данные загрузились,
и только потом проверять отсутствие:

```python
expect(page.get_by_test_id("orders-empty")).to_be_visible()  # таблица загружена и пуста
expect(page.get_by_test_id("order-row")).to_have_count(0)
```

Или дождаться ответа сервера (раздел 5).

##### Ловушка 2: одинаковый тост

```python
deposit(page, "USDT", "100")    # тост «Баланс USDT пополнен»
deposit(page, "USDT", "100")    # проверка тоста проходит СРАЗУ — по старому тосту
```

Второй вызов мог ещё не дойти до сервера, а проверка уже зелёная. Хуже того: форма после
успешного ответа делает `reset()`. Если ответ на **первый** запрос пришёл, когда тест уже ввёл
сумму для второго, — `reset()` её стирает, и второй клик отправляет пустую форму. Так на стенде
три `place_order` подряд создавали два ордера. Варианты:
- перед вторым действием дождаться, что тост исчез: `expect(toast).to_be_hidden()`;
- проверять **бизнес-результат**, а не тост: баланс стал 200;
- ждать ответ сервера на каждый запрос (`expect_response`) — так сделаны хелперы
  `deposit` и `place_order` в `tests/ui/helpers.py`.

##### Ловушка 3: проверка «мигающего» состояния

```python
button.click()
expect(button).to_be_disabled()   # флейк: запрос мог уже завершиться, кнопка снова enabled
```

Короткие промежуточные состояния (спиннер, disabled на 50 мс) проверять ненадёжно — их можно
не застать. Проверяй устойчивое конечное состояние. Если промежуточное состояние — требование,
его тестируют замедлением сети (раздел 9) или подменой ответа (модуль про сеть).

---

#### 5. Ожидание сети: `expect_response` и `expect_request`

Контекстный менеджер: **сначала** начинаем ждать, **потом** делаем действие — иначе ответ
может прийти раньше, чем мы начали слушать.

```python
with page.expect_response("**/balances/deposit") as response_info:
    page.get_by_role("button", name="Пополнить").click()
response = response_info.value

assert response.status == 200
assert response.json() == {"asset": "USDT", "available": "1000", "locked": "0"}
```

Аргумент — glob (`"**/orders"`), регулярка или функция-предикат:

```python
with page.expect_response(
    lambda r: r.url.endswith("/orders") and r.request.method == "POST"
) as info:
    page.get_by_role("button", name="Разместить ордер").click()
order = info.value.json()
order_id = order["id"]     # теперь можно найти строку: [data-testid=order-row][data-id=...]
```

Почему важен предикат: `GET /orders` уходит раз в 2 с от опроса — glob `"**/orders"` может
поймать его вместо твоего `POST`.

Запрос, который отправил браузер:

```python
with page.expect_request("**/orders") as request_info:
    ...click()
request = request_info.value
request.method                 # "POST"
request.post_data_json         # {"symbol": "ETH-USDT", "side": "BUY", "price": "100", ...}
request.headers["authorization"]
```

Что есть у `Response`: `status`, `ok`, `url`, `headers`, `json()`, `text()`, `request`.
У `Request`: `method`, `url`, `headers`, `post_data`, `post_data_json`, `response()`.

Таймаут — как у действий (30 с), меняется `timeout=` в `expect_response(...)`.

##### Когда ждать сеть в UI-тесте

Уместно:
- получить данные, которых нет на экране (id созданного ордера);
- проверить, что UI отправил правильный запрос (поле не потерялось, сумма не округлилась);
- синхронизироваться: «ответ пришёл» — надёжный сигнал, что можно проверять экран;
- отличить баг фронтенда от бэкенда: сервер ответил верно, а UI показал не то.

Неуместно: заменять проверки экрана проверками JSON. UI-тест проверяет то, что видит пользователь.
Ответы API подробно проверяют API-тесты.

Другие события страницы: `expect_request_finished`, `expect_console_message`,
`expect_event("...")`, `expect_popup`, `expect_download` (U3).

---

#### 6. URL и загрузка страницы

```python
page.goto("/")                                       # стенд редиректит на /app/
expect(page).to_have_url(re.compile(r"/app/$"))       # проверка с повтором
page.wait_for_url("**/app/")                          # ожидание (например, после клика по ссылке)
```

`goto` по умолчанию ждёт событие `load`. Состояния загрузки:

| `wait_until` / `wait_for_load_state` | Когда наступает |
|---|---|
| `"commit"` | пришёл ответ на навигацию |
| `"domcontentloaded"` | HTML разобран |
| `"load"` (по умолч.) | загружены картинки, стили, скрипты |
| `"networkidle"` | 500 мс без сетевых запросов |

**`networkidle` не рекомендуют**: на странице с опросом (у нас раз в 2 с), веб-сокетами
или аналитикой сеть не бывает тихой долго — тест виснет или ведёт себя случайно.
И он ничего не говорит о нужных данных. Вместо него — проверка конкретного элемента.

---

#### 7. Произвольное условие: `wait_for_function`

Когда нужно дождаться состояния, которого нет в DOM:

```python
page.wait_for_function("() => localStorage.getItem('token') !== null")
page.wait_for_function("n => document.querySelectorAll('[data-testid=order-row]').length >= n", arg=3)
```

Функция выполняется в браузере многократно, пока не вернёт truthy (таймаут 30 с).
Применять редко — для DOM почти всегда есть подходящий `expect`.

##### `locator.wait_for(state=...)`

```python
page.get_by_test_id("toast").wait_for(state="hidden")   # "attached" | "detached" | "visible" | "hidden"
```

Ждёт состояние элемента без проверки. Нужен в хелперах, где дальше идёт ветвление или действие.
В тесте для проверки — `expect`.

##### Своё ожидание на Python

В JS-версии есть `expect.poll` и `expect(...).to_pass()` для повторения произвольного кода.
**В Python их нет.** Если нужно подождать не-UI условие (например, статус через API),
пишут короткий цикл с дедлайном:

```python
import time

def wait_until(condition, timeout: float = 10, interval: float = 0.5, message: str = ""):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return
        time.sleep(interval)
    raise AssertionError(message or "условие не выполнилось")
```

Здесь `sleep` — это **интервал опроса**, а не «подождать на всякий случай»: цикл заканчивается,
как только условие выполнено.

---

#### 8. Таймауты

| Что | По умолчанию | Как поменять |
|---|---|---|
| `expect` | 5 с | `timeout=` в проверке; `expect.set_options(timeout=...)` |
| действия | 30 с | `page.set_default_timeout()`, `context.set_default_timeout()` |
| навигация | 30 с | `page.set_default_navigation_timeout()` |
| `expect_response`, `wait_for_*` | 30 с | `timeout=` |

Правила:
- увеличивать таймаут **точечно** там, где процесс реально долгий (матчинг, генерация отчёта),
  с комментарием почему;
- не поднимать глобальный таймаут «чтобы не падало» — тесты станут медленными при каждом
  настоящем падении, а флейк никуда не денется;
- `timeout=0` — без ограничения, в тестах не использовать.

---

#### 9. Как воспроизвести флейк: медленная сеть

Флейк «иногда падает в CI» локально не ловится — всё быстрое. Замедли сеть, и гонка видна
каждый раз. В `tests/ui/helpers.py` есть хелпер:

```python
from tests.ui.helpers import slow_network

slow_network(page, 400)       # +400 мс к каждому запросу (только Chromium, через CDP)
```

На стенде с задержкой 400 мс сразу после тоста «Баланс пополнен» `text_content()` баланса
возвращает старое `"0"`, а `expect(...).to_have_text("1000")` дожидается нового значения.

Другие способы: `--slowmo` (замедляет действия, а не сеть — гонки с сетью он **скрывает**),
режим сбоев стенда `EXCHANGE_CHAOS_RATE` (U2.4), задержка через `page.route` (модуль про сеть).

---

#### 10. Антипаттерны ожидания

| Антипаттерн | Почему плохо | Вместо |
|---|---|---|
| `time.sleep(2)`, `page.wait_for_timeout(2000)` | всегда медленно; при задержке больше 2 с всё равно падает | `expect` на результат |
| `assert loc.is_visible()` | проверка в моменте | `expect(loc).to_be_visible()` |
| `if loc.is_visible(): loc.click()` для «вдруг появится» | гонка: элемент появится через 100 мс | детерминированный сценарий; `wait_for` в хелпере |
| `wait_until="networkidle"` | висит на опросе, ничего не доказывает | `expect` на нужный элемент |
| `page.wait_for_selector(...)` | старое API на селекторах | локатор + `expect` / `wait_for` |
| глобально `timeout=60_000` | маскирует проблемы, медленные падения | точечный `timeout=` |
| `try: expect(...) except: pass` | проверка, которая не может упасть | убрать или сделать мягкой осознанно |
| проверка отсутствия сразу после загрузки | проходит до загрузки данных | сначала положительный признак |
| `expect_response("**/orders")` с опросом на странице | ловит чужой GET | предикат с методом |

---

#### Собес: вопросы и ответы

**1. Почему в Playwright проверяют через `expect`, а не `assert`?**
> UI асинхронный: после действия запрос и перерисовка ещё идут. `assert` проверяет один раз
> в моменте и падает, если UI не успел, — это флейк. `expect` — web-first assertion: повторяет
> проверку, каждый раз заново ищет элемент, пока условие не выполнится или не выйдет таймаут
> (по умолчанию 5 секунд). При падении показывает лог попыток и последнее значение.

**2. Какие методы Locator не ждут и когда они всё же нужны?**
> `is_visible`, `is_enabled`, `count`, `text_content`, `inner_text`, `input_value`,
> `get_attribute` — возвращают значение в моменте. Для проверок вместо них `to_be_visible`,
> `to_have_count`, `to_have_text` и т.д. Методы «в моменте» нужны, чтобы взять значение для
> следующих шагов (id, текущий баланс) или для ветвления в хелпере.

**3. Как дождаться ответа сервера? Когда это уместно в UI-тесте?**
> `with page.expect_response(url_or_predicate) as info:` и действие внутри блока — слушать
> начинаем до действия. Потом `info.value.status`, `.json()`. Уместно, чтобы взять данные,
> которых нет на экране (id), проверить, что UI отправил правильный запрос, или
> синхронизироваться перед проверкой экрана. Если на странице есть опрос, фильтрую предикатом
> по методу. Заменять проверки экрана проверками JSON не стоит — это работа API-тестов.

**4. Почему `sleep` / `wait_for_timeout` — антипаттерн? Что вместо?**
> Фиксированная пауза одновременно слишком длинная (тест всегда медленный) и слишком короткая
> (при нагрузке ответ дольше паузы — падение). Она не проверяет условие. Вместо — ожидание
> конкретного результата: `expect` на элемент, `expect_response`, `wait_for_url`,
> в крайнем случае `wait_for_function` или цикл с дедлайном.

**5. Почему не рекомендуют `networkidle`?**
> Он ждёт 500 мс без сетевых запросов. На страницах с опросом, веб-сокетами, аналитикой сеть
> не затихает — тест висит до таймаута или проходит случайно. И тишина в сети не значит, что
> на экране нужные данные. Надёжнее ждать конкретный элемент или ответ.

**6. Проверка прошла, но ничего не доказала — как такое бывает?**
> Проверки отсутствия — `to_have_count(0)`, `to_be_hidden`, `not_to_have_text` — верны и до
> загрузки данных, поэтому проходят мгновенно. То же со старым тостом с тем же текстом.
> Защита — сначала дождаться положительного признака загрузки (текст «Ордеров пока нет»,
> ответ сервера) или проверять бизнес-результат, а не промежуточный сигнал.

**7. Что такое soft assertions?**
> `expect.soft(...)` не останавливает тест на ошибке: ошибки копятся, тест падает в конце со
> списком всех. Удобно для набора независимых проверок одного экрана. Не подходит, когда
> следующий шаг зависит от проверки — тогда обычный `expect`.

**8. Какие таймауты есть в Playwright и как их настраивать?**
> `expect` — 5 с, действия и навигация — 30 с, ожидания событий — 30 с. Меняются на уровне
> проверки (`timeout=`), страницы или context (`set_default_timeout`), для `expect` глобально —
> `expect.set_options`. На тест целиком — `pytest-timeout`. Увеличиваю точечно там, где процесс
> реально долгий, а не глобально.

**9. Как воспроизвести флейк, который бывает только в CI?**
> Сделать окружение медленнее: эмуляция задержки сети (в Chromium через CDP), нагрузка на
> машину, режим сбоев стенда, параллельный запуск. Повторить тест много раз. `--slowmo` для
> этого плохо подходит: он замедляет действия теста, и гонки с сетью исчезают. Потом смотрю
> trace: где тест прочитал значение раньше, чем оно обновилось.

### Задания — `tests/ui/test_u2_01_waiting_async_ui.py`

```text
U2. Урок 1 — web-first assertions и асинхронный UI.

Теория: practice/u2_01_waiting_async_ui.md
Запуск:
    uv run pytest tests/ui/test_u2_01_waiting_async_ui.py -v

Можно использовать: фикстуры logged_in_page, create_user, user_email (tests/ui/conftest.py),
хелперы register, deposit, place_order, balance_row, amount, slow_network (tests/ui/helpers.py).
Правила: никаких sleep / wait_for_timeout; проверки — только expect (кроме задачи 1а).

Задача 1. Флейк своими руками.
    а) Новый пользователь, slow_network(page, 400), пополни USDT 1000 через deposit().
       Сразу после этого: assert <доступно USDT>.text_content() == "1000".
       Запусти — тест должен упасть. Убери slow_network — пройдёт. Так выглядит флейк.
    б) Отдельный тест: то же самое, но правильной проверкой. Должен проходить с задержкой.
    В «Ответах»: почему без задержки assert проходит и почему это не значит, что тест верный.

Задача 2. Каталог проверок (только смотрим на экран, без проверки бизнес-логики).
    - page.goto("/") → URL заканчивается на /app/ (to_have_url + регулярка), заголовок "Mini Exchange";
    - после входа на форме ордера: пара ETH-USDT (to_have_value), «Купить» выбран, «Продать» нет,
      поле «Цена» редактируемое и пустое, кнопка «Разместить ордер» enabled;
    - заполни цену "123" — to_have_value;
    - пополни USDT 10: после успеха поле «Сумма» пустое (форма сбросилась), у тоста роль status;
    - размести BUY цена 1 кол-во 1: у ячейки статуса класс status (to_have_class),
      строка видна в области экрана (to_be_in_viewport).

Задача 3. Проверка, которая ничего не доказала.
    а) Пользователь с одним ордером (размести BUY цена 1 кол-во 1, дождись строки).
       slow_network(page, 800), page.reload(), дождись кабинета.
       expect(<строки ордеров>).to_have_count(0) — запусти. Тест ЗЕЛЁНЫЙ, хотя ордер есть.
       Затем перепиши его так, чтобы проверка отражала правду (строк 1),
       и объясни в «Ответах», почему наивная версия была зелёной.
    б) Тест «у нового пользователя нет ордеров», который нельзя обмануть: со slow_network(page, 800)
       он должен проверять отсутствие ордеров ПОСЛЕ того, как таблица загрузилась.

Задача 4. Одинаковые тосты.
    Хелпер deposit() из helpers.py уже ждёт ответ сервера — здесь пишешь свою наивную версию.
    а) Функция naive_deposit(page, asset, value): заполнить форму, нажать, проверить ТОЛЬКО тост.
       Новый пользователь, slow_network(page, 400), naive_deposit USDT 100 три раза подряд,
       потом проверь, что доступно USDT 300. Запусти несколько раз — что видишь?
       (Подсказка: посмотри в app.js, что делает форма после успешного ответа.)
    б) Функция deposit_and_wait(page, asset, value) -> dict: ждёт ответ POST /balances/deposit
       и возвращает его JSON. Тот же сценарий с ней — стабильно 300.
    В «Ответах»: что доказала проверка тоста во втором и третьем вызовах naive_deposit,
    откуда взялась поломка и почему с двумя пополнениями её не видно.

Задача 5. expect_response.
    Пополни ETH 2.5 через UI, поймай ответ POST /balances/deposit.
    Проверь: статус 200, JSON целиком == {"asset": "ETH", "available": "2.5", "locked": "0"},
    и в таблице доступно ETH то же значение, что в ответе.

Задача 6. expect_request.
    Пополни USDT 1000, размести BUY ETH-USDT цена "100.50" кол-во "0.5".
    Поймай запрос: метод POST, post_data_json содержит symbol, side, price, quantity ровно
    такими, как ввёл пользователь (строки!), заголовок authorization начинается с "Bearer ".
    Подумай, почему glob "**/orders" без предиката здесь опасен.

Задача 7. id из ответа.
    Пополни USDT 1000, размести три BUY-ордера: цены 10, 20, 30 (кол-во 1).
    id ордера с ценой 20 возьми из ответа POST /orders.
    Найди его строку по data-id (не по цене!), отмени кнопкой в строке, поймай ответ DELETE:
    статус 200, в JSON status "CANCELED". В UI: у этой строки CANCELED, у остальных двух NEW.

Задача 8. expect.soft.
    У нового пользователя все три актива: доступно 0 и заблокировано 0 — шесть мягких проверок.
    Временно сломай две (ожидай "1") — посмотри, как выглядит отчёт, потом верни.
    В «Ответах»: чем отчёт отличается от обычного expect и когда soft не подходит.

Задача 9. Состояние вне DOM.
    Зарегистрируйся — page.wait_for_function дождись, что token в localStorage не null.
    Нажми «Выйти» — дождись, что token стал null, и проверь, что видна форма входа.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Почему в Playwright проверяют через expect, а не assert?
    2. Какие методы Locator не ждут и когда они всё же нужны?
    3. Как дождаться ответа сервера? Когда это уместно в UI-тесте?
    4. Почему sleep / wait_for_timeout — антипаттерн? Что вместо?
    5. Почему не рекомендуют networkidle?
    6. Проверка прошла, но ничего не доказала — как такое бывает?
    7. Что такое soft assertions?
    8. Какие таймауты есть в Playwright и как их настраивать?
    9. Как воспроизвести флейк, который бывает только в CI?
```

<a id="u2-2"></a>

## U2.2 Цепочки, фильтры и strict mode

*Теория: `practice/u2_02_chains_filters_strict.md`*

Задания: `tests/ui/test_u2_02_chains_filters_strict.py`.

Основы локаторов (`get_by_*`, `filter`, `first/nth`, `and_/or_`, строка таблицы → кнопка)
были в U1.2. Здесь — то, на чём реально ломаются тесты: strict mode и как его разрешать,
тонкости `filter`, ловушки `nth` в цепочках, таблицы по названию колонки, порядок строк,
списки, которые перерисовываются, и отладка локаторов.

---

#### 1. Strict mode

Правило: **если операция работает с одним элементом, а локатор нашёл несколько — ошибка**.
Playwright не выбирает «первый попавшийся».

```python
page.get_by_role("button", name="Отменить").click()   # три открытых ордера
```

```
Locator.click: Error: strict mode violation: get_by_role("button", name="Отменить") resolved to 3 elements:
    1) <button ... data-id="d308...">Отменить</button> aka get_by_role("row", name="ETH-USDT BUY 20 1 0 NEW").get_by_test_id("cancel-order")
    2) <button ... data-id="86ba...">Отменить</button> aka get_by_role("row", name="ETH-USDT BUY 100 1 0 NEW").get_by_test_id("cancel-order")
    3) ...
```

Зачем так строго: в Selenium `find_element` молча берёт первый элемент. Тест кликает «Отменить»
не в той строке, проходит дальше — и падает через три шага с непонятной ошибкой, или, хуже,
не падает вообще. Strict mode превращает неоднозначность в ошибку **в момент поиска**.

Читай сообщение: Playwright перечисляет все найденные элементы и для каждого подсказывает
уникальный локатор (`aka ...`). Это готовые варианты, как сузить поиск.

##### Какие операции строгие

| Строгие (нужен ровно 1 элемент) | Не строгие (работают со списком) |
|---|---|
| все действия: `click`, `fill`, `check`, `select_option`, `hover`, `press`… | `count()`, `all()`, `all_text_contents()`, `all_inner_texts()` |
| `text_content()`, `inner_text()`, `input_value()`, `get_attribute()`, `is_visible()`… | `to_have_count(n)` |
| `expect`: `to_be_visible`, `to_have_text("строка")`, `to_have_value`, `to_be_checked`… | `to_have_text([...])`, `to_contain_text([...])` — проверка **списком** |
| | `first`, `last`, `nth(i)` — сами выбирают один элемент |

У `expect` нарушение strict mode выглядит как обычное падение проверки, а причина видна
в логе вызова: `locator resolved to 3 elements`.

##### Примеры неоднозначности на стенде

| Локатор | Сколько находит | Почему |
|---|---|---|
| `page.get_by_role("combobox")` | 3 | «Актив» в пополнении, «Пара» в ордере, фильтр «Статус» |
| `page.get_by_text("NEW")` | N + 1 | ячейки статуса **и** `<option>NEW</option>` в фильтре |
| `page.get_by_role("button", name="Отменить")` | по числу открытых ордеров | кнопка в каждой строке |
| `page.get_by_label("Цена")` | 1 | одно поле, но держи в уме: в форме фильтра могла бы быть вторая «Цена» |

---

#### 2. Как разрешать: от лучшего к худшему

1. **Точнее описать элемент** — роль + имя, `exact=True`:
   ```python
   page.get_by_role("combobox", name="Пара")
   page.get_by_text("NEW", exact=True)          # точное совпадение, но option всё равно подходит
   ```
2. **Сузить область** — искать внутри контейнера:
   ```python
   page.locator("#order-form").get_by_role("combobox")
   page.get_by_test_id("orders-table").get_by_text("NEW", exact=True)
   ```
3. **Отфильтровать по содержимому** — строка с нужной ценой:
   ```python
   rows.filter(has=page.get_by_role("cell", name="20", exact=True)).get_by_role("button", name="Отменить")
   ```
4. **Уникальный атрибут** — `data-id`, test-id:
   ```python
   page.locator(f'[data-testid="order-row"][data-id="{order_id}"]')
   ```
5. **Позиция** — `first`, `last`, `nth` — только когда позиция и есть требование (раздел 3).

##### Почему `.first` — плохая «починка»

```python
page.get_by_role("button", name="Отменить").first.click()   # ошибка ушла
```

Ошибка ушла, но тест теперь отменяет **какой-то** ордер — тот, что оказался сверху. Сегодня это
нужный, завтра сортировку поменяли — и тест отменяет чужой. Хуже: `.first` прячет баги.
Если из-за двойного клика создалось **два** одинаковых ордера, проверка
`rows.filter(has_text="BUY").first` зелёная — дубль никто не заметит.
Строгий локатор в этой ситуации упал бы и показал проблему.

`.first` / `nth` оправданы, когда:
- порядок — это требование: «новый ордер появляется сверху», «первый в списке — самый дешёвый»;
- элементы действительно взаимозаменяемы: «отменить все открытые по одному» (раздел 6);
- в справочнике, где элементы одинаковые по смыслу (первая из похожих карточек для smoke).

---

#### 3. Тонкости `filter`

##### `has_text` — подстрока, без регистра

```python
rows.filter(has_text="10")
```

- ищет **подстроку** в тексте элемента **вместе с потомками**;
- без учёта регистра, пробелы по краям обрезаются, внутри — схлопываются;
- регулярка `re.compile(...)` — как написал, с учётом регистра (флаг `re.I`, если нужно).

Ловушка на стенде: ордера с ценами 10 и 100. `filter(has_text="10")` находит **обе** строки.
А ещё строку, где количество `10` или исполнено `0.10`. Подстрока по всей строке почти
никогда не означает «цена равна 10».

Регулярка по всей строке тоже не спасает: `text_content()` строки склеивает ячейки так, как они
стоят в HTML. У стенда первые четыре ячейки идут подряд **без пробелов**:
`"ETH-USDTBUY1010"` (цена 10, кол-во 10) — по тексту не понять, где кончается цена.

Надёжные варианты:

```python
# ячейка с ТОЧНЫМ текстом внутри строки
rows.filter(has=page.get_by_role("cell", name="10", exact=True))

# строка по доступному имени: ячейки через пробел — так подсказывает сам Playwright
page.get_by_role("row", name="ETH-USDT BUY 10 1 0 NEW")

# конкретная колонка — раздел 4
```

Но и `cell name="10" exact` найдёт строку, где **количество** равно 10. Если в строке могут
совпасть разные колонки — ищи по колонке, и **тоже точно**:

```python
price_cell = page.locator("td:nth-child(3)")                     # колонка «Цена» (раздел 4)
rows.filter(has=price_cell.filter(has_text="10"))                # 2 строки: 10 и 100 — снова подстрока
rows.filter(has=price_cell.get_by_text("10", exact=True))        # 1 строка
rows.filter(has=price_cell.filter(has_text=re.compile(r"^10$"))) # 1 строка
```

Проверено на стенде: ордера 10, 100, 1 с количеством 10 у всех — `has_text="10"` по строке даёт 3,
`cell exact` даёт 3, колонка с подстрокой — 2, колонка с точным совпадением — 1.

##### `has` — вложенный элемент, относительный поиск

```python
rows.filter(has=page.get_by_role("button", name="Отменить"))      # открытые ордера
rows.filter(has_not=page.get_by_role("button", name="Отменить"))  # закрытые
```

Внутренний локатор ищется **внутри каждого** элемента внешнего, хоть и записан от `page`.
Ограничение: внутренний локатор не должен выходить за пределы (нельзя `frame_locator`).

##### Комбинации

```python
rows.filter(has_text="BUY").filter(has=cancel)          # открытые BUY — фильтры последовательно
page.get_by_role("button").filter(visible=True)          # только видимые
page.get_by_role("button", name="Отменить").and_(page.locator('[data-id="..."]'))
```

##### `get_by_text`: `exact`

| | `exact=False` (по умолч.) | `exact=True` |
|---|---|---|
| совпадение | подстрока | весь текст элемента |
| регистр | не важен | важен |
| пробелы | обрезаются, схлопываются | обрезаются, схлопываются |

---

#### 4. Таблицы: колонка по заголовку и ловушка `nth`

##### `nth` в цепочке — от всего списка

```python
rows = page.get_by_test_id("order-row")
rows.locator("td").nth(2)        # НЕ «третья ячейка каждой строки»
```

`rows.locator("td")` — это **все** ячейки всех строк подряд. `nth(2)` — третья ячейка
**во всей таблице**, одна штука. Цепочка выполняется слева направо над списком, а `nth` берёт
один элемент из результата.

Третья ячейка в каждой строке:

```python
rows.locator("td:nth-child(3)")                  # CSS: третья по счёту ячейка у своего родителя
expect(rows.locator("td:nth-child(3)")).to_have_text(["30", "20", "10"])

rows.nth(0).locator("td").nth(2)                 # одна ячейка конкретной строки
```

##### Колонка по названию заголовка

Индекс колонки зашит в тест — сломается, если добавят колонку. Лучше вычислить:

```python
def column(page: Page, table: Locator, header: str) -> Locator:
    headers = table.locator("thead th").all_text_contents()   # ['Пара', 'Сторона', 'Цена', ...]
    index = headers.index(header) + 1                         # nth-child считает с 1
    return table.locator(f"tbody td:nth-child({index})")

prices = column(page, page.get_by_test_id("orders-table"), "Цена")
expect(prices).to_have_text(["30", "20", "10"])
```

Ячейка в найденной строке: `row.locator(f"td:nth-child({index})")`.

##### Порядок строк

У стенда ордера идут **новые сверху** (`ORDER BY created_at DESC`). Значит, проверка списком
`to_have_text([...])` должна учитывать порядок создания. Если порядок не гарантирован
требованием — сортируй в тесте:

```python
expect(prices).to_have_count(3)                       # сначала дождаться, что все на месте
values = sorted(Decimal(p) for p in prices.all_text_contents())
assert values == [Decimal("10"), Decimal("20"), Decimal("30")]
```

Сортировать числа как строки нельзя: `"100" < "20"`.

---

#### 5. Locator и ElementHandle: почему нет stale element

| | Locator | ElementHandle |
|---|---|---|
| Что это | **описание**, как найти элемент | ссылка на **конкретный** DOM-узел |
| Когда ищет | при каждом действии/проверке заново | один раз, при получении |
| После перерисовки | находит новый узел | узел удалён → `Element is not attached to the DOM` |
| Как получить | `page.locator(...)`, `get_by_*` | `page.query_selector(...)`, `locator.element_handle()` |

Наш фронтенд раз в 2 с **заменяет** содержимое таблиц (`tbody.innerHTML = ...`) — все старые
DOM-узлы строк удаляются и создаются новые. ElementHandle на строку протухнет через 2 с,
Locator — нет. Это то, что в Selenium называется `StaleElementReferenceException`; в Playwright
его нет, пока работаешь через локаторы. ElementHandle в тестах не используют.

---

#### 6. Списки, которые меняются

##### `all()` — снимок, а не живой список

```python
for button in page.get_by_role("button", name="Отменить").all():   # ПЛОХО
    button.click()
```

`all()` возвращает список `nth(0)`, `nth(1)`, `nth(2)`… по количеству элементов **в момент
вызова** и **не ждёт** их появления. После первой отмены кнопок стало меньше и таблица
перерисовалась: `nth(2)` указывает на другую кнопку или на ничто — тест виснет до таймаута
или отменяет не то. В документации прямо сказано: на меняющемся списке `all()` даёт
непредсказуемый результат.

Правильно — каждый раз брать актуальный первый элемент и ждать, что список изменился:

```python
cancel = page.get_by_role("button", name="Отменить")
expect(cancel).to_have_count(3)
for left in (2, 1, 0):
    cancel.first.click()
    expect(cancel).to_have_count(left)      # дождались перерисовки, прежде чем кликать дальше
```

Здесь `.first` уместен: все кнопки взаимозаменяемы, нужно отменить все.

##### Перебор только для чтения

`all()` / `all_text_contents()` безопасны, когда список уже устоялся:

```python
expect(rows).to_have_count(3)                    # 1. дождаться нужного количества
statuses = rows.get_by_test_id("order-status").all_text_contents()   # 2. прочитать
```

Но если можно проверить списком через `expect(...).to_have_text([...])` — так лучше:
и ждёт, и проверяет.

---

#### 7. Отладка локаторов

```bash
PWDEBUG=1 uv run pytest tests/ui/test_u2_02_chains_filters_strict.py -k cancel
```

- **Inspector**: шаги теста по одному, подсветка элемента, который нашёл локатор.
  Кнопка **Pick locator** — навести на элемент, Playwright предложит лучший локатор.
- `page.pause()` в тесте — остановиться в этом месте и открыть Inspector (`--headed`).
- `locator.highlight()` — подсветить в браузере то, что нашёл локатор.
- В отладчике: `loc.count()`, `loc.all_text_contents()`, `print(loc)` — покажет сам селектор.
- Сообщение strict mode — список найденных элементов с подсказками `aka`.
- Trace Viewer (`--tracing on`) — после прогона: DOM на каждом шаге, что нашёл каждый локатор.
  Подробно в модуле про отладку.

---

#### 8. Частые ошибки

| Ошибка | Чем плохо | Как правильно |
|---|---|---|
| `.first` после strict mode violation | прячет дубли, кликает не туда | сузить локатор |
| `filter(has_text="10")` для «цена 10» | подстрока: 100, 0.10, количество 10 | ячейка по колонке или `exact` |
| `rows.locator("td").nth(2)` для колонки | одна ячейка на всю таблицу | `td:nth-child(3)` |
| индекс колонки числом в тесте | ломается при новой колонке | индекс из заголовков |
| `for b in loc.all(): b.click()` на меняющемся списке | индексы съезжают | `first` + ожидание `to_have_count` |
| `query_selector` / `element_handle` | протухает после перерисовки | локаторы |
| сортировка чисел-строк | `"100" < "20"` | `Decimal` |
| `to_have_text([...])` без мысли о порядке | падает при другом порядке | знать порядок или сортировать |
| поиск по тексту, который меняется (`NEW` → `CANCELED`) | строка «пропадает» | неизменный признак: id, цена |

---

#### Собес: вопросы и ответы

**1. Что такое strict mode и зачем он нужен?**
> Если операция ожидает один элемент — действие, чтение текста, проверка видимости, —
> а локатор нашёл несколько, Playwright падает с ошибкой strict mode violation, а не берёт первый.
> Так неоднозначный локатор обнаруживается сразу, а не через три шага, когда тест кликнул не в той
> строке. В сообщении перечислены все найденные элементы с подсказками уникальных локаторов.

**2. Какие операции строгие, какие нет?**
> Строгие — все действия, чтение одного значения (`text_content`, `input_value`) и проверки одного
> элемента (`to_be_visible`, `to_have_text` со строкой). Не строгие — `count`, `all`,
> `all_text_contents`, `to_have_count` и `to_have_text` со списком. `first`, `last`, `nth`
> сами выбирают один элемент.

**3. Локатор нашёл несколько элементов — что делаешь?**
> Уточняю описание: роль с именем, `exact=True`. Сужаю область — ищу внутри формы, таблицы, строки.
> Фильтрую по содержимому — `filter(has=...)` с точной ячейкой. Использую уникальный атрибут —
> test-id, data-id. Позицию `first` / `nth` беру, только если порядок — требование.

**4. Почему `.first` / `nth` — плохая починка? Когда допустимо?**
> Ошибка исчезает, но тест начинает действовать на «какой-то» элемент: при смене сортировки
> кликнет не туда, а дубликаты элементов — например, двойной ордер — станут невидимы.
> Допустимо, когда порядок и есть требование («новый сверху») или элементы взаимозаменяемы
> («отменить все по одному»).

**5. Как работает `filter(has_text=...)` и какие ловушки?**
> Ищет подстроку в тексте элемента вместе с потомками, без учёта регистра, пробелы нормализуются.
> Поэтому `"10"` найдёт и 100, и 0.10, и количество 10. Регулярка по строке тоже неудобна:
> текст строки — склейка ячеек без разделителей. Надёжно — фильтр по вложенной ячейке
> с точным текстом или по конкретной колонке, либо `get_by_role("row", name=...)`.

**6. Как найти ячейку по названию колонки?**
> Прочитать заголовки `thead th` через `all_text_contents`, найти индекс нужного,
> и взять ячейку `td:nth-child(index+1)` внутри строки. Не хардкодить индекс: добавят колонку —
> тест сломается. И помнить, что `rows.locator("td").nth(2)` — одна ячейка на всю таблицу,
> а не колонка.

**7. Чем Locator отличается от ElementHandle? Есть ли в Playwright stale element?**
> Locator — описание поиска, он находит элемент заново при каждом действии. ElementHandle —
> ссылка на конкретный DOM-узел; если страница перерисовала элемент, ссылка протухает.
> Пока работаешь через локаторы, stale element нет — поэтому ElementHandle в тестах не используют.

**8. Как работать со списком, который перерисовывается?**
> Не перебирать `all()` с действиями: это снимок индексов, после изменения списка они съезжают.
> Для действий — брать актуальный `first` и ждать `to_have_count` после каждого шага.
> Для чтения — сначала дождаться устойчивого состояния (`to_have_count`), а лучше проверить
> списком через `to_have_text([...])`, который сам ждёт.

**9. Как отлаживаешь локатор?**
> `PWDEBUG=1` или `page.pause()` — Inspector: пошагово, подсветка, Pick locator.
> `locator.highlight()`, `count()` и `all_text_contents()` в отладчике. Читаю сообщение strict mode —
> там все найденные элементы. После прогона — Trace Viewer: что нашёл каждый локатор на каждом шаге.

### Задания — `tests/ui/test_u2_02_chains_filters_strict.py`

```text
U2. Урок 2 — цепочки, фильтры и strict mode.

Теория: practice/u2_02_chains_filters_strict.md
Запуск:
    uv run pytest tests/ui/test_u2_02_chains_filters_strict.py -v

Можно использовать: фикстуры logged_in_page, create_user (tests/ui/conftest.py),
хелперы deposit, place_order (возвращает JSON ордера), balance_row, amount (tests/ui/helpers.py).
Правила: XPath нельзя; .first / nth — только там, где задача это разрешает, с комментарием почему.

Задача 1. Strict mode своими глазами.
    Пополни USDT 1000, размести два BUY-ордера (цены 1 и 2).
    Для каждого локатора ниже: pytest.raises(Error, match="strict mode violation") вокруг действия
    (Error из playwright.sync_api), а затем — однозначный вариант, который работает:
        - page.get_by_role("combobox") → select_option("BTC") в форме пополнения;
        - page.get_by_text("NEW") → text_content(); объясни, откуда лишний элемент;
        - page.get_by_role("button", name="Отменить") → click(); однозначно отмени ордер с ценой 2.
    Чтобы не ждать 30 с при ошибке, передавай timeout=2000 в действие.

Задача 2. Ловушка подстроки.
    Пополни USDT 2000. Размести BUY по ценам 10, 100 и 1 с количеством 10 (кол-во у всех 10).
    а) Сколько строк находят: rows.filter(has_text="10") и
       rows.filter(has=page.get_by_role("cell", name="10", exact=True))? to_have_count; объясни.
    б) Найди строку «цена 10» двумя надёжными способами:
       через ячейку колонки «Цена» с точным совпадением и через get_by_role("row", name=...).
       Каждый способ — to_have_count(1).
    в) Отмени именно ордер с ценой 10. Проверь: он CANCELED, ордера 100 и 1 — NEW.

Задача 3. Колонка по заголовку.
    Напиши функцию column(table, header) -> Locator: индекс из заголовков таблицы, ячейки tbody.
    Размести BUY 10, 20, 30 (кол-во 1, 2, 3).
    Проверь списком: колонка «Цена» == ["30", "20", "10"] (новые сверху), «Кол-во» == ["3", "2", "1"],
    «Статус» — все NEW.
    Отдельно: expect(rows.locator("td").nth(2)).to_have_count(?) — сколько? Объясни в «Ответах».

Задача 4. Сортировка чисел.
    Размести BUY 9, 100, 25 (кол-во 1). Проверь, что если отсортировать цены как числа,
    получится [9, 25, 100]. Потом покажи, что сортировка строк дала бы другой порядок (assert !=).
    Не забудь дождаться всех строк, прежде чем читать значения.

Задача 5. Отменить всё в перерисовывающейся таблице.
    Размести 4 BUY-ордера (цены 1, 2, 3, 4).
    а) Сначала попробуй наивно: for b in cancel_buttons.all(): b.click(timeout=3000).
       Запусти 2–3 раза, посмотри результат. Оставь этот вариант в отдельном тесте
       с @pytest.mark.skip(reason="демонстрация: all() на меняющемся списке") и объясни в «Ответах».
    б) Надёжный вариант: отменяй по одному с ожиданием, пока кнопок станет меньше.
       В конце: все 4 статуса CANCELED (списком), кнопок «Отменить» — 0.

Задача 6. has / has_not.
    Размести BUY 1, BUY 2 и SELL-ордер (пополни ETH 1, SELL ETH-USDT цена 99999 кол-во 1).
    Отмени BUY 2.
    Проверь через filter(has=...) / filter(has_not=...) с кнопкой «Отменить»:
        - открытых строк 2, закрытых 1, и у закрытой статус CANCELED;
        - открытых BUY ровно 1 (два фильтра подряд);
        - у открытого SELL цена 99999 (по колонке из задачи 3).

Задача 7. Locator vs ElementHandle.
    Размести ордер. Возьми handle = page.get_by_test_id("order-row").element_handle()
    и локатор row = page.get_by_test_id("order-row").
    Дождись перерисовки таблицы (опрос раз в 2 с): page.wait_for_function("el => !el.isConnected",
    arg=handle) — функция выполняется в браузере, пока узел не удалят из DOM.
    Проверь: handle.evaluate("el => el.isConnected") is False, а expect(row).to_be_visible() проходит.
    Попробуй handle.click() — какая ошибка? Запиши в «Ответах».

Задача 8. Inspector (руками, без автотеста).
    PWDEBUG=1 uv run pytest tests/ui/test_u2_02_chains_filters_strict.py -k <любой тест>
    Через Pick locator выбери ячейку «Заблокировано» строки USDT и кнопку «Отменить» в любой строке.
    Запиши в «Ответах», что предложил Playwright, и сравни с тем, как написал бы сам.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое strict mode и зачем он нужен?
    2. Какие операции строгие, какие нет?
    3. Локатор нашёл несколько элементов — что делаешь?
    4. Почему .first / nth — плохая починка? Когда допустимо?
    5. Как работает filter(has_text=...) и какие ловушки?
    6. Как найти ячейку по названию колонки?
    7. Чем Locator отличается от ElementHandle? Есть ли в Playwright stale element?
    8. Как работать со списком, который перерисовывается?
    9. Как отлаживаешь локатор?
```

<a id="u2-3"></a>

## U2.3 Codegen и Inspector

*Теория: `practice/u2_03_codegen_inspector.md`*

Задания: `tests/ui/test_u2_03_codegen_inspector.py`.

План: как записать сценарий codegen'ом и какие опции нужны на нашем стенде; что он генерирует
и почему это ещё не тест; как переписать запись в нормальный тест (чек-лист); Inspector —
пошаговый прогон, Pick locator, запись с середины теста через `page.pause()`; лог `DEBUG=pw:api`.

Trace Viewer, скриншоты и видео на падении — в модуле U7 (отладка и отчёты).

---

#### 1. Что такое codegen и зачем он нужен

`playwright codegen` открывает браузер и окно Inspector. Ты кликаешь по сайту — Playwright пишет
код. Для каждого элемента он сам подбирает локатор по тем же правилам, что и в подсказках
strict mode.

Для чего он реально полезен:
- **быстро подобрать локаторы** на незнакомой странице — особенно где нет ролей и test-id;
- **черновик сценария** — последовательность шагов, которую потом переписываешь;
- **разобраться, как работает страница** — что за элементы, что происходит после клика;
- на собесе и в работе — показать, что знаешь инструмент и **его ограничения**.

Для чего не нужен: генерировать тесты «как есть» в репозиторий. Запись — это черновик (раздел 4).

---

#### 2. Запуск на нашем стенде

```bash
uv run playwright codegen --target python-pytest --channel chrome http://localhost:8080/app/
```

- `--target python-pytest` — код в виде pytest-теста с фикстурой `page`
  (по умолчанию `python` — скрипт с `sync_playwright()` и ручным запуском браузера);
- `--channel chrome` — **обязательно у нас**: на macOS 12 свежий Chromium Playwright не ставится,
  как и в `addopts` проекта.

Полезные опции:

| Опция | Зачем |
|---|---|
| `-o файл.py` | сохранить код в файл при закрытии |
| `--viewport-size "1440,900"` | размер окна как в тестах (`browser_context_args`) |
| `--lang ru-RU`, `--timezone Europe/Moscow` | локаль и часовой пояс |
| `--device "iPhone 13"` | мобильная эмуляция |
| `--color-scheme dark` | тёмная тема |
| `--save-storage .auth/state.json` | при закрытии сохранить cookies + localStorage |
| `--load-storage .auth/state.json` | стартовать уже залогиненным |
| `--test-id-attribute data-qa` | какой атрибут считать test-id (по умолчанию `data-testid`) |
| `--save-har file.har` | записать весь сетевой трафик (U3) |
| `--target python-async` / `python` | другой вид кода |

`.auth/` у нас в `.gitignore`: в state лежит живой JWT, коммитить его нельзя.

##### Панель записи

В браузере сверху панель:

| Кнопка | Что делает |
|---|---|
| ⏺ Record | вкл/выкл запись действий |
| Pick locator | навести на элемент — показать лучший локатор, без записи действия |
| Assert visibility | клик по элементу → `expect(...).to_be_visible()` |
| Assert text | → `expect(...).to_contain_text(...)` (текст можно поправить) |
| Assert value | для input/select → `to_have_value(...)` |
| Assert snapshot | → `to_match_aria_snapshot(...)` для блока |

---

#### 3. Как codegen выбирает локатор

Приоритет примерно такой:

1. **test-id** (`data-testid` или то, что указано в `--test-id-attribute`);
2. роль + доступное имя — `get_by_role("button", name="Войти")`;
3. label, placeholder, alt, title;
4. текст — `get_by_text(...)`;
5. CSS, если ничего уникального нет; при неоднозначности — добавляет `.nth(i)` или цепочку.

Он проверяет, что локатор **уникален в момент записи**. Не проверяет, что он останется
уникальным: при двух открытых ордерах «Отменить» получит `.first` / `.nth(1)`, при одном —
просто `get_by_role("button", name="Отменить")`, который завтра упадёт на strict mode.

На нашем стенде у элементов есть `data-testid`, поэтому codegen почти везде предложит
`get_by_test_id(...)`. Это **отличается** от приоритета нашего курса (роль → label → test-id):
роль заодно проверяет доступность и то, что видит пользователь. Хочешь увидеть, что codegen
выбрал бы без test-id, — запусти с `--test-id-attribute` несуществующим атрибутом (задача 4).

---

#### 4. Что генерирует codegen — и что с этим не так

Примерно так выглядит запись «регистрация → пополнение → ордер → отмена»:

```python
import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("http://localhost:8080/app/")
    page.get_by_test_id("email-input").click()
    page.get_by_test_id("email-input").fill("test1@test.com")
    page.get_by_test_id("email-input").press("Tab")
    page.get_by_test_id("password-input").fill("password123")
    page.get_by_test_id("register-button").click()
    page.get_by_test_id("deposit-amount").click()
    page.get_by_test_id("deposit-amount").fill("1000")
    page.get_by_test_id("deposit-button").click()
    page.get_by_test_id("order-price").click()
    page.get_by_test_id("order-price").fill("100")
    page.get_by_test_id("order-quantity").click()
    page.get_by_test_id("order-quantity").fill("1")
    page.get_by_test_id("place-order-button").click()
    page.get_by_test_id("cancel-order").click()
    expect(page.get_by_test_id("order-status")).to_contain_text("CANCELED")
```

Твой будет похож, но не идентичен — зависит от того, куда кликал.

##### Чек-лист переписывания

| В записи | Проблема | Как в нормальном тесте |
|---|---|---|
| `goto("http://localhost:8080/app/")` | адрес зашит — не переключить окружение | `goto("/app/")` + `base_url` |
| `fill("test1@test.com")` | второй прогон: «email уже занят» | уникальные данные: `user_email`, `create_user` |
| `.click()` перед `.fill()`, `press("Tab")` | лишние шаги — запись твоих движений, а не сценарий | только `fill` |
| регистрация в каждом тесте вручную | дублирование | фикстура `logged_in_page`, хелперы |
| нет проверок между шагами | «кликнули» ≠ «сработало»: пополнение могло не пройти, а тест идёт дальше | после значимых шагов — проверка результата или хелпер, который ждёт ответ |
| `get_by_test_id("cancel-order").click()` | уникален только пока ордер один | строка по признаку → кнопка внутри |
| `to_contain_text("CANCELED")` для статуса | подстрока; и только одна проверка в конце | `to_have_text` + бизнес-результат: баланс разблокирован |
| `.nth(1)` / `.first` | позиция в момент записи | `filter` по содержимому |
| имя `test_example`, один длинный тест | непонятно, что проверяет | имя = проверяемое поведение; один тест — одна цель |
| `import re` без использования | шум | убрать |

Главное, чего codegen **не может**: понять, что ты проверяешь. Он записывает действия, а тест —
это **проверка ожидаемого результата**. Проверки, данные, изоляция и структура — твоя работа.

---

#### 5. Inspector: пошаговый прогон

```bash
PWDEBUG=1 uv run pytest tests/ui/test_u2_03_codegen_inspector.py -k deposit
```

Что делает `PWDEBUG=1`:
- запускает браузер **headed**;
- ставит таймауты действий в **0** (без ограничения) — можно думать сколько угодно;
- останавливается **перед первым действием** и открывает Inspector.

В окне Inspector:

| Элемент | Что |
|---|---|
| ▶ Resume (F8) | выполнять до конца или до следующего `page.pause()` |
| Step over (F10) | выполнить одно действие |
| Pick locator | выбрать элемент в браузере — показать локатор |
| поле Locator | ввести свой локатор — браузер **подсветит**, что он находит (и сколько) |
| лог действия | для текущего шага: какой элемент нашёл локатор, какие actionability-проверки ждал |
| Record | начать запись прямо с текущего состояния страницы |

Поле Locator — лучший способ проверить локатор: вписал
`get_by_test_id("order-row").filter(has_text="10")` — сразу видно, что подсвечены две строки.

##### `page.pause()`

```python
def test_order(logged_in_page: Page):
    deposit(logged_in_page, "USDT", "1000")
    logged_in_page.pause()          # здесь остановимся и откроется Inspector
    ...
```

Запускать с `--headed` (или `PWDEBUG=1`). Без headed-режима pause тоже откроет Inspector,
но удобнее видеть браузер.

**Запись с середины теста.** Это главный приём с codegen: фикстура уже залогинила и пополнила
счёт, тест стоит на `pause()` → в Inspector жмёшь Record → кликаешь нужный кусок сценария →
копируешь сгенерированные строки в тест → убираешь `pause()` → переписываешь по чек-листу.
Не нужно каждый раз проходить регистрацию руками.

**Не забыть убрать `pause()`**: в CI тест повиснет. Это частое замечание на ревью.

---

#### 6. Лог `DEBUG=pw:api`

Без окон — подробный лог в консоль, что Playwright делает на каждом шаге:

```bash
DEBUG=pw:api uv run pytest tests/ui/test_u2_03_codegen_inspector.py -k deposit -s
```

```
pw:api waiting for get_by_role("button", name="Войти")
pw:api   locator resolved to <button type="submit" data-testid="login-button">Войти</button>
pw:api attempting click action
pw:api   waiting for element to be visible, enabled and stable
pw:api   element is visible, enabled and stable
pw:api   scrolling into view if needed
pw:api   done scrolling
pw:api   performing click action
pw:api   click action done
```

(реальный вывод на стенде для клика по «Войти»)

Пригодится, когда тест висит на действии: видно, **чего** он ждёт —
`element is not enabled`, `<div class="toast"> intercepts pointer events`, `element is not stable`.

---

#### 7. Частые ошибки

- Коммитят запись codegen без переписывания: зашитые URL и данные, нет проверок.
- Доверяют `.nth()` из записи — локатор привязан к состоянию страницы в момент записи.
- Записывают долгий сценарий с регистрацией каждый раз вместо `page.pause()` + Record.
- Оставляют `page.pause()` в коде.
- Запускают codegen без `--channel chrome` у нас — Chromium не стартует.
- Коммитят `--save-storage` файл с токеном.
- Используют только Pick locator и не проверяют локатор в поле Locator на нескольких элементах
  (два ордера вместо одного).

---

#### Собес: вопросы и ответы

**1. Пользуешься ли codegen? Для чего?**
> Да, как вспомогательный инструмент: быстро подобрать локаторы на незнакомой странице, получить
> черновик шагов и разобраться, как страница реагирует. Записанный код как тест не использую:
> там зашитые адреса и данные, лишние клики, нет проверок результата и локаторы привязаны
> к состоянию на момент записи. Запись всегда переписываю под фикстуры, хелперы и проверки.

**2. Что нужно поменять в коде после codegen?**
> Адрес — на относительный с `base_url`. Данные — на уникальные из фикстур. Убрать лишние
> `click` перед `fill` и нажатия Tab. Вынести логин и подготовку в фикстуры и хелперы.
> Добавить проверки бизнес-результата после значимых шагов. Заменить позиционные локаторы
> на фильтры по содержимому. Разбить на тесты с понятными именами.

**3. Как codegen выбирает локатор? Совпадает ли это с тем, как выбираешь ты?**
> Сначала test-id, потом роль с именем, label, placeholder, текст, в крайнем случае CSS,
> и проверяет уникальность в момент записи. Я обычно ставлю роль выше test-id: она заодно
> проверяет доступность и то, что видит пользователь. И codegen не знает, останется ли локатор
> уникальным при других данных — это проверяю сам.

**4. Как отладить тест по шагам?**
> `PWDEBUG=1` — headed, без таймаутов, пауза перед первым действием, Inspector: шаг за шагом,
> лог actionability, подсветка элементов, поле для проверки локатора. Или `page.pause()`
> в нужном месте. Если окна неудобны — `DEBUG=pw:api` в консоль. После прогона — Trace Viewer.

**5. Как записать шаги, не проходя каждый раз логин?**
> Поставить `page.pause()` в тест после фикстур — пользователь уже залогинен — и нажать Record
> в Inspector. Или запустить codegen с `--load-storage`, сохранив state через `--save-storage`.

**6. Тест висит на клике — как понять почему?**
> Посмотреть лог действия в Inspector или `DEBUG=pw:api`: Playwright пишет, какую проверку
> ждёт — элемент невидим, disabled, двигается, или его перекрывает другой элемент, и какой именно.
> Дальше чиню причину, а не ставлю `force=True`.

### Задания — `tests/ui/test_u2_03_codegen_inspector.py`

```text
U2. Урок 3 — Codegen и Inspector.

Теория: practice/u2_03_codegen_inspector.md
Запуск:
    uv run pytest tests/ui/test_u2_03_codegen_inspector.py -v

Задачи 1, 4, 5, 8 — руками в браузере, результат — файлы и записи в «Ответах».
Стенд должен быть запущен: docker compose up -d → http://localhost:8080.

Задача 1. Запись сценария.
    uv run playwright codegen --target python-pytest --channel chrome         --viewport-size "1440,900" -o practice/u2_03_recorded_raw.py http://localhost:8080/app/
    Запиши: регистрация → пополнить USDT 1000 → BUY ETH-USDT цена 100 кол-во 1 → отменить ордер.
    Через панель добавь проверки: Assert text на статус CANCELED, Assert value на поле «Сумма».
    Закрой окно — файл сохранится. НЕ правь его: это исходник для задач 2 и 3.
    (Имя без test_ — pytest его не соберёт.)

Задача 2. Ревью записи.
    Пройди practice/u2_03_recorded_raw.py по чек-листу из теории (раздел 4).
    В «Ответах» — список проблем с номерами строк, минимум 6.
    Запусти запись дважды: uv run pytest practice/u2_03_recorded_raw.py — что на втором прогоне и почему?

Задача 3. Переписать.
    Здесь, в этом файле: тот же сценарий как нормальный тест (или несколько тестов).
    Фикстуры и хелперы, уникальные данные, локаторы по приоритету курса, проверки бизнес-результата:
    после пополнения доступно 1000; после ордера заблокировано 100 и доступно 900;
    после отмены статус CANCELED, кнопки нет, снова 1000 и 0.

Задача 4. Какие локаторы без test-id.
    Запусти codegen с --test-id-attribute data-nothing (несуществующий атрибут), сделай то же самое,
    сохрани в practice/u2_03_recorded_no_testid.py.
    В «Ответах»: сравни с задачей 1 — какие локаторы стали другими, какие ты бы взял в тест и почему.

Задача 5. Запись залогиненным.
    а) codegen ... --save-storage .auth/u2_03.json http://localhost:8080/app/ — зарегистрируйся, закрой.
    б) codegen ... --load-storage .auth/u2_03.json http://localhost:8080/app/ — открылся кабинет?
    в) Проверь: git status не показывает .auth/ (он в .gitignore). Почему этот файл нельзя коммитить?

Задача 6. page.pause() + Record.
    Тест: logged_in_page, deposit USDT 1000, потом logged_in_page.pause().
    Запусти с --headed, в Inspector нажми Record, размести BUY ETH-USDT цена 50 кол-во 2
    и отмени его. Скопируй сгенерированные строки в тест, убери pause(), перепиши по чек-листу.
    В итоге тест без pause: ордер создан (заблокировано 100), отменён (заблокировано 0).

Задача 7. Inspector пошагово.
    PWDEBUG=1 uv run pytest tests/ui/test_u2_03_codegen_inspector.py -k <тест из задачи 3>
    Пройди Step over до клика «Разместить ордер» — посмотри лог действия: что ждал Playwright.
    Пока тест на паузе, руками в браузере размести ещё два BUY-ордера: цены 10 и 100.
    В поле Locator проверь три локатора и запиши в «Ответах», сколько элементов подсветилось и почему:
        get_by_role("button", name="Отменить")
        get_by_test_id("order-row").filter(has_text="10")
        get_by_role("combobox")

Задача 8. DEBUG=pw:api.
    DEBUG=pw:api uv run pytest tests/ui/test_u2_03_codegen_inspector.py -k <тест из задачи 3> -s
    Найди в логе клик по «Пополнить»: какие проверки ждал Playwright? Скопируй 5–6 строк в «Ответы».

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Пользуешься ли codegen? Для чего?
    2. Что нужно поменять в коде после codegen?
    3. Как codegen выбирает локатор? Совпадает ли это с тем, как выбираешь ты?
    4. Как отладить тест по шагам?
    5. Как записать шаги, не проходя каждый раз логин?
    6. Тест висит на клике — как понять почему?
```

<a id="u2-4"></a>

## U2.4 Флейки и собес по модулю U2

*Теория: `practice/u2_04_flaky_interview.md`*

Задания: `tests/ui/test_u2_04_flaky.py`.

План: что такое флейк и почему он дорогой; откуда они берутся (классификация с примерами,
которые мы уже встретили на стенде); как воспроизвести и найти причину; как чинить
по категориям; ретраи и карантин — когда можно, когда вредно; чек-лист ревью на флейки.
В конце — шпаргалка и банк вопросов по всему модулю U2.

---

#### 1. Что такое флейк

**Флейк (flaky test)** — тест, который на одном и том же коде то проходит, то падает.

Почему это дорого:
- команда перестаёт верить красному: «а, это опять флейк» — и пропускает настоящий баг;
- перезапуски CI съедают время;
- каждый флейк — либо проблема теста, либо **настоящая гонка в продукте**, которую видят пользователи.
  Не разобравшись, нельзя сказать, что из двух.

---

#### 2. Откуда берутся флейки

| Категория | Пример | Где мы это видели |
|---|---|---|
| **Ожидания / гонки в тесте** | прочитали значение до обновления UI | U2.1: `text_content()` сразу после тоста даёт старое `"0"` |
| | проверка по старому сигналу | U2.1: одинаковый тост → `form.reset()` стёр ввод, 2 ордера из 3 |
| | проверка отсутствия до загрузки | U2.1: `to_have_count(0)` зелёный, хотя ордер есть |
| **Общие данные** | тесты делят пользователя, стакан, справочник | U1.4: наш SELL исполнился об чужой BUY 101 из U1.2 |
| **Зависимость от порядка** | тест работает, только если до него прошёл другой | `storage_state` из прошлого теста, общий email |
| **Позиционные локаторы** | `.first` / `nth` при меняющемся порядке | U2.2: `all()` на перерисовывающейся таблице |
| **Время** | `datetime.now()`, полночь, часовой пояс, истёкший токен | токен в сохранённом state истёк |
| **Фоновые процессы** | результат появится «когда-нибудь» | матчинг раз в 1 с + опрос раз в 2 с → таймаут 15 с в U1.4 |
| **Окружение** | 5xx, медленная сеть, перегруженный CI | stage с режимом сбоев (раздел 3) |
| **Инфраструктура** | браузер упал, не хватило памяти, порт занят | |
| **Продукт** | настоящая гонка в приложении | двойной клик создаёт два ордера; ответ потерян, но действие выполнено |

Самые частые — первые две строки. Почти всегда «флейк» — это **тест, который не ждёт нужного
результата** или **делит данные с другими тестами**.

---

#### 3. Режим сбоев стенда

```bash
EXCHANGE_CHAOS_RATE=0.3 docker compose up -d        # основной стенд :8080, 30% запросов — 503
docker compose --profile stage up -d                 # stage :8081, своя база, 5% сбоев
```

Что делает (`exchange/chaos.py`):
- случайные запросы получают **503** с `Retry-After: 1`;
- **половина** сбоев случается **после** обработки: изменения сохранены, а клиент получил ошибку —
  так выглядит ответ, потерянный по дороге;
- `/health` и `/docs` не затрагиваются, а **статика `/app/` — затрагивается**: может не загрузиться
  `index.html`, `app.js` или `styles.css`.

Что видит тест (по коду `chaos.py` и `app.js`):

| Запрос получил 503 | Что в UI | Как падает тест |
|---|---|---|
| `app.js` / `index.html` | страница пустая или без JS | `Locator.fill: Timeout 30000ms exceeded` — **про 503 ни слова** |
| `POST /auth/register` | ошибка в форме | кабинет не виден: `expected to be visible` |
| `POST /balances/deposit` | тост «Service temporarily unavailable» | тост не тот / баланс не тот |
| `GET /orders` из опроса | ничего: фронт молча ждёт следующий опрос | только задержка на 2 с |
| `POST` после обработки | ошибка в UI, но действие **выполнено** | баланс «внезапно» больше ожидаемого |

Похожая история случилась при подготовке урока: на stage все тесты падали с `Locator.fill: Timeout`.
Причиной был не режим сбоев, а **устаревший образ** stage без веб-интерфейса: `/app/` отдавал 404.
Лечилось `docker compose --profile stage up -d --build`. Вывод: **текст ошибки — это симптом,
а не причина**. Причину показывают trace, скриншот, логи сервера.

---

#### 4. Как найти причину

##### Шаг 1. Воспроизвести

```bash
uv run pytest tests/ui/test_x.py -k name --count 20 -x        # pytest-repeat: 20 раз, стоп на первом падении
uv run pytest tests/ui/test_x.py --count 10 -q | tail -1        # процент падений
```

Если не воспроизводится — сделать окружение похожим на CI:
- **медленная сеть**: `slow_network(page, 400)` (U2.1) — лучший способ поймать гонку ожидания;
- **сбои**: stage или `EXCHANGE_CHAOS_RATE`;
- **headless**, тот же размер окна, тот же браузер, что в CI;
- **другой порядок / только этот тест отдельно** — проверка зависимости от порядка;
- **параллельный запуск** (xdist — U6) — проверка общих данных.

`--slowmo` для поиска гонок **не подходит**: он замедляет действия теста, и UI успевает обновиться — гонка прячется.

##### Шаг 2. Собрать артефакты

```bash
uv run pytest ... --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure
uv run playwright show-trace test-results/<папка теста>/trace.zip
```

В trace: каждый шаг, DOM до и после, сеть со статусами, консоль. Видно, например, что на шаге `fill`
страница пустая, а во вкладке Network `app.js` — 503. Подробно — U7.

##### Шаг 3. Логи сервера по X-Request-ID

Стенд возвращает `X-Request-ID` в каждом ответе и пишет его в лог:

```python
with page.expect_response(lambda r: r.url.endswith("/balances/deposit")) as info:
    ...click()
print(info.value.status, info.value.headers["x-request-id"])
```

```bash
docker compose logs exchange-stage | grep <request_id>
```

Так отличают «бэкенд ответил 503 / 500» от «бэкенд ответил 200, а UI показал не то».

##### Шаг 4. Классифицировать

| Сообщение | Чаще всего значит |
|---|---|
| `TimeoutError: Locator.click/fill: Timeout` | элемента нет: страница не загрузилась, не тот экран, локатор устарел |
| `AssertionError ... Actual value: <старое>` | проверили не то / не дождались нужного сигнала / данные чужие |
| `strict mode violation` | данных больше, чем ожидал тест (дубль, чужие данные) |
| `Element is not attached to the DOM` | ElementHandle после перерисовки |
| разный `Actual value` в разных прогонах | гонка или общие данные |

---

#### 5. Как чинить

| Причина | Починка |
|---|---|
| не дождались результата | `expect` на бизнес-результат; хелпер ждёт ответ (`expect_response`), а не тост |
| проверка отсутствия до загрузки | сначала положительный признак загрузки |
| общие данные | свой пользователь на тест; данные, не пересекающиеся с чужими; очистка после себя |
| порядок тестов | каждый тест готовит своё состояние сам |
| позиционный локатор | `filter` по неизменному признаку, `data-id` |
| фоновый процесс | точечный `timeout=` с комментарием почему; или дождаться через API |
| время | фиксировать время (`page.clock` — U3), не зависеть от «сейчас» |
| нестабильное окружение | чинить окружение; тест не должен маскировать 5xx |
| баг продукта | **баг-репорт**, тест остаётся красным или `xfail` со ссылкой |

Чего **не** делать: `sleep`, большой глобальный таймаут, `force=True`, `try/except` вокруг проверки,
повтор действия в тесте «если не получилось».

---

#### 6. Ретраи и карантин

##### pytest-rerunfailures

```bash
uv run pytest --reruns 2 --reruns-delay 1          # упавший тест перезапускается до 2 раз
```

```python
@pytest.mark.flaky(reruns=2, reruns_delay=1)       # только для одного теста
def test_trade(...): ...
```

В отчёте такие тесты помечены `RERUN`. Тест, прошедший со второй попытки, — **флейк**,
даже если итог зелёный.

Когда ретраи допустимы:
- в CI как **временная** страховка от инфраструктурных сбоев, при этом отчёт показывает,
  какие тесты прошли с перезапуска, и по ним заводятся задачи;
- для тестов на реальном внешнем окружении, которое вы не контролируете.

Почему вредны «по умолчанию»:
- прячут **настоящие гонки в продукте** — пользователь их увидит, а CI зелёный;
- прячут гонки в тесте — флейков становится больше, никто не чинит;
- замедляют прогон: каждое падение — это ещё 1–2 полных прогона теста.

##### Повтор действия внутри теста — опасно

```python
for _ in range(3):                  # ПЛОХО
    deposit_button.click()
    if toast_ok(): break
```

Если запрос выполнился, а ответ потерялся (половина сбоев на стенде), повтор **пополнит дважды**.
Неидемпотентные действия повторять нельзя. Перезапуск **всего** теста безопаснее: новый пользователь,
новые данные. (Как API решает это ключом идемпотентности — в модуле API.)

##### Карантин

Флейк, который не починить сразу, выносят из основного прогона, но не удаляют:

```python
@pytest.mark.quarantine            # зарегистрировать маркер; основной прогон: -m "not quarantine"
def test_trade(...): ...
```

Правила: у каждого теста в карантине — задача и владелец; карантин регулярно разбирают;
тест возвращается после N зелёных прогонов подряд (`--count 50`).
Для известного бага продукта — `xfail(reason="BUG-...", strict=True)`.

---

#### 7. Чек-лист ревью на флейки

- [ ] нет `sleep`, `wait_for_timeout`, `networkidle`;
- [ ] проверки через `expect`, не через `is_visible()` / `count()` / `text_content()`;
- [ ] после действия проверяется **результат**, а не промежуточный сигнал (тост, disabled);
- [ ] перед проверкой отсутствия — положительный признак загрузки;
- [ ] свой пользователь и данные на тест; данные не пересекаются с чужими (цены, имена);
- [ ] тест не зависит от порядка и других тестов;
- [ ] нет `.first` / `nth` / `all()` с действиями без причины;
- [ ] долгие процессы — точечный таймаут с комментарием;
- [ ] нет повторов неидемпотентных действий;
- [ ] нет `force=True`, `try/except` вокруг `expect`, `page.pause()`;
- [ ] прогнан `--count 20` и под `slow_network` — зелёный.

---

#### 8. Шпаргалка по модулю U2

**Ожидание перед действием** (U1.4) — actionability: attached, visible, stable, receives events,
enabled, editable. 30 с.

**Ожидание результата** (U2.1) — `expect` повторяет проверку, 5 с. Методы «в моменте»
(`is_visible`, `count`, `text_content`) — не для проверок. `expect.soft` — копит ошибки.
Ловушки: ранняя проверка отсутствия, одинаковый тост, мигающие состояния.
Сеть: `expect_response` / `expect_request` — слушать до действия, фильтровать по методу.
`networkidle` — нет. `wait_for_function` — для состояния вне DOM.

**Локаторы** (U2.2) — strict mode: одна операция — один элемент. Разрешать: точнее роль/имя → контейнер
→ `filter` → `data-id` → позиция только как требование. `has_text` — подстрока без регистра.
`rows.locator("td").nth(2)` — одна ячейка на таблицу; колонка — `td:nth-child`. Locator ищет заново,
ElementHandle протухает. `all()` на меняющемся списке — нет.

**Инструменты** (U2.3) — codegen: черновик и подбор локаторов, переписывать всегда.
Inspector: `PWDEBUG=1`, `page.pause()` + Record. `DEBUG=pw:api` — чего ждёт действие.

**Флейки** (U2.4) — воспроизвести (`--count`, `slow_network`, chaos) → артефакты (trace) →
логи по X-Request-ID → классифицировать → чинить причину. Ретраи — временно и с отчётом.

---

#### Собес: вопросы и ответы

**1. Тест флейкает. Как найдёшь причину?**
> Сначала воспроизвожу: гоняю тест много раз (`--count 20`), если не падает — делаю окружение похожим
> на CI: замедляю сеть, включаю сбои, запускаю отдельно и в другом порядке, параллельно.
> Собираю артефакты: trace, скриншот, видео. В trace смотрю, на каком шаге UI был не в том состоянии
> и что было в сети. Ответы сервера сверяю с логами по X-Request-ID. Дальше классифицирую:
> не дождались результата, общие данные, порядок, окружение или настоящая гонка в продукте —
> и чиню причину, а не добавляю паузу.

**2. Какие самые частые причины флейков в UI-тестах?**
> Тест не ждёт нужного результата: читает значение в моменте, проверяет промежуточный сигнал вроде
> тоста, проверяет отсутствие до загрузки данных. Второе — общие данные между тестами.
> Дальше — позиционные локаторы, зависимость от порядка, время, фоновые процессы,
> нестабильное окружение. И иногда это настоящая гонка в приложении — тогда это баг.

**3. Почему `sleep` / `wait_for_timeout` — антипаттерн?**
> Пауза одновременно слишком длинная — тест всегда медленный — и слишком короткая: в CI под нагрузкой
> ответ идёт дольше, и тест падает. Она не проверяет условие. Нужно ждать конкретный результат:
> `expect` на элемент, ответ сервера, URL.

**4. Как относишься к ретраям упавших тестов?**
> Как к временной мере. Ретраи прячут и гонки в тесте, и настоящие гонки в продукте, и замедляют прогон.
> Если включаем — только в CI, с отчётом, какие тесты прошли со второй попытки, и с задачами на них.
> Повторять неидемпотентное действие внутри теста нельзя вообще: если ответ потерялся, а действие
> выполнилось, повтор задвоит операцию.

**5. Что делать с флейком, который нельзя починить сейчас?**
> Карантин: вынести из основного прогона маркером, завести задачу с владельцем, регулярно разбирать.
> Вернуть после серии зелёных прогонов. Если причина — известный баг продукта, `xfail` со ссылкой
> на баг и `strict=True`, чтобы заметить, когда починят.

**6. Тест упал с `Timeout 30000ms` на `fill`. О чём это говорит?**
> Что поля не было на странице 30 секунд — но не почему. Возможно, страница не загрузилась
> (5xx на статику), открылся не тот экран, сменился локатор или пользователь не залогинился.
> Смотрю trace: DOM на этом шаге и вкладку Network. На нашем стенде в режиме сбоев так выглядит
> 503 на `app.js`.

**7. Локатор нашёл несколько элементов. Что делать?** — см. U2.2, вопрос 3.

**8. Почему `expect`, а не `assert`?** — см. U2.1, вопрос 1.

**9. Как в одном тесте убедиться, что UI отправил правильный запрос?** — см. U2.1, `expect_request`.

**10. Как защитить тест от общих данных?**
> Свой пользователь на каждый тест через фабрику; данные, которые не пересекаются с чужими —
> уникальные имена, цены вне диапазона других тестов; очистка после себя, если ресурс общий;
> не полагаться на «пустое» состояние системы. В идеале — изолированное окружение на прогон.

### Задания — `tests/ui/test_u2_04_flaky.py`

```text
U2. Урок 4 — флейки и собес по модулю U2.

Теория: practice/u2_04_flaky_interview.md
Подготовка:
    uv sync                                    # поставит pytest-repeat и pytest-rerunfailures
    docker compose --profile stage up -d --build   # stage :8081 с 5% сбоев; --build обязателен,
                                                   # иначе может остаться старый образ без /app/
Запуск против stage:
    uv run pytest tests/ui/test_u2_04_flaky.py --base-url http://localhost:8081 -v

Задача 1. Флейки на stage.
    Прогони решённый U1.4 против stage три раза подряд:
        uv run pytest tests/ui/test_u1_04_context_pytest.py --base-url http://localhost:8081             --count 3 --tracing retain-on-failure -q
    (Занимает несколько минут: каждое падение ждёт таймаут.)
    В «Ответах»: сколько упало; для 2–3 падений — текст ошибки и НАСТОЯЩАЯ причина из trace:
        uv run playwright show-trace test-results/<папка>/trace.zip   (вкладка Network)

Задача 2. Потерянный ответ.
    Против stage с 30% сбоев: EXCHANGE_STAGE_CHAOS_RATE=0.3 docker compose --profile stage up -d
    Тест: новый пользователь (если регистрация упала — это тоже сбой, перезапусти),
    пополняй USDT 100 в цикле, пока не увидишь тост "Service temporarily unavailable"
    (не больше 20 попыток; ловить ответ через expect_response, считать успешные).
    Затем reload и прочитай доступный USDT. Сравни с 100 * <число успешных ответов>.
    Если больше — нашёл «ответ потерян, но действие выполнено».
    В «Ответах»: что увидит пользователь и почему повторять такое действие в тесте опасно.
    После задачи верни 5%: docker compose --profile stage up -d

Задача 3. X-Request-ID.
    Против stage: поймай ответ на пополнение, выведи статус и заголовок x-request-id (запуск с -s).
    Найди запрос в логах: docker compose logs exchange-stage | grep <id>
    Скопируй строку лога в «Ответы». Повтори, пока не поймаешь 503, — как он выглядит в логе?

Задача 4. Процент флейков.
    Перенеси сюда naive_deposit из U2.1 (задача 4а): три пополнения подряд, ожидаешь 300.
    Против основного стенда :8080 (без сбоев):
        а) без slow_network: --count 10 — сколько упало?
        б) со slow_network(page, 400): --count 10 — сколько упало?
    Запиши оба числа и объясни разницу.

Задача 5. Ретраи прячут проблему.
    Тот же тест со slow_network: uv run pytest ... -k naive --count 5 --reruns 3
    Посмотри на RERUN в выводе. В «Ответах»: почему зелёный итог здесь — плохой результат.

Задача 6. Карантин.
    Зарегистрируй маркер quarantine в pyproject.toml. Пометь им naive-тест.
    Покажи, что uv run pytest tests/ui/test_u2_04_flaky.py -m "not quarantine" его не запускает.

Задача 7. Классификация (письменно, в «Ответах»).
    Для каждого случая: категория (раздел 2 теории), как проверить гипотезу, как починить.
        а) Тест «отмена ордера» падает 1 раз из 15, strict mode violation: 2 кнопки «Отменить».
        б) Тест проходит один, падает только если перед ним запускался тест логина.
        в) В CI падает «баланс 900», локально всегда зелёный; Actual value: 1000.
        г) Тест падает каждую ночь между 00:00 и 00:05.
        д) При параллельном запуске падает «у продавца исполнено 1», Actual: 0.
        е) Иногда после одного клика «Разместить ордер» в таблице два одинаковых ордера,
           хотя тест кликает ровно один раз.

Задача 8. Устный собес по модулю U2.
    Включи диктофон: 10 случайных вопросов из разделов «Собес» U2.1–U2.4, 40–90 с на ответ,
    без подглядывания. Прослушай, сверь. В «Ответах» — номера, на которых «поплыл».

Вопросы собеса — раздел «Собес» теории (10 вопросов), отвечай своими словами в «Ответах».
```


---

# U3. Сложные элементы и сценарии

<a id="u3-1"></a>

## U3.1 Вкладки, всплывающие окна и iframe

*Теория: `practice/u3_01_tabs_popups_iframes.md`*

Задания: `tests/ui/test_u3_01_tabs_popups_iframes.py`. Страница: **лаборатория** `/app/lab.html`
(блоки «Вкладки и окна», «Виджет курса»; стенд пересобери: `docker compose up -d --build`).

Модуль U3: U3.1 вкладки, окна, iframe → U3.2 диалоги и файлы → U3.3 мышь, клавиатура, скролл →
U3.4 Shadow DOM, таблицы, cookies и localStorage + собес и лайвкодинг.

---

#### 1. Новая вкладка (`target="_blank"`)

Ссылка «Открыть отчёт BTC» на лаборатории открывает `report.html` в новой вкладке. Новая вкладка —
новый объект `Page` **в том же context** (общие cookies и localStorage, U1.4). Поймать её — слушать
событие **до** клика:

```python
with page.context.expect_page() as new_page_info:
    page.get_by_test_id("report-link").click()
report = new_page_info.value                      # Page новой вкладки

expect(report.get_by_test_id("report-title")).to_have_text("Отчёт по BTC")
expect(report).to_have_title("Отчёт BTC")
report.close()                                    # закрыть вкладку; page продолжает работать
```

Проверено на лаборатории. Дождаться загрузки новой вкладки явно — `report.wait_for_load_state()`,
но обычно хватает web-first `expect` на её содержимое.

Все вкладки context — `page.context.pages`. Переключаться «фокусом», как в Selenium, не нужно: у каждой
вкладки свой объект, работаешь с тем, который нужен. `report.bring_to_front()` — только если важна
активная вкладка (например, для `document.visibilityState`).

Если открытие вкладки — деталь реализации, а не сценарий, ссылку можно проверить без перехода:
`expect(link).to_have_attribute("href", re.compile(r"report\.html\?asset=BTC"))` и `target="_blank"`.

---

#### 2. Всплывающее окно (`window.open`)

Кнопка «Открыть калькулятор» вызывает `window.open("calc.html", ...)`. Это **popup** — страница,
у которой есть `opener`:

```python
with page.expect_popup() as popup_info:
    page.get_by_test_id("popup-button").click()
calc = popup_info.value

calc.get_by_test_id("calc-price").fill("100")
calc.get_by_test_id("calc-quantity").fill("2.5")
calc.get_by_test_id("calc-submit").click()        # окно отправляет результат opener'у и закрывается

expect(page.get_by_test_id("popup-result")).to_have_text("250.00")
assert calc.is_closed()
```

Проверено: результат пришёл в основную страницу через `postMessage`, окно закрылось само.

| | `page.expect_popup()` | `context.expect_page()` |
|---|---|---|
| Что ловит | страницы, открытые **этой** страницей (`window.open`, `target=_blank`) | **любую** новую страницу context |
| Когда | связь «открыл → открытое» важна | вкладка могла открыться откуда угодно |

`page.on("popup", handler)` — если окно открывается не по твоему действию (реклама, OAuth).

##### OAuth и платёжные окна

Типичный сценарий: «Войти через Google» открывает popup, после логина он закрывается, основная страница
залогинена. В тестах сторонний провайдер **не используют** (капчи, лимиты, 2FA): мокают (U6.1) или
логинят через API и storage_state (U5). Popup-механику проверяют на своём тестовом провайдере.

---

#### 3. iframe

iframe — **отдельный документ** внутри страницы. Локаторы страницы внутрь iframe не видят:

```python
page.get_by_test_id("widget-price")               # 0 элементов — он внутри iframe
```

##### frame_locator — основной способ

```python
widget = page.frame_locator('[data-testid="rate-widget"]')     # или "iframe[title='Курс ETH']"
widget.get_by_test_id("widget-amount").fill("2")
expect(widget.get_by_test_id("widget-total")).to_have_text("7000.00")
widget.get_by_test_id("widget-refresh").click()
expect(widget.get_by_test_id("widget-price")).to_have_text("3510.00")
```

`frame_locator` ленивый, как Locator: iframe перезагрузили — продолжает работать.
В современном API есть и `locator.content_frame` — то же из обычного локатора на `<iframe>`:

```python
widget = page.get_by_title("Курс ETH").content_frame
```

Проверено: оба способа находят цену в виджете.

##### Frame — объект документа

```python
page.frames                                       # главный + все iframe: ['lab.html', 'widget.html']
frame = page.frame(url=re.compile(r"widget\.html"))
frame.evaluate("document.title")
```

`Frame` нужен для `evaluate` внутри iframe, ожиданий навигации iframe. Для действий и проверок —
`frame_locator`.

##### Вложенные и общение со страницей

```python
page.frame_locator("#outer").frame_locator("#inner").get_by_role("button")
```

Кнопка «Подписаться» в виджете отправляет `postMessage` родителю — основная страница показывает
«Подписка на ETH-USDT». Тест проверяет **результат** на стороне страницы:
`expect(page.get_by_test_id("widget-message")).to_have_text("Подписка на ETH-USDT")`.

##### Другой домен

Cross-origin iframe (платёжная форма на домене провайдера) Playwright обрабатывает так же — `frame_locator`
работает, в отличие от JS в странице, которому браузер запретил бы доступ. Но **логику провайдера**
не тестируют — только интеграцию: форма встроена, результат вернулся.

---

#### 4. Частые ошибки

| Ошибка | Как правильно |
|---|---|
| клик, потом `context.pages[-1]` | `expect_page` / `expect_popup` **вокруг** клика — иначе гонка |
| ищут элемент iframe локатором страницы | `frame_locator` / `content_frame` |
| `page.frames[1]` по индексу | по `url` или `name`, а лучше `frame_locator` по атрибуту iframe |
| «переключение» на вкладку, как в Selenium | у каждой вкладки свой `Page` |
| тестируют сторонний OAuth / платёжку вживую | мок или логин через API |
| забыли, что вкладка в том же context | новая вкладка видит тот же логин — это не изоляция |

---

#### Собес: вопросы и ответы

**1. Как работать с новой вкладкой в Playwright?**
> Обернуть действие в `context.expect_page()` или `page.expect_popup()` — получаю объект новой страницы.
> Переключаться не нужно: работаю с ним напрямую, основная страница остаётся доступна. Вкладка в том же
> context — общие cookies и localStorage. После проверки закрываю.

**2. Чем отличается popup от новой вкладки?**
> Технически оба — новая Page в context. Popup — страница, открытая этой страницей (`window.open` или
> `target=_blank`), у неё есть opener; `expect_popup` ловит именно их. `context.expect_page` ловит любую новую
> страницу context.

**3. Как тестировать iframe?**
> `frame_locator` по атрибуту iframe или `content_frame` у локатора iframe — дальше обычные локаторы и expect
> внутри. Он ленивый, переживает перезагрузку iframe. Объект Frame — для evaluate. Cross-origin работает
> так же. Если iframe общается со страницей через postMessage — проверяю результат на стороне страницы.

**4. Как тестировать «Войти через Google»?**
> Сторонний провайдер в автотестах не дёргаю — капчи, лимиты, 2FA. Логин — через API и storage_state или
> мок ответа провайдера. Механику popup проверяю на тестовом провайдере, если он есть.

### Задания — `tests/ui/test_u3_01_tabs_popups_iframes.py`

```text
U3. Урок 1 — вкладки, всплывающие окна и iframe.

Теория: practice/u3_01_tabs_popups_iframes.md
Страница: /app/lab.html (стенд пересобрать: docker compose up -d --build).
Запуск:
    uv run pytest tests/ui/test_u3_01_tabs_popups_iframes.py -v

Задача 1. LabPage (ui_framework/pages/lab_page.py; если делал U6.3 — дополни) и компоненты:
    WindowsPanel (report_link, popup_button, popup_result), RateWidget (root — FrameLocator виджета:
    price, amount, total, refresh, subscribe). Подумай: подходит ли BaseComponent из U4.2 для FrameLocator?

Задача 2. Новая вкладка.
    Клик по «Открыть отчёт BTC» → новая вкладка: заголовок «Отчёт по BTC», title «Отчёт BTC».
    Закрой вкладку — лаборатория работает (кликни что-нибудь и проверь). Сколько страниц в context
    до и после?

Задача 3. Тот же отчёт без перехода.
    Проверь href и target ссылки, не открывая вкладку. В «Ответах»: когда достаточно такой проверки,
    а когда нужно открывать вкладку.

Задача 4. Popup-калькулятор.
    parametrize: (100, 2.5 → 250.00), (0.1, 3 → 0.30), (пусто, 5 → 0.00).
    После «Рассчитать и закрыть» окно закрыто, в лаборатории — результат.

Задача 5. Вкладка из меню «Ещё».
    Пункт «Отчёт USDT» в меню по наведению → новая вкладка с отчётом USDT.
    Какой способ ожидания выберешь — expect_popup или context.expect_page — и почему?

Задача 6. iframe.
    а) Сумма 2 → итог 7000.00; «Обновить» → цена 3510.00 и итог 7020.00.
    б) Тот же сценарий через content_frame вместо frame_locator.
    в) «Подписаться» → в лаборатории (вне iframe!) «Подписка на ETH-USDT».
    г) Покажи, что page.get_by_test_id("widget-price") без frame_locator находит 0 элементов
       (to_have_count(0)) — и объясни.

Задача 7. Frame.
    Найди frame виджета через page.frame(url=...) и прочитай document.title через evaluate.
    Перезагрузи iframe (frame.goto(frame.url) или evaluate("location.reload()")) — твой RateWidget
    из задачи 1 продолжает работать? Почему?

Задача 8. Изоляция вкладок (вспомни U1.4).
    Нажми «Принять» в баннере cookies в лаборатории, открой отчёт в новой вкладке, вернись и открой
    лабораторию во второй вкладке того же context: баннер есть? А в новом context?

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как работать с новой вкладкой в Playwright?
    2. Чем отличается popup от новой вкладки?
    3. Как тестировать iframe?
    4. Как тестировать «Войти через Google»?
```

<a id="u3-2"></a>

## U3.2 Диалоги браузера, загрузка и скачивание файлов

*Теория: `practice/u3_02_dialogs_files.md`*

Задания: `tests/ui/test_u3_02_dialogs_files.py`. Страница: лаборатория `/app/lab.html`
(блоки «Диалоги», «Импорт и экспорт»).

План: нативные диалоги `alert` / `confirm` / `prompt` / `beforeunload` и как Playwright с ними
работает (поведение по умолчанию — проверено); загрузка файлов — `set_input_files` с диска, из памяти,
несколько, очистка, file chooser; скачивание — `expect_download`, имя, сохранение, проверка содержимого;
генерация файлов для тестов.

---

#### 1. Диалоги браузера

Это **нативные** окна браузера (`alert`, `confirm`, `prompt`), не HTML-модалки (U4.2). Пока диалог открыт,
страница заблокирована — JS ждёт ответа.

##### Поведение по умолчанию

Если у страницы **нет** обработчика события `dialog`, Playwright **сам закрывает** диалог (`dismiss`).
Проверено: кнопка «Очистить избранное» без обработчика → `confirm` вернул `false` → «Отменено».
Для `confirm` это «Отмена», для `prompt` — `null`.

Поэтому тест «подтверждаю удаление» без обработчика молча проверит **отмену**.

##### Обработчик

```python
page.once("dialog", lambda dialog: dialog.accept())        # один раз, на ближайший диалог
page.get_by_test_id("confirm-button").click()
expect(page.get_by_test_id("dialog-result")).to_have_text("Избранное очищено")
```

```python
def answer(dialog: Dialog) -> None:
    assert dialog.type == "prompt"
    assert dialog.message == "Новое имя портфеля"
    assert dialog.default_value == "Основной"
    dialog.accept("Агрессивный")                            # текст для prompt

page.once("dialog", answer)
page.get_by_test_id("prompt-button").click()
expect(page.get_by_test_id("portfolio-name")).to_have_text("Агрессивный")
```

| Свойство / метод | Что |
|---|---|
| `dialog.type` | `alert`, `confirm`, `prompt`, `beforeunload` |
| `dialog.message` | текст диалога |
| `dialog.default_value` | значение по умолчанию у `prompt` |
| `dialog.accept(text=None)` | «ОК» (для prompt — с текстом) |
| `dialog.dismiss()` | «Отмена» / закрыть |

Проверено на лаборатории: `alert` «Торги идут круглосуточно», `confirm` «Удалить всё избранное?»,
`prompt` с значением по умолчанию «Основной».

##### Ловушки

- **Обработчик обязан ответить.** Если обработчик есть, но не вызвал `accept`/`dismiss`, диалог висит,
  и действие (`click`) висит до таймаута. Обработчик, который только логирует, — ошибка.
- `page.on("dialog", ...)` действует **до конца** жизни страницы — следующий диалог в тесте попадёт в тот же
  обработчик. Для одного диалога — `page.once`. Снять — `page.remove_listener("dialog", handler)`.
- Проверки (`assert`) внутри обработчика выполняются в обработчике событий: упавший `assert` может не уронить
  тест сразу и превратиться в непонятный таймаут. Надёжнее **сохранить** данные диалога и проверить их
  в теле теста:

```python
dialogs: list[tuple[str, str]] = []
page.once("dialog", lambda d: (dialogs.append((d.type, d.message)), d.accept()))
page.get_by_test_id("alert-button").click()
assert dialogs == [("alert", "Торги идут круглосуточно")]
```

- `beforeunload` («Уйти со страницы? Изменения не сохранятся») появляется при `page.close(run_before_unload=True)`
  или навигации; по умолчанию `page.close()` его не вызывает.

---

#### 2. Загрузка файлов

##### set_input_files

```python
upload = page.get_by_test_id("import-input")

upload.set_input_files("tests/ui/data/trades.csv")                    # путь
upload.set_input_files([path1, path2])                                 # несколько (если input multiple)
upload.set_input_files({"name": "bad.csv", "mimeType": "text/csv",     # из памяти, без файла на диске
                        "buffer": b"a,b\n1,2\n"})
upload.set_input_files([])                                             # очистить выбор
```

Проверено на лаборатории:
- CSV с двумя строками → «Импортировано строк: 2 (файлов: 1)»;
- неверные колонки из буфера → «Ошибка: Ожидались колонки: …»;
- пустой список → «Файлы не выбраны».

`set_input_files` работает с `<input type="file">` **напрямую** — системное окно выбора файла не открывается
(его автотест и не смог бы нажать). Input может быть скрытым (кастомная кнопка «Загрузить» поверх) — всё равно
вызывай на input.

##### file chooser — когда input не найти

Если кнопка создаёт input динамически или его не достать локатором:

```python
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="Загрузить аватар").click()
chooser = fc_info.value
chooser.is_multiple()                    # можно ли несколько (проверено: аватар — False)
chooser.set_files("avatar.png")
```

##### Drag & drop файла в зону загрузки

Зоны «перетащите файл сюда» слушают событие `drop` с `DataTransfer`. Обычно у них есть скрытый input — используй
его. Если нет — `dispatch_event("drop", {"dataTransfer": data_transfer})`, где `data_transfer` создают через
`page.evaluate_handle(...)`. Это редкий случай, достаточно знать, что так можно.

---

#### 3. Скачивание файлов

```python
with page.expect_download() as download_info:
    page.get_by_test_id("export-button").click()
download = download_info.value

download.suggested_filename                         # имя, которое предлагает сайт: quotes-2026-10-10.csv
path = tmp_path / download.suggested_filename
download.save_as(path)                              # сохранить, пока context жив
rows = path.read_text(encoding="utf-8").splitlines()
assert rows[0] == "ticker,price,change"
```

Проверено: экспорт — `quotes-<дата>.csv`, 21 строка (заголовок + 20 котировок).

- скачанный файл лежит во временной папке и **удаляется при закрытии context** — сохраняй через `save_as`;
- `download.path()` — путь к временному файлу (ждёт завершения скачивания);
- `download.failure()` — `None`, если скачалось;
- имя файла с датой — тест не должен зависеть от «сегодня» (U4.4, U6.2): проверяй шаблон
  `re.fullmatch(r"quotes-\d{4}-\d{2}-\d{2}\.csv", name)` или зафиксируй время `page.clock`.

##### Что проверять в скачанном файле

- формат: заголовки, разделитель, кодировка;
- содержимое **совпадает с тем, что на экране** (или в API) — это главное;
- для XLSX/PDF — библиотеки чтения (`openpyxl`, `pypdf`), проверка ключевых значений, а не байт в байт.

---

#### 4. Файлы для тестов

| Нужно | Как |
|---|---|
| CSV / JSON | собрать в тесте (`csv`, `json`) в `tmp_path` или буфер в памяти |
| картинка | `page.screenshot(path=...)`, Pillow, или маленький PNG в `tests/ui/data/` |
| большой файл (проверка лимита) | `path.write_bytes(os.urandom(2 * 1024 * 1024))` |
| файл с «плохим» именем | `"отчёт 2030 (копия).csv"`, очень длинное, без расширения |
| неверный формат | `.exe` вместо `.csv`, CSV без заголовка, пустой файл |

Граничные кейсы загрузки (U5.2 + тест-дизайн F2): размер на границе лимита, 0 байт, неверный тип, несколько файлов,
повторная загрузка того же файла, отмена выбора.

---

#### Собес: вопросы и ответы

**1. Как работать с alert / confirm / prompt в Playwright?**
> Подписаться на событие `dialog` до действия — `page.once` для одного диалога — и в обработчике вызвать
> `accept` или `dismiss`, для prompt — `accept(text)`. Без обработчика Playwright сам закрывает диалог через
> dismiss, поэтому «подтверждение» без обработчика на самом деле проверит отмену. Обработчик обязан ответить,
> иначе действие повиснет. Данные диалога сохраняю и проверяю в теле теста.

**2. Как протестировать загрузку файла?**
> `set_input_files` на `input type=file` — путь, список или файл из памяти с именем, типом и байтами; пустой
> список очищает. Системное окно не открывается. Если input не достать — `expect_file_chooser` вокруг клика.
> Проверяю результат в UI и граничные случаи: размер, тип, пустой файл, несколько файлов.

**3. Как протестировать скачивание файла?**
> `expect_download` вокруг клика, `save_as` в `tmp_path` — пока context жив, потом временный файл удалится.
> Проверяю имя (шаблоном, если в нём дата) и содержимое: формат и совпадение с данными на экране или в API.

**4. Чем нативный диалог отличается от модального окна?**
> Нативный — окно браузера, блокирует JS страницы; в DOM его нет, работаю через событие `dialog`.
> Модальное окно — обычный HTML-элемент с ролью dialog; с ним работаю локаторами и компонентом (U4.2).

### Задания — `tests/ui/test_u3_02_dialogs_files.py`

```text
U3. Урок 2 — диалоги браузера, загрузка и скачивание файлов.

Теория: practice/u3_02_dialogs_files.md
Страница: /app/lab.html (блоки «Диалоги», «Импорт и экспорт»).
Запуск:
    uv run pytest tests/ui/test_u3_02_dialogs_files.py -v

Задача 1. Компоненты в LabPage: DialogsPanel (кнопки, portfolio_name, result), FilesPanel
    (import_input, import_status, import_rows, export_button, avatar_input, avatar_preview).
    Хелпер dialog_answer(page, action="accept", text=None) -> list (собирает type/message/default_value).

Задача 2. confirm.
    а) Без обработчика нажми «Очистить избранное» — что в результате? Почему? (Ответ — в теории; сначала
       объясни сам.)
    б) accept → «Избранное очищено», список избранного пуст (to_have_count(0)).
    в) dismiss → «Отменено», в избранном по-прежнему BTC, ETH, USDT.
    Проверь тип и текст диалога в теле теста, не внутри обработчика.

Задача 3. prompt — parametrize.
    ("Агрессивный" → имя «Агрессивный»), ("  Долгосрок  " → «Долгосрок» — пробелы обрезаны),
    ("" → «Имя не может быть пустым», имя прежнее), (отмена → «Переименование отменено»).
    Проверь default_value диалога.

Задача 4. Ловушка обработчика.
    Повесь page.on("dialog", lambda d: print(d.message)) — без accept/dismiss — и нажми «Инфо»
    с timeout=3000 у клика. Что произошло? Запиши в «Ответах». Тест-демонстрацию оставь с xfail(strict=True).

Задача 5. Импорт CSV.
    а) Файл из tmp_path с 3 сделками → «Импортировано строк: 3 (файлов: 1)», в таблице 3 строки с теми данными.
    б) Два файла сразу (2 + 1 строки) → 3 строки, «файлов: 2».
    в) parametrize негативов из памяти (без файлов на диске): неверный заголовок, side=HOLD, цена 0,
       пустой файл. Для каждого — какое сообщение? (Посмотри parseCsv в exchange/web/lab.js.)
    г) Файл 2 МБ → «файл больше 1 МБ». А ровно 1 МБ (1024*1024 байт)? Граница — включительно или нет?
       Проверь и запиши — это пример граничного значения из F2.
    д) set_input_files([]) → «Файлы не выбраны», таблица пуста.

Задача 6. Аватар через file chooser.
    expect_file_chooser вокруг клика по input аватара; is_multiple() == False; загрузи PNG
    (сгенерируй page.screenshot в tmp_path). Превью видно, alt == имя файла.

Задача 7. Экспорт.
    Скачай CSV: имя по шаблону quotes-YYYY-MM-DD.csv; заголовок ticker,price,change; строк 20;
    значения совпадают с таблицей котировок на экране (колонки через Table из U4.2).
    Затем: отсортируй таблицу по цене и скачай снова — порядок строк в файле изменился? Ожидаемо ли это?

Задача 8. Имя файла с датой.
    page.clock.install(time="2030-01-15T10:00:00Z") до goto → экспорт называется quotes-2030-01-15.csv.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как работать с alert / confirm / prompt в Playwright?
    2. Как протестировать загрузку файла?
    3. Как протестировать скачивание файла?
    4. Чем нативный диалог отличается от модального окна?
```

<a id="u3-3"></a>

## U3.3 Мышь, клавиатура, скролл и бесконечные списки

*Теория: `practice/u3_03_mouse_keyboard_scroll.md`*

Задания: `tests/ui/test_u3_03_mouse_keyboard_scroll.py`. Страница: лаборатория `/app/lab.html`
(меню «Ещё», «Избранное», «Котировки», «Лента сделок»).

План: hover и меню по наведению; drag & drop (высокоуровнево и вручную); клавиатура — `press`,
`press_sequentially`, `keyboard`, сочетания клавиш; поиск с debounce; скролл; бесконечная лента —
как дочитать до конца без `sleep`; клик с модификаторами, двойной и правый клик.

---

#### 1. Hover и меню

Меню «Ещё» на лаборатории открывается **по наведению** (`mouseenter`) и закрывается при уходе мыши.

```python
page.get_by_role("button", name="Ещё ▾").hover()
expect(page.get_by_role("menuitem").first).to_be_visible()
page.get_by_role("menuitem").filter(has_text="Кабинет").click()
```

Проверено. Детали:
- `hover()` двигает мышь к центру элемента — с теми же проверками actionability, что `click` (U1.4);
- после `hover` нельзя «увести мышь» случайным действием: `click` по элементу **вне** меню закроет меню;
  клик по пункту меню — нормально, мышь переходит внутрь меню;
- тултипы (`title`, кастомные подсказки) — `hover`, потом `expect(tooltip).to_be_visible()`;
- на тач-устройствах hover нет — меню по наведению на мобильном часто сломано (U6.3, эмуляция).

---

#### 2. Drag & drop

```python
items = page.get_by_test_id("watch-item")
items.filter(has_text="BTC").drag_to(items.filter(has_text="USDT"))
expect(items).to_have_text(["ETH", "USDT", "BTC"])
```

Проверено: лаборатория использует HTML5 Drag and Drop (`draggable`, `dragstart`/`drop`), и `drag_to`
с ним работает.

Вручную — когда нужна точная траектория (слайдеры, канвас, сортировка по позиции):

```python
box = source.bounding_box()
page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
page.mouse.down()
page.mouse.move(target_x, target_y, steps=10)      # steps — промежуточные события mousemove
page.mouse.up()
```

Библиотеки drag-and-drop на JS (SortableJS, react-dnd) иногда реагируют только на «живое» движение мыши —
тогда ручной вариант со `steps` работает, а `drag_to` нет. Проверяй **результат** (порядок элементов),
а не события.

---

#### 3. Клавиатура

| Метод | Что делает | Когда |
|---|---|---|
| `locator.fill("text")` | заменить значение целиком, одним событием `input` | почти всегда |
| `locator.press_sequentially("abc", delay=50)` | печатать по символу: `keydown`/`keypress`/`input`/`keyup` | автодополнение, маски ввода, обработчики на каждую клавишу |
| `locator.press("Enter")` | нажать клавишу на элементе (фокус на нём) | Enter, Escape, Tab, стрелки |
| `locator.clear()` | очистить поле | |
| `page.keyboard.press("Control+K")` | клавиша/сочетание на странице (туда, где фокус) | глобальные горячие клавиши |
| `page.keyboard.type("bt")` | печатать в элемент с фокусом | после фокуса горячей клавишей |
| `page.keyboard.down("Shift")` / `up` | зажать модификатор | выделение, мультивыбор |

Проверено на лаборатории:
- поле тикера: `fill("sol")` + `press("Enter")` → SOL в избранном; `press("Escape")` очищает поле;
- `page.keyboard.press("Control+k")` → фокус в поиске котировок (`to_be_focused()`), затем
  `keyboard.type("bt")` → одна строка (BTC).

Названия клавиш: `Enter`, `Escape`, `Tab`, `Backspace`, `Delete`, `ArrowDown`, `Home`, `PageDown`, `F5`, `a`–`z`.
Модификаторы: `Shift`, `Control`, `Alt`, `Meta` (⌘ на macOS) и `ControlOrMeta` — Control на Windows/Linux и ⌘ на macOS,
для сочетаний вроде «копировать».

Доступность с клавиатуры: можно ли пройти форму только `Tab` + `Enter`? Это и тест UX, и тест доступности (U8).

---

#### 4. Поиск с debounce

Поиск котировок применяется через **300 мс после последнего ввода** (`setTimeout`), как в настоящих поисках.

```python
search.fill("bt")
expect(rows).to_have_count(1)                     # expect подождёт — debounce не проблема
```

`sleep(0.3)` не нужен (U2.1). Ловушка — проверка отсутствия (U2.1, ловушка 1):

```python
search.fill("zzz")
expect(rows).to_have_count(0)        # может пройти ДО применения фильтра? — нет: до фильтра строк 20
```

Здесь всё в порядке: до фильтра строк 20, проверка дождётся 0. Но `expect(rows).to_have_count(20)` после
`fill("")` пройдёт мгновенно, если фильтр ещё не применился, — проверка ничего не докажет. Проверяй
**изменение**, а не исходное состояние. Детерминированно — `page.clock` (U6.2): `run_for(300)`.

---

#### 5. Скролл

Playwright **сам** прокручивает к элементу перед действием (`scrolling into view if needed`, U2.3).
Явный скролл нужен, когда скролл — это и есть сценарий:

```python
locator.scroll_into_view_if_needed()
page.mouse.wheel(0, 500)                           # колесо — по элементу под мышью
page.keyboard.press("End")                         # в фокусированном контейнере
locator.evaluate("el => el.scrollTop = el.scrollHeight")   # контейнер до конца
expect(locator).to_be_in_viewport()                # элемент в видимой области
```

---

#### 6. Бесконечная лента

«Лента сделок» показывает 20 записей и догружает ещё 20, когда прокрутили до низа контейнера (с задержкой
400 мс), всего 200. Задача: дочитать до конца **без sleep** и без «покрутить 10 раз на всякий случай».

```python
items = page.get_by_test_id("feed-item")
count = page.get_by_test_id("feed-count")

expect(items).to_have_count(20)
while "Это все сделки" not in (count.text_content() or ""):
    loaded = items.count()                         # сколько есть сейчас (для сравнения, не для проверки)
    items.last.scroll_into_view_if_needed()        # прокрутить контейнер к последней записи
    expect(items).not_to_have_count(loaded)        # дождаться догрузки
expect(items).to_have_count(200)
```

Проверено: лента дочитывается до «Загружено: 200. Это все сделки».

Принципы:
- **условие окончания** — признак от приложения («это всё», пустой ответ API), а не число итераций;
- после каждой прокрутки — **ждать изменения** (`not_to_have_count(loaded)`), иначе следующий скролл
  уйдёт до загрузки;
- защита от вечного цикла — максимум итераций с понятной ошибкой;
- если нужен конкретный элемент («сделка #150»), не обязательно грузить всё: крути, пока он не появится.

Виртуализированные списки (react-window): в DOM только видимые строки, старые **удаляются**. Счёт
по количеству в DOM не работает — проверяй по содержимому видимых строк и по признаку конца.

---

#### 7. Прочие действия мыши

```python
loc.dblclick()
loc.click(button="right")                          # контекстное меню
loc.click(modifiers=["Shift"])                     # выделение диапазона
loc.click(modifiers=["ControlOrMeta"])             # мультивыбор / «открыть в новой вкладке»
loc.click(position={"x": 5, "y": 5})               # точка внутри элемента
loc.tap()                                          # тач (context с has_touch=True)
```

---

#### Собес: вопросы и ответы

**1. Как тестировать меню по наведению и drag & drop?**
> Меню — `hover` на триггер, `expect` на пункты, клик по пункту. Drag & drop — `drag_to` от источника к цели;
> если библиотека реагирует только на живое движение — вручную через `mouse.move/down/up` со `steps`.
> Проверяю результат — порядок элементов, а не события.

**2. Чем `fill` отличается от `press_sequentially`?**
> `fill` ставит значение сразу, одним событием input — быстро, подходит почти всегда. `press_sequentially`
> печатает посимвольно со всеми событиями клавиатуры — для автодополнения, масок, обработчиков на каждую
> клавишу. `press` — одна клавиша или сочетание.

**3. Как протестировать бесконечную прокрутку?**
> Цикл: прокрутить к последнему элементу, дождаться, что их стало больше, — пока приложение не покажет
> признак конца. Условие выхода — сигнал приложения, а не число итераций; без sleep; с защитой от вечного
> цикла. Для виртуализированных списков считаю не DOM-элементы, а содержимое и признак конца.

**4. Как тестировать поиск с debounce?**
> Просто `expect` на результат — он подождёт. Не проверяю «исходное» состояние сразу после ввода: оно верно
> и до применения фильтра. Детерминированно — `page.clock.run_for` на время debounce.

**5. Как проверить горячие клавиши?**
> `page.keyboard.press("ControlOrMeta+K")` — сочетание отправляется туда, где фокус; потом проверяю результат —
> например, `to_be_focused` у поля поиска. `ControlOrMeta` — чтобы тест работал и на macOS, и на Linux в CI.

### Задания — `tests/ui/test_u3_03_mouse_keyboard_scroll.py`

```text
U3. Урок 3 — мышь, клавиатура, скролл и бесконечные списки.

Теория: practice/u3_03_mouse_keyboard_scroll.md
Страница: /app/lab.html.
Запуск:
    uv run pytest tests/ui/test_u3_03_mouse_keyboard_scroll.py -v

Задача 1. Компоненты в LabPage: MoreMenu (open() — hover, item(name)), Watchlist (items, input, add(ticker)),
    QuotesTable (наследник Table из U4.2: search, rows, count, sort_by(column)), Feed (items, count, load_all()).

Задача 2. Меню по наведению.
    а) hover → три пункта меню видны; увести мышь (hover на заголовок «Лаборатория») → пункты скрыты.
    б) Пункт «Кабинет» ведёт на /app/index.html (to_have_url), пункт «API (Swagger)» — новая вкладка /docs.

Задача 3. Drag & drop.
    parametrize: (BTC → USDT ⇒ ETH, USDT, BTC), (USDT → BTC ⇒ USDT, BTC, ETH), (ETH → ETH ⇒ без изменений).
    Тост показывает новый порядок — проверь и его. Сделай один кейс вручную через mouse.move/down/up со steps.

Задача 4. Клавиатура в избранном.
    а) «sol» + Enter → SOL в конце, поле пустое; повторно «SOL» + Enter → тост «SOL уже в избранном», дубля нет.
    б) press_sequentially("dot") + Escape → поле пустое, ничего не добавилось.
    в) Пустое поле + Enter → ничего не произошло. Как проверить «ничего не произошло» корректно (U2.1)?

Задача 5. Горячая клавиша.
    ControlOrMeta+K → фокус в поиске (to_be_focused); keyboard.type("et") → строки только с «ET» в тикере.
    Сколько их? (Посчитай по TICKERS в exchange/web/lab.js, не подглядывая в UI.)

Задача 6. Поиск с debounce.
    а) fill("bt") → 1 строка; fill("") → снова 20, и «Показано: 20 из 20».
    б) Покажи ловушку: после fill("") проверка to_have_count(20) могла пройти до применения фильтра?
       Как сделать проверку, которая точно доказывает, что фильтр сбросился (подсказка: проверь сначала
       промежуточное состояние или используй page.clock)?

Задача 7. Бесконечная лента.
    Feed.load_all(max_loops=20): цикл из теории с защитой от вечного цикла (понятная ошибка).
    Проверь: 200 записей, последняя — «#200 …», текст «Это все сделки».
    Отдельно: найти запись «#77» — грузить только до неё (меньше итераций, чем load_all?).

Задача 8. Прочие действия мыши.
    Двойной клик по заголовку «Цена» в котировках — сколько раз сменилась сортировка (aria-sort у th)?
    Объясни. Клик с modifiers=["ControlOrMeta"] по ссылке «Открыть отчёт BTC» — что произошло?

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как тестировать меню по наведению и drag & drop?
    2. Чем fill отличается от press_sequentially?
    3. Как протестировать бесконечную прокрутку?
    4. Как тестировать поиск с debounce?
    5. Как проверить горячие клавиши?
```

<a id="u3-4"></a>

## U3.4 Shadow DOM, таблицы, cookies и localStorage; собес по модулю U3

*Теория: `practice/u3_04_shadow_tables_storage_interview.md`*

Задания: `tests/ui/test_u3_04_shadow_tables_storage.py`. Страница: лаборатория `/app/lab.html`
(«Тикер (веб-компонент)», «Котировки», баннер cookies).

План: Shadow DOM — что это и как Playwright с ним работает (проверено); динамические таблицы —
сортировка и фильтр, как проверить правильно; cookies и localStorage — читать, подкладывать, чистить;
история про атрибут `hidden`; шпаргалка и вопросы собеса по модулю U3; лайвкодинг таблицы.

---

#### 1. Shadow DOM

Веб-компонент `<price-ticker>` прячет свою разметку в **shadow root** — отдельное поддерево, изолированное
от стилей и селекторов страницы. Так устроены дизайн-системы (Lit, Stencil), Salesforce, многие виджеты.

##### Playwright пробивает открытый shadow DOM сам

```python
page.get_by_test_id("ticker-price")                   # внутри shadow root — находится
page.get_by_role("button", name="Следить")            # тоже
page.locator("price-ticker button")                   # CSS — тоже
page.locator("xpath=//price-ticker//button")          # XPath — НЕТ
```

Проверено: роль, текст, test-id и CSS находят элементы внутри shadow root; XPath — 0 элементов.
XPath по стандарту не ходит в shadow DOM — ещё одна причина не использовать его (U1.2).

Selenium (до 4.x) требовал `shadow_root` руками — это частый вопрос «как работать с Shadow DOM».

##### Закрытый shadow root

`attachShadow({mode: "closed"})` — снаружи недоступен ни JS страницы, ни Playwright. Тестируют через то,
что компонент отдаёт наружу (атрибуты, события, видимый результат) или просят разработчиков `mode: "open"`
в тестовой сборке. На практике закрытые встречаются редко.

##### Разметка компонента: part и атрибуты

Компонент может отдавать части наружу (`part="price"`) и принимать данные атрибутами (`price="65000"`).
Проверка атрибута хоста: `expect(page.get_by_test_id("ticker")).to_have_attribute("symbol", "BTC-USDT")`.

---

#### 2. Динамические таблицы: сортировка и фильтр

Таблица котировок: 20 строк, сортировка по клику на заголовок (повторный клик — обратный порядок),
поиск с debounce (U3.3), счётчик «Показано: N из 20», атрибут `aria-sort` на `th`.

##### Как проверить сортировку

```python
table.sort_by("Цена")
prices = table.column("Цена")                                  # Table из U4.2
expect(prices).to_have_count(20)                               # 1. дождаться устойчивого состояния
values = [Decimal(v) for v in prices.all_text_contents()]      # 2. прочитать
assert values == sorted(values)                                # 3. сравнить с отсортированной копией
expect(table.header("Цена")).to_have_attribute("aria-sort", "ascending")
```

Правила (U2.2):
- сравнивать **как числа** (`Decimal`), не как строки: `"100" < "20"`;
- проверять **весь** столбец, а не первую и последнюю строку;
- сортировка **по другой колонке** не должна терять строки: множество строк до и после — одинаковое;
- стабильность: при равных значениях порядок сохраняется? (у котировок цены уникальны, но так спрашивают);
- состояние для пользователя: стрелка/`aria-sort` — тоже часть требования и доступности.

##### Ожидание после клика

Сортировка на клиенте мгновенная, но **не всегда**: серверная сортировка — запрос и перерисовка. Чтение сразу после
клика — гонка (U2.1). Безопасно: дождаться признака (атрибут `aria-sort`, `expect_response`) или проверить первую
строку через `expect`, потом читать весь столбец.

##### Фильтр

```python
search.fill("bt")
expect(rows).to_have_count(1)
expect(table.column("Тикер")).to_have_text(["BTC"])
expect(count).to_have_text("Показано: 1 из 20")
```

Фильтр + сортировка вместе: отсортировать, отфильтровать — порядок сохранился? Сбросить фильтр — сортировка осталась?

##### Strict mode в таблицах лаборатории

`page.get_by_role("columnheader", name="Цена")` находит **два** заголовка: в котировках и в таблице импорта.
Сужай до таблицы: `quotes.get_by_role("columnheader", name="Цена")` (U2.2, U4.2).

---

#### 3. Cookies и localStorage

##### Cookies

```python
context.cookies()                                         # все cookies context
context.cookies("http://localhost:8080")                   # для URL
context.add_cookies([{"name": "consent", "value": "1", "url": base_url}])
context.clear_cookies()                                    # все; clear_cookies(name="consent") — точечно
```

Проверено на лаборатории:
- «Принять» в баннере → cookie `consent=1`;
- `add_cookies` **до** `goto` → баннер не показывается — так пропускают cookie-баннеры, онбординги, A/B-тесты;
- `clear_cookies()` + `reload` → баннер снова виден.

##### localStorage / sessionStorage

API у context нет — через страницу или storage_state:

```python
page.evaluate("localStorage.getItem('token')")
page.evaluate("([k, v]) => localStorage.setItem(k, v)", ["k", "v"])
page.evaluate("localStorage.clear()")
context.storage_state()["origins"]                       # [{'origin': 'http://localhost:8080', 'localStorage': [...]}]
```

Подложить **до** загрузки — `storage_state` в `new_context` (U5.1). sessionStorage в storage_state не сохраняется.

##### Зачем в тестах

- пропустить баннеры и онбординг (cookie / флаг в localStorage);
- проверить, что приложение **сохраняет** настройки (тема, выбранная пара) — записалось и применилось после reload;
- проверить выход: токен удалён из хранилища (U1.4);
- фиче-флаги и A/B-группа, если их выбирает cookie.

---

#### 4. История: `hidden` и CSS

При подготовке урока баннер cookies на лаборатории был виден **всегда**, хотя у него стоял атрибут `hidden`.
Причина: в CSS у `.banner` было `display: flex`, а правило автора страницы сильнее встроенного правила браузера
`[hidden] { display: none }`. Исправлено: `.banner[hidden] { display: none; }`.

Что из этого для тестировщика:
- `to_be_hidden()` / `to_be_visible()` проверяют **реальную видимость** (размер, `display`, `visibility`), а не атрибут —
  поэтому тест и поймал баг: «expected hidden, actual visible», хотя в логе видно `<div hidden="" ...>`;
- проверка атрибута (`to_have_attribute("hidden", "")`) этот баг **пропустила** бы — проверяй то, что видит пользователь.

---

#### 5. Шпаргалка по модулю U3

- **Вкладки и окна (U3.1)**: `context.expect_page()` / `page.expect_popup()` вокруг действия; у каждой вкладки свой
  Page; вкладки делят context. iframe — `frame_locator` или `content_frame`; Frame — для evaluate; postMessage —
  проверяй результат на странице.
- **Диалоги и файлы (U3.2)**: без обработчика — авто-dismiss; обработчик обязан ответить; `page.once`; данные —
  в тело теста. `set_input_files` (путь, буфер, список, `[]`), `expect_file_chooser`. `expect_download` + `save_as`;
  имя с датой — шаблон или clock.
- **Мышь и клавиатура (U3.3)**: hover-меню; `drag_to` / ручной drag; `fill` vs `press_sequentially` vs `press`;
  `ControlOrMeta`; debounce — expect, не sleep; бесконечная лента — до признака конца, ждать прироста.
- **Shadow DOM, таблицы, хранилища (U3.4)**: открытый shadow — локаторы пробивают, XPath нет; сортировка — весь столбец
  в Decimal + `aria-sort`; cookies — `add_cookies` до goto, `clear_cookies`; localStorage — evaluate / storage_state.

---

#### Собес: вопросы и ответы

Плюс вопросы U3.1 (4), U3.2 (4), U3.3 (5).

**1. Как работать с Shadow DOM?**
> Playwright пробивает открытый shadow DOM сам: роли, текст, test-id и CSS находят элементы внутри. XPath — нет.
> Закрытый shadow root недоступен: тестирую через внешнее поведение компонента или прошу open-режим в тестовой
> сборке.

**2. Как проверить сортировку таблицы?**
> Дождаться устойчивого состояния, прочитать весь столбец, привести к числам или датам и сравнить с отсортированной
> копией. Проверить обратный порядок, что строки не потерялись, индикатор сортировки (`aria-sort`). Не сравнивать
> числа как строки и не ограничиваться первой строкой.

**3. Как пропустить cookie-баннер в тестах?**
> Подложить cookie согласия через `context.add_cookies` до загрузки страницы (или флаг в localStorage через
> storage_state). Отдельный тест — на сам баннер: появляется без cookie, кнопка ставит cookie, после reload не
> появляется.

**4. Как тестировать iframe, новую вкладку, загрузку и скачивание файла?** (вопрос из программы)
> iframe — `frame_locator` или `content_frame`. Вкладка — `context.expect_page` или `expect_popup` вокруг клика.
> Загрузка — `set_input_files` на input, без системного окна. Скачивание — `expect_download`, `save_as`, проверка
> имени и содержимого против экрана.

**5. Атрибут hidden есть, а элемент виден — как такое бывает?**
> CSS автора с `display` перебивает встроенное правило `[hidden]`. Поэтому проверяю видимость через
> `to_be_visible`/`to_be_hidden` — они смотрят на реальную отрисовку, а не на атрибут.

### Задания — `tests/ui/test_u3_04_shadow_tables_storage.py`

```text
U3. Урок 4 — Shadow DOM, таблицы, cookies и localStorage; собес по модулю U3.

Теория: practice/u3_04_shadow_tables_storage_interview.md
Страница: /app/lab.html (стенд пересобрать: docker compose up -d --build).
Запуск:
    uv run pytest tests/ui/test_u3_04_shadow_tables_storage.py -v

Задача 1. Shadow DOM.
    а) Компонент PriceTicker (root — хост <price-ticker>): price, follow_button.
       Цена 65000, атрибут symbol хоста — BTC-USDT.
    б) «Следить» → кнопка «Не следить» и тост «Следим за BTC-USDT»; ещё клик → «Следить», тост «Слежение выключено».
    в) Покажи, что XPath не видит кнопку внутри shadow root (to_have_count(0)), а CSS и get_by_role — видят.

Задача 2. Сортировка котировок.
    QuotesTable (U3.3): sort_by(column), header(column), column(name).
    parametrize по колонкам «Тикер», «Цена», «Изменение, %»:
        клик → по возрастанию (сравни с sorted, числа — Decimal), aria-sort ascending;
        ещё клик → по убыванию, aria-sort descending;
        множество строк до и после сортировки одинаковое.

Задача 3. Сортировка + фильтр.
    Сортировка по цене ↓, затем поиск «A» → строки по-прежнему по убыванию цены, счётчик «Показано: N из 20».
    Сбрось поиск → снова 20 строк, сортировка сохранилась.

Задача 4. Strict mode в таблицах.
    page.get_by_role("columnheader", name="Цена") — сколько? Почему? Исправь через QuotesTable.

Задача 5. Cookies.
    а) Новый context без cookies → баннер виден; «Принять» → cookie consent=1 (проверь context.cookies()),
       баннер скрыт; reload → не появился.
    б) add_cookies до goto → баннера нет с самого начала.
    в) clear_cookies(name="consent") + reload → баннер снова есть.
    г) Фикстура lab_page по умолчанию без баннера (через add_cookies) — чтобы он не мешал другим тестам.

Задача 6. localStorage.
    В кабинете (/app/) после входа: token и email в localStorage; после «Выйти» — нет обоих.
    Запиши в localStorage мусорный token перед reload — что покажет кабинет? (Вспомни U5.1.)

Задача 7. hidden против видимости.
    Напиши проверку, которая поймала бы старый баг баннера (раздел 4 теории): баннер с атрибутом hidden
    должен быть невидим. И проверку через to_have_attribute("hidden", "") — объясни, почему она слабее.

Задача 8. Лайвкодинг (из программы) — 20 минут.
    «Таблица котировок: фильтр и сортировка». Без подглядывания в свои решения задач 2–3:
    поиск «O» → только тикеры с O; сортировка по изменению ↑; первая строка — тикер с минимальным изменением
    среди отфильтрованных; сброс → 20 строк. Засеки время, запиши в «Ответы».

Задача 9. Устный собес по модулю U3.
    10 вопросов из «Собес» U3.1–U3.4 (18 вопросов), вслух. Номера, где «поплыл», — в «Ответы».

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как работать с Shadow DOM?
    2. Как проверить сортировку таблицы?
    3. Как пропустить cookie-баннер в тестах?
    4. Как тестировать iframe, новую вкладку, загрузку и скачивание файла?
    5. Атрибут hidden есть, а элемент виден — как такое бывает?
```


---

# U4. Page Object и архитектура

<a id="u4-1"></a>

## U4.1 Page Object

*Теория: `practice/u4_01_page_object.md`*

Задания: `tests/ui/test_u4_01_page_object.py`, код — в `ui_framework/pages/`.
Ревью: `practice/u4_01_review_me.py`.

План: какую проблему решает Page Object; граница «страница — как, тест — что»; как устроить
PO на нашем стенде (SPA: один URL, два экрана); что возвращают методы; можно ли проверки внутри
PO; базовая страница; антипаттерны; как PO выглядит на собесе.

Модуль U4 целиком: U4.1 Page Object → U4.2 компоненты → U4.3 фикстуры страниц и конфиг окружений →
U4.4 утилиты, Allure-шаги и структура проекта → U4.5 Screenplay, собес и каркас фреймворка.

---

#### 1. Проблема

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

#### 2. Идея

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
def test_deposit(auth_page, user_email):
    dashboard = auth_page.open().register(user_email, PASSWORD)
    dashboard.deposit("USDT", "1000")
    expect(dashboard.balance_available("USDT")).to_have_text("1000")
```

Поменялась кнопка — правим одну строку в `DashboardPage`. Тест читается как сценарий.

---

#### 3. PO на нашем стенде

Стенд — SPA: всё живёт на `/app/`, но экранов два — форма входа и кабинет. PO — **на экран**,
а не на URL:

```
ui_framework/
  pages/
    base_page.py         # BasePage: page, open(path), общий тост
    auth_page.py         # AuthPage: вход и регистрация
    dashboard_page.py    # DashboardPage: шапка, балансы, пополнение, ордера
```

##### BasePage

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

##### Локаторы в `__init__`

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

##### Действия и переходы

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
Тест пишет цепочкой: `auth_page.open().login(...).deposit(...)`.

Позитивный и негативный вход — разные методы: `login` обещает кабинет и ждёт его,
`login_expecting_error` остаётся на форме. Один метод `login(..., expect_success=True)` с ветвлением
внутри читается хуже и прячет, что ожидает тест.

##### Что возвращать для проверок: Locator, а не строку

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

#### 4. Проверки внутри Page Object

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

#### 5. Как выглядит DashboardPage

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

##### Циклический импорт

`AuthPage.login()` возвращает `DashboardPage`, `DashboardPage.logout()` — `AuthPage`.
Модули импортируют друг друга. Решения:
- импорт внутри метода: `from ui_framework.pages.dashboard_page import DashboardPage`;
- аннотация строкой (`-> "DashboardPage"`) + `from __future__ import annotations`
  + `if TYPE_CHECKING:` для импорта только для подсказок типов.

---

#### 6. Фикстуры для страниц (кратко, подробно — U4.3)

```python
@pytest.fixture
def auth_page(page: Page) -> AuthPage:
    return AuthPage(page)

@pytest.fixture
def dashboard(auth_page: AuthPage, user_email: str) -> DashboardPage:
    return auth_page.open().register(user_email, PASSWORD)
```

Тест просит то, что ему нужно: `dashboard` — уже залогиненный кабинет.

---

#### 7. Антипаттерны

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

---

#### 8. Почему PO, а не просто функции-хелперы

| | Функции (`helpers.py`) | Page Object |
|---|---|---|
| Где локаторы | внутри каждой функции, дублируются | в одном месте на экран |
| Навигация | неявная | метод возвращает следующий экран |
| Автодополнение в IDE | список функций модуля | `dashboard.` → всё, что можно на экране |
| Масштаб | хорошо для 10–20 тестов | для сотен тестов и нескольких экранов |

Для маленького набора тестов хелперов хватает. Это нормальный ответ на собесе: «PO — не догма,
выбираю по размеру проекта».

---

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u4_01_page_object.py`

```text
U4. Урок 1 — Page Object.

Теория: practice/u4_01_page_object.md
Код страниц пишешь в ui_framework/pages/ (файлы-заготовки уже есть), тесты — здесь.
Запуск:
    uv run pytest tests/ui/test_u4_01_page_object.py -v

Правила:
    - в тестах НЕТ page.get_by_* / page.locator — только методы и локаторы из PO;
    - в PO нет бизнес-проверок (раздел 4 теории), разрешены wait_loaded и проверка ответа своего действия;
    - для проверок PO отдаёт Locator, тест делает expect;
    - tests/ui/helpers.py в этом уроке не используем — всё через PO.

Задача 1. BasePage (ui_framework/pages/base_page.py).
    Атрибут класса path, __init__(page) с локатором toast, метод open() -> self.

Задача 2. AuthPage (ui_framework/pages/auth_page.py).
    path = "/app/". Локаторы: root, email, password, login_button, register_button, error.
    Методы: wait_loaded() -> self; fill_credentials(email, password);
    register(email, password) -> DashboardPage; login(email, password) -> DashboardPage;
    login_expecting_error(email, password) -> AuthPage.
    Реши, как избежать циклического импорта с DashboardPage (раздел 5 теории).

Задача 3. DashboardPage (ui_framework/pages/dashboard_page.py).
    Локаторы: root, user_email, logout_button, order_rows. Методы:
        wait_loaded() -> self; logout() -> AuthPage;
        deposit(asset, amount) -> dict            — ждёт ответ POST /balances/deposit, падает не на 2xx;
        deposit_expecting_error(asset, amount)    — без проверки ответа, для негативных тестов;
        place_order(side, price, quantity, symbol="ETH-USDT") -> dict   — то же для POST /orders;
        balance_available(asset) -> Locator; balance_locked(asset) -> Locator;
        order_row(order_id) -> Locator; order_status(order_id) -> Locator; cancel_order(order_id).

Задача 4. Фикстуры (tests/ui/conftest.py).
    auth_page — AuthPage(page); dashboard — зарегистрированный пользователь, DashboardPage.

Задача 5. Тесты через PO.
    а) Регистрация → в шапке email; выход → видна форма входа.
    б) Вход: верные данные → кабинет; parametrize (неверный пароль, несуществующий email) →
       ошибка "Invalid email or password", кабинет скрыт.
    в) Пополнение USDT 1000 → доступно 1000, заблокировано 0.
    г) Неверные суммы пополнения ("0", "-5", "abc") через deposit_expecting_error:
       тост не «Баланс USDT пополнен», доступно 0. (Вспомни U2.1: дождись, что тост сменился.)
    д) Ордер BUY 100 x 1 → заблокировано 100, доступно 900; отмена → CANCELED, 1000 и 0.
       id ордера — из ответа place_order.

Задача 6. Ревью practice/u4_01_review_me.py — минимум 10 проблем, ответы в том файле.

Задача 7. Устойчивость к изменениям.
    Представь: кнопку «Пополнить» переименовали в «Зачислить».
    а) Сколько мест надо поправить в твоём коде? А в тестах U1.4 до PO?
    б) Временно поменяй локатор кнопки в DashboardPage на name="Зачислить", запусти тесты:
       как выглядит падение и по нему понятно, где чинить? Верни обратно.
    Ответ — в «Ответах».

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое Page Object и зачем он нужен?
    2. Где граница между Page Object и тестом? Можно ли проверки внутри PO?
    3. Что возвращают методы PO?
    4. Где хранить локаторы? Почему их можно создавать в __init__?
    5. Как не превратить Page Object в свалку?
    6. PO или хелперы-функции?
    7. Как PO в Playwright отличается от PO в Selenium?
```

### Файл для ревью — `practice/u4_01_review_me.py`

```python
"""U4.1, задача 6 — ревью Page Object от «коллеги».

Код рабочий (почти), но на ревью его не пропустят. Найди минимум 10 проблем.
Для каждой: строка, что не так, как исправить. Ответы — внизу файла.
Подсказка: сверяйся с разделом 7 теории (антипаттерны) и с U2.1–U2.2.
"""

import time

from playwright.sync_api import Page, expect

EMAIL = "trader@test.com"
PASSWORD = "password123"


class ExchangePage:
    LOGIN_BUTTON = "[data-testid=login-button]"
    REGISTER_BUTTON = "text=Зарегистрироваться"
    DEPOSIT_BUTTON = "#deposit-form > button"

    def __init__(self, page: Page):
        self.page = page
        self.last_order_price = None

    def open(self):
        self.page.goto("http://localhost:8080/app/")
        self.page.wait_for_load_state("networkidle")

    def click_register_button(self):
        self.page.click(self.REGISTER_BUTTON)

    def login(self):
        self.page.fill("[data-testid=email-input]", EMAIL)
        self.page.fill("[data-testid=password-input]", PASSWORD)
        self.page.click(self.LOGIN_BUTTON)
        time.sleep(2)

    def deposit_and_check(self, asset, amount):
        self.page.select_option("[data-testid=deposit-asset]", asset)
        self.page.fill("[data-testid=deposit-amount]", amount)
        self.page.click(self.DEPOSIT_BUTTON)
        expect(self.page.locator(f"[data-asset={asset}] [data-testid=balance-available]")).to_have_text(amount)

    def get_balance(self, asset):
        return self.page.locator(f"[data-asset={asset}] [data-testid=balance-available]").text_content()

    def place_order(self, price, quantity):
        self.page.fill("[data-testid=order-price]", price)
        self.page.fill("[data-testid=order-quantity]", quantity)
        self.page.click("[data-testid=place-order-button]")
        self.last_order_price = price

    def cancel_last_order(self):
        self.page.locator("[data-testid=cancel-order]").first.click()

    def is_order_cancelled(self):
        return "CANCELED" in self.page.locator("[data-testid=order-status]").first.text_content()

    def logout(self):
        try:
            self.page.click("[data-testid=logout-button]", timeout=1000)
        except Exception:
            pass


def test_order_flow(page: Page):
    exchange = ExchangePage(page)
    exchange.open()
    exchange.login()
    exchange.deposit_and_check("USDT", "1000")
    exchange.place_order("100", "1")
    assert exchange.get_balance("USDT") == "900"
    exchange.cancel_last_order()
    assert exchange.is_order_cancelled()


# Ответы
"""
"""
```

<a id="u4-2"></a>

## U4.2 Компоненты

*Теория: `practice/u4_02_components.md`*

Задания: `tests/ui/test_u4_02_components.py`, код — в `ui_framework/components/`.

План: почему PO страницы разрастается и что такое компонент; корневой локатор и поиск
внутри него; композиция страницы из компонентов; компонент строки таблицы; общий компонент
таблицы и его наследники; тост и шапка как общие компоненты; модальное окно как паттерн;
фасад на странице — нужен ли; антипаттерны; собес.

---

#### 1. Зачем компоненты

После U4.1 `DashboardPage` знает всё: шапку, балансы, две формы, таблицу ордеров, тост.
Это уже 15+ методов, и растёт. В реальном приложении хуже:
- та же **таблица** (сортировка, фильтр, пагинация) есть на пяти страницах;
- **шапка** с пользователем и выходом — на всех страницах после входа;
- **тост** / уведомления — глобальные;
- **модалка подтверждения** — одна и та же разметка, разные тексты.

**Компонент** — класс для повторяющейся части экрана. Страница **собирается** из компонентов
(композиция), а не описывает всё сама.

```python
dashboard.deposit_form.deposit("USDT", "1000")
expect(dashboard.balances.available("USDT")).to_have_text("1000")
row = dashboard.orders.row(order_id)
expect(row.status).to_have_text("NEW")
row.cancel()
```

---

#### 2. Корневой локатор

Компонент получает **root** — локатор своего блока — и ищет всё **внутри** него:

```python
from playwright.sync_api import Locator


class BaseComponent:
    def __init__(self, root: Locator):
        self.root = root
        self.page = root.page          # если нужен доступ к странице (ответы сети)
```

```python
class DepositForm(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.asset = root.get_by_label("Актив")
        self.amount = root.get_by_placeholder("Сумма")
        self.submit_button = root.get_by_role("button", name="Пополнить")
```

Что это даёт:
- **strict mode решён структурно**: `root.get_by_role("combobox")` в форме пополнения — один элемент,
  хотя на странице их три (U2.2);
- компонент **переиспользуется**: вторая форма пополнения на другой странице — тот же класс с другим root;
- локаторы короче: не нужно в каждом повторять `page.locator("#deposit-form")...`.

Правило: внутри компонента **только `self.root...`**, не `self.page.get_by_...` — иначе компонент
найдёт элементы чужого блока. Исключение — то, что вне DOM-блока: ответы сети (`self.page.expect_response`).

---

#### 3. Композиция страницы

```python
class DashboardPage(BasePage):
    path = "/app/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.root = page.get_by_test_id("dashboard")
        self.header = Header(page.get_by_test_id("user-panel"))
        self.balances = BalancesTable(page.get_by_test_id("balances-table"))
        self.deposit_form = DepositForm(page.locator("#deposit-form"))
        self.order_form = OrderForm(page.locator("#order-form"))
        self.orders = OrdersTable(page.get_by_test_id("orders-table").locator(".."))
```

Страница отвечает за **где** (какой root у какого компонента) и за **переходы** между экранами.
Компонент — за **как** внутри своего блока.

У таблицы ордеров root — родитель таблицы (`..`): в него входят и фильтр «Статус», и текст
«Ордеров пока нет». Root выбирай так, чтобы в него попало всё, чем компонент управляет.
Лучше — попросить у разработчиков test-id на контейнер (на стенде у карточки его нет).

---

#### 4. Строка таблицы — тоже компонент

```python
class OrderRow(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.status = root.get_by_test_id("order-status")
        self.filled = root.get_by_test_id("order-filled")
        self.cancel_button = root.get_by_role("button", name="Отменить")

    def cancel(self) -> dict:
        with self.page.expect_response(lambda r: r.request.method == "DELETE") as info:
            self.cancel_button.click()
        assert info.value.ok, info.value.text()
        return info.value.json()
```

```python
class OrdersTable(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.rows = root.get_by_test_id("order-row")
        self.empty = root.get_by_test_id("orders-empty")
        self.status_filter = root.get_by_label("Статус")

    def row(self, order_id: str) -> OrderRow:
        return OrderRow(self.rows.and_(self.root.locator(f'[data-id="{order_id}"]')))
```

Тест работает со строкой как с объектом: `orders.row(id).cancel()`, `expect(orders.row(id).status)`.
Локатор строки ленивый — после перерисовки таблицы раз в 2 с объект `OrderRow` продолжает работать
(U2.2: Locator, а не ElementHandle).

---

#### 5. Общая таблица и наследники

Логика «колонка по заголовку» (U2.2) одинакова для любой таблицы — её место в базовом классе:

```python
class Table(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.header_cells = root.locator("thead th")
        self.body_rows = root.locator("tbody tr")

    def column_index(self, name: str) -> int:
        return self.header_cells.all_text_contents().index(name) + 1

    def column(self, name: str) -> Locator:
        return self.root.locator(f"tbody td:nth-child({self.column_index(name)})")
```

```python
class BalancesTable(Table):
    def row(self, asset: str) -> Locator:
        return self.root.locator(f'[data-testid="balance-row"][data-asset="{asset}"]')

    def available(self, asset: str) -> Locator:
        return self.row(asset).get_by_test_id("balance-available")
```

`OrdersTable` тоже может наследовать `Table`, но его root — карточка, а не `<table>`.
Тогда `Table` внутри: `self.table = Table(root.locator("table"))` — **композиция вместо наследования**.
Оба варианта нормальны; наследуй, когда «является» (балансы — это таблица), компонуй, когда «содержит»
(карточка ордеров содержит таблицу и фильтр).

Осторожно: `all_text_contents()` не ждёт (U2.1). Заголовки таблицы статичны и есть в HTML сразу,
поэтому здесь можно. Для динамических заголовков — сначала `expect(self.header_cells).not_to_have_count(0)`.

---

#### 6. Глобальные компоненты: тост и шапка

```python
class Toast(BaseComponent):
    def wait_hidden(self) -> None:
        expect(self.root).to_be_hidden()
```

Тост один на всё приложение → создаётся в `BasePage`: `self.toast = Toast(page.get_by_test_id("toast"))`.
Шапка есть на всех экранах после входа → в общем предке залогиненных страниц или в каждой такой странице.

Метод `Header.logout()` должен вернуть `AuthPage` — но компонент не должен знать о страницах
(иначе компоненты и страницы импортируют друг друга). Решение: компонент только **кликает**,
переход возвращает страница:

```python
class DashboardPage(BasePage):
    def logout(self) -> "AuthPage":
        self.header.logout()
        return AuthPage(self.page).wait_loaded()
```

---

#### 7. Модальное окно (паттерн)

На стенде модалок нет, но на собесе спросят. Типичная модалка подтверждения:

```python
class ConfirmDialog(BaseComponent):
    def __init__(self, root: Locator):
        super().__init__(root)
        self.title = root.get_by_role("heading")
        self.confirm_button = root.get_by_role("button", name="Подтвердить")
        self.cancel_button = root.get_by_role("button", name="Отмена")

    def confirm(self) -> None:
        self.confirm_button.click()
        expect(self.root).to_be_hidden()        # синхронизация: окно закрылось
```

```python
class OrderRow(BaseComponent):
    def request_cancel(self) -> ConfirmDialog:
        self.cancel_button.click()
        dialog = ConfirmDialog(self.page.get_by_role("dialog"))
        expect(dialog.root).to_be_visible()
        return dialog
```

Root модалки — `page.get_by_role("dialog")`: окна обычно рендерятся в конец `<body>`, вне блока,
из которого их открыли, поэтому здесь `self.page` оправдан. Метод, открывающий модалку,
**возвращает её компонент** — как переход на другой экран.

Не путать с нативными `alert` / `confirm` браузера — это `page.on("dialog")`, модуль U3.

---

#### 8. Фасад на странице — нужен ли

Два стиля:

```python
dashboard.deposit_form.deposit("USDT", "1000")    # через компонент
dashboard.deposit("USDT", "1000")                 # фасад: страница делегирует компоненту
```

| | Только компоненты | Фасад на странице |
|---|---|---|
| Тест | чуть длиннее, видно, с каким блоком работаем | короче |
| Страница | тонкая | дублирует методы компонентов |
| Изменения | правится компонент | компонент + фасад |

Рекомендация: фасадные методы — только для **сценариев**, где участвуют несколько компонентов
или переход («войти», «выйти»). Действия внутри одного блока — через компонент.
В задании 6 ты решишь, оставлять ли `dashboard.deposit()` из U4.1, и объяснишь выбор.

---

#### 9. Антипаттерны

| Антипаттерн | Чем плохо |
|---|---|
| `self.page.get_by_...` внутри компонента | находит элементы чужих блоков, strict mode, нельзя переиспользовать |
| компонент знает о страницах (возвращает `AuthPage`) | циклические импорты, компонент нельзя перенести |
| компонент знает о других компонентах | связность; общее — через страницу |
| длинные цепочки в тесте: `dashboard.orders.table.rows.nth(0).cells.nth(2)` | тест снова знает DOM |
| компонент на каждый элемент (`Button`, `Input`) | обёртки без смысла над Locator |
| бизнес-проверки в компонентах | как в PO (U4.1) |
| root, в который не входит часть компонента | фильтр «Статус» вне root таблицы — компонент не может им управлять |

---

#### Собес: вопросы и ответы

**1. Что такое компонент в Page Object и зачем он?**
> Класс для повторяющейся части экрана — формы, таблицы, шапки, модалки, тоста. Получает корневой
> локатор и ищет всё внутри него. Страница собирается из компонентов. Это убирает дублирование —
> одна таблица на пяти страницах описана один раз, — уменьшает размер PO страниц и решает
> неоднозначность локаторов: внутри блока элемент уникален.

**2. Как компонент находит свои элементы?**
> Через root: все локаторы строятся от него — `self.root.get_by_role(...)`. На страницу выходит
> только то, что физически вне блока: ответы сети, модалки, которые рендерятся в конец body.

**3. Наследование или композиция в PO?**
> Композиция — по умолчанию: страница содержит компоненты, карточка содержит таблицу и фильтр.
> Наследование — для «является»: таблица балансов — это таблица, она наследует общую логику колонок.
> Наследовать страницы друг от друга не нужно — общее выносится в BasePage или компоненты.

**4. Как устроишь работу с таблицей?**
> Базовый компонент таблицы: заголовки, колонка по имени через индекс, строки. Наследник для
> конкретной таблицы добавляет доменные методы: строку по id, фильтр. Строка — свой компонент
> со статусом и действиями. Тест пишет `orders.row(id).cancel()` и
> `expect(orders.row(id).status).to_have_text(...)`.

**5. Как работаешь с модальными окнами?**
> Модалка — компонент с root `get_by_role("dialog")`. Метод, который её открывает, ждёт видимость
> и возвращает компонент. `confirm()` нажимает кнопку и ждёт, что окно закрылось. Нативные alert
> и confirm браузера — отдельная история, через `page.on("dialog")`.

**6. Нужны ли фасадные методы на странице?**
> Для сценариев, где участвуют несколько компонентов или есть переход, — да: «войти», «выйти».
> Действия внутри одного блока — через компонент, иначе страница дублирует все методы компонентов.

### Задания — `tests/ui/test_u4_02_components.py`

```text
U4. Урок 2 — компоненты.

Теория: practice/u4_02_components.md
Код компонентов — ui_framework/components/ (заготовки base, common, forms, tables), тесты — здесь.
Запуск:
    uv run pytest tests/ui/test_u4_02_components.py tests/ui/test_u4_01_page_object.py -v

Правила:
    - внутри компонента только self.root... (кроме ответов сети и того, что физически вне блока);
    - компоненты не знают о страницах и друг о друге; переходы между экранами возвращает страница;
    - в тестах нет page.get_by_* / page.locator.

Задача 1. BaseComponent (base.py): __init__(root) — self.root и self.page = root.page.

Задача 2. Toast и Header (common.py).
    Toast: wait_hidden(). Header: email (Locator), logout() — только клик.
    В BasePage self.toast теперь — компонент Toast, а не голый Locator.

Задача 3. Формы (forms.py).
    DepositForm: asset, amount, submit_button; deposit(asset, amount) -> dict (ждёт ответ, падает не на 2xx);
                 deposit_expecting_error(asset, amount).
    OrderForm:   symbol, price, quantity, error, submit_button; side(side) — выбрать радио «Купить»/«Продать»;
                 place(side, price, quantity, symbol="ETH-USDT") -> dict; place_expecting_error(...).

Задача 4. Table (tables.py): header_cells, body_rows, column_index(name), column(name) -> Locator.
    BalancesTable(Table): row(asset), available(asset), locked(asset).

Задача 5. OrderRow и OrdersTable (tables.py).
    OrderRow: status, filled, cancel_button; cell(column_name) -> Locator; cancel() -> dict (ждёт DELETE).
        Подумай: откуда OrderRow узнает индекс колонки по имени? (Ему нужна таблица.)
    OrdersTable: root — карточка ордеров (в неё входят фильтр и «Ордеров пока нет»);
        rows, empty, status_filter; table (Table внутри карточки — композиция);
        row(order_id) -> OrderRow; filter_by_status(status) (""/NEW/.../CANCELED).

Задача 6. DashboardPage из компонентов.
    header, balances, deposit_form, order_form, orders; logout() остаётся на странице (переход).
    Реши, оставлять ли фасады deposit()/place_order() из U4.1 (раздел 8 теории). Тесты U4.1 должны
    проходить — либо без изменений (фасад), либо поправь их. Выбор объясни в «Ответах».

Задача 7. Тесты на компоненты.
    а) Ордер с пустой ценой → ошибка формы ордера видна и содержит "price"; строк ордеров 0
       (вспомни U2.1: перед проверкой отсутствия — положительный признак загрузки).
    б) Три BUY (цены 10, 20, 30); отмени 20 через orders.row(id).cancel();
       фильтр CANCELED → одна строка, cell("Цена") == "20"; фильтр NEW → колонка «Цена» == ["30", "10"].
    в) Балансы нового пользователя: колонка «Актив» — все три актива одной проверкой списком
       (сначала посмотри, в каком порядке их отдаёт стенд — порядок в форме пополнения другой);
       доступно 0 у всех трёх (expect.soft).
    г) Выход через dashboard.logout() → AuthPage, форма входа видна; повторный вход тем же email → кабинет.

Задача 8. Структура (письменно в «Ответах»).
    Куда положишь метод «отменить все открытые ордера»: OrdersTable, DashboardPage или хелпер в тесте?
    А «проверить, что ордер исполнился» (ждёт FILLED с таймаутом 15 с)? Почему?

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое компонент в Page Object и зачем он?
    2. Как компонент находит свои элементы?
    3. Наследование или композиция в PO?
    4. Как устроишь работу с таблицей?
    5. Как работаешь с модальными окнами?
    6. Нужны ли фасадные методы на странице?
```

<a id="u4-3"></a>

## U4.3 Фикстуры страниц и конфиг окружений

*Теория: `practice/u4_03_fixtures_config.md`*

Задания: `tests/ui/test_u4_03_fixtures_config.py`, код — `ui_framework/config/`, `ui_framework/fixtures/`.

Основы фикстур (scope, yield, conftest, `browser_context_args`) были в U1.4. Здесь — то, из чего
собирают фреймворк: фикстуры страниц, фабрики с уборкой, `request` и маркеры с данными,
параметризованные фикстуры, фикстуры в пакете фреймворка (`pytest_plugins`), конфиг окружений
на pydantic-settings, секреты, наборы тестов по маркерам.

---

#### 1. Фикстуры страниц

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

##### Фабрика страниц

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

#### 2. Уборка: yield, финализаторы, фабрики

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

##### Фабрика с уборкой

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

##### Что если teardown упал

Тест прошёл, а уборка упала — pytest покажет **ERROR at teardown** (не FAILED). Если упали оба —
увидишь и FAILED, и ERROR. Уборку пишут защитно: не падать, если «уже убрано».

`request.addfinalizer(func)` — то же, что код после `yield`, но можно зарегистрировать
несколько функций по ходу. С `yield` читается проще — используй его.

##### Зачем убирать, если пользователь каждый раз новый

Пользователь новый, но **стакан общий** (U1.4: наш SELL исполнился об чужой BUY).
Открытые ордера, оставленные тестами, мешают другим. Отменить свои — дешёвая гигиена.
Через UI это медленно; в U5 научимся убирать через API (`page.request`).

---

#### 3. `request`: что знает фикстура о тесте

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

#### 4. Параметризованные фикстуры

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

##### `indirect=True` — параметр в фикстуру из теста

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

#### 5. autouse — когда можно

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

#### 6. Где живут фикстуры: иерархия conftest и `pytest_plugins`

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

#### 7. Конфиг окружений на pydantic-settings

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

##### Связать с pytest-playwright

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

##### Секреты

- в коде и в git — **никогда**: пароли, токены, ключи;
- в CI — переменные окружения / secrets CI (`UI_USER_PASSWORD`);
- локально — `envs/*.local.env` (в `.gitignore`) или `.env`;
- `SecretStr`: в логах и `repr` печатается `**********`, значение — `.get_secret_value()`;
- не печатать секреты в Allure-шагах и логах.

---

#### 8. Наборы тестов

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

#### 9. Частые ошибки

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

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u4_03_fixtures_config.py`

```text
U4. Урок 3 — фикстуры страниц и конфиг окружений.

Теория: practice/u4_03_fixtures_config.md
Код: ui_framework/config/settings.py, ui_framework/fixtures/{pages,data}.py, tests/conftest.py (создать).
Запуск:
    uv run pytest tests/ui/test_u4_03_fixtures_config.py -v
    ENV=stage uv run pytest tests/ui/test_u4_03_fixtures_config.py -m smoke -v   # stage: up -d --build

Задача 1. Settings (ui_framework/config/settings.py).
    Поля: env, base_url, user_password (SecretStr), expect_timeout_ms, action_timeout_ms, matching_timeout_ms.
    Выбор окружения переменной ENV (local | docker | stage, по умолчанию docker),
    файлы envs/ui.<env>.env (в git) и envs/ui.<env>.local.env (не в git — проверь .gitignore).
    Создай envs/ui.local.env, envs/ui.docker.env, envs/ui.stage.env с адресами из таблицы теории;
    на stage таймауты больше.

Задача 2. Связать с pytest (tests/conftest.py — корневой, создать).
    - pytest_plugins с фикстурами из ui_framework/fixtures;
    - фикстуры settings (session) и base_url (session; --base-url из командной строки главнее);
    - pytest_configure: expect.set_options(timeout=...) из настроек;
    - pytest_report_header: env и base_url в шапке прогона;
    - убери base_url из pyproject.toml и проверь, что тесты U1.4 и U4.1 по-прежнему идут на :8080.

Задача 3. Фикстуры данных и страниц.
    data.py: unique_email() (функция) и фикстура user_email.
    pages.py: auth_page, dashboard (пароль — из settings), new_dashboard (фабрика: новый context → DashboardPage).
    Перенеси сюда фикстуры из tests/ui/conftest.py, которые относятся к PO (U4.1–U4.2), чтобы не было
    двух источников. Фикстуры U1.4 (logged_in_page, create_user) оставь — на них опираются старые уроки.

Задача 4. autouse.
    Фикстура, выставляющая page.set_default_timeout(settings.action_timeout_ms) всем UI-тестам.
    Где ей место: tests/ui/conftest.py или ui_framework/fixtures? Объясни в «Ответах».

Задача 5. Маркер с данными.
    Зарегистрируй маркер balance. dashboard читает его и пополняет счёт:
        @pytest.mark.balance(USDT="1000", ETH="2")
    Тест: доступно USDT 1000 и ETH 2, BTC 0.

Задача 6. Уборка.
    order_factory: создаёт ордера через order_form, после теста отменяет те, что ещё открыты.
    Тест 1: создай 3 ордера, один отмени сам — уборка не должна упасть на уже отменённом.
    Тест 2: создай ордер и упади (assert False) под @pytest.mark.xfail(strict=True) — запусти с -s:
            покажи (print в teardown), что уборка выполнилась.

Задача 7. Параметризация.
    а) Параметризованная фикстура asset (USDT, BTC, ETH) с ids; тест пополнения на 1 — 3 прогона.
    б) funded_dashboard через indirect=True: два набора — {"USDT": "1000"} и {"ETH": "5", "BTC": "1"};
       проверь доступные балансы из request.param (один тест, проверки в цикле по словарю).

Задача 8. Два пользователя через new_dashboard.
    Продавец SELL ETH-USDT, покупатель BUY по той же цене (вспомни U1.4: цена вне чужих ордеров),
    оба ордера FILLED (таймаут — settings.matching_timeout_ms), балансы обоих после сделки.

Задача 9. Наборы.
    Пометь smoke тесты задач 5 и 8. Зарегистрируй regression; модуль целиком — pytestmark = regression.
    Запусти: uv run pytest tests/ui/test_u4_03_fixtures_config.py -m smoke и ENV=stage ... -m smoke.
    В «Ответах»: что показала шапка прогона, и сколько упало на stage (5% сбоев).

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Какие scope у фикстур и что когда используешь?
    2. Как выполняется cleanup в фикстурах?
    3. Как запустить одни и те же UI-тесты на разных окружениях?
    4. Где хранишь секреты?
    5. Когда используешь autouse?
    6. Как передать фикстуре параметры из теста?
    7. Где лежат фикстуры в твоём фреймворке?
```

<a id="u4-4"></a>

## U4.4 Утилиты, Allure и структура проекта

*Теория: `practice/u4_04_utils_allure_structure.md`*

Задания: `tests/ui/test_u4_04_utils_allure.py`, код — `ui_framework/utils/`, `ui_framework/data/`,
`ui_framework/fixtures/reporting.py`.

План: что такое слой утилит и что в него класть (и что нет); деньги и даты; генераторы и модели
тестовых данных; ожидание произвольного условия; логирование шагов; Allure — шаги, вложения,
метки, скриншот при падении, окружение, просмотр отчёта; итоговая структура UI-фреймворка.

---

#### 1. Слой утилит

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

#### 2. Деньги

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

##### Даты

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

#### 3. Тестовые данные: генераторы и модели

##### Генераторы уникальных значений

```python
from uuid import uuid4


def unique_email(prefix: str = "user") -> str:
    return f"{prefix}_{uuid4().hex[:8]}@test.com"
```

Faker (`faker.email()`) даёт «правдоподобные» данные, но **не гарантирует уникальность** — на сотнях
прогонов будут совпадения. Для ключевых полей (email, имя) — uuid; Faker — для «декоративных».

##### Модель данных

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

##### Данные, не пересекающиеся с чужими

Урок U1.4: стакан общий. Генератор цены вне диапазона «чужих» ордеров:

```python
def isolated_price(low: int = 300, high: int = 499) -> str:
    return str(random.randint(low, high))
```

Лучше — вообще не зависеть от общего стакана (своё окружение на прогон), но если нельзя —
такие правила фиксируются в одном месте с комментарием почему.

---

#### 4. Ожидание условия (polling)

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

#### 5. Логирование шагов

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

#### 6. Allure

`allure-pytest` уже стоит. Запуск с отчётом:

```bash
uv run pytest tests/ui -m smoke --alluredir allure-results --clean-alluredir
allure serve allure-results                          # собрать и открыть в браузере
allure generate allure-results -o allure-report --clean   # статический отчёт
```

Allure CLI на машине есть, но ему нужна **Java** (`brew install openjdk`, дальше следовать
подсказке brew про PATH). `allure-results/` и `allure-report/` в `.gitignore`.

##### Шаги

```python
import allure


class DepositForm(BaseComponent):
    @allure.step("Пополнить {asset} на {amount}")
    def deposit(self, asset: str, amount: str) -> dict: ...
```

```python
def test_deposit(dashboard):
    dashboard.deposit_form.deposit("USDT", "1000")
    with allure.step("Проверить баланс"):
        expect(dashboard.balances.available("USDT")).to_have_text("1000")
```

- декоратор на методах PO / компонентов — шаги появляются во **всех** тестах автоматически;
- `{asset}` подставляет аргумент по имени; строки Allure показывает **в кавычках**:
  `Пополнить 'USDT' на '1000'` (проверено на нашей версии);
- вложенные шаги — дерево: `deposit` внутри шага `with allure.step(...)`;
- пароли не попадают в шаги: не делай `@allure.step("Войти {email} / {password}")`.

##### Вложения

```python
allure.attach(page.screenshot(full_page=True), name="screenshot", attachment_type=allure.attachment_type.PNG)
allure.attach(json.dumps(order, indent=2), name="order", attachment_type=allure.attachment_type.JSON)
allure.attach.file("test-results/.../trace.zip", name="trace", extension="zip")
```

##### Скриншот при падении — хук

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

##### Метки

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

##### Окружение в отчёте

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

#### 7. Структура UI-фреймворка

```
ui_framework/
  config/
    settings.py          # Settings: окружения, таймауты, секреты (U4.3)
  pages/                 # экраны: BasePage, AuthPage, DashboardPage (U4.1)
  components/            # формы, таблицы, тост, шапка (U4.2)
  fixtures/              # pytest-плагины: pages.py, data.py, reporting.py (U4.3–U4.4)
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
- **зависимости в одну сторону**: tests → fixtures → pages → components → utils/data.
  `utils` не импортирует `pages`, компоненты не импортируют страницы (U4.2);
- **конфиг в одном месте** — окружения переключаются без правки кода;
- **данные отдельно от логики** — модели и генераторы переиспользуются в API-тестах.

---

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u4_04_utils_allure.py`

```text
U4. Урок 4 — утилиты, Allure и структура проекта.

Теория: practice/u4_04_utils_allure_structure.md
Код: ui_framework/utils/{money,waiting}.py, ui_framework/data/{models,generators}.py,
     ui_framework/fixtures/reporting.py (заготовки есть).
Запуск:
    uv run pytest tests/ui/test_u4_04_utils_allure.py -v --alluredir allure-results --clean-alluredir
    allure serve allure-results          # нужна Java: brew install openjdk (см. теорию, раздел 6)

Задача 1. Деньги (utils/money.py).
    to_decimal(value) и format_amount(value) — как сервер (exchange/schemas.py, _format_amount).
    Короткие проверки здесь же (обычные pytest-тесты без браузера, без фикстуры page):
        "100.50" → "100.5"; "1000.000" → "1000"; "0" → "0"; "0.00000001" → "0.00000001"; 1000 - 100.50 → "899.5".
    Подумай: почему Decimal(0.1) != Decimal("0.1")? Проверь и запиши в «Ответах».
    Заметь: если autouse-фикстура из U4.3 берёт page, эти тесты без браузера всё равно поднимут браузер
    (теория U4.3, раздел 5). Как это исправить: перенести тесты утилит в tests/unit/? сделать autouse
    умнее? Реши и объясни в «Ответах».

Задача 2. wait_until (utils/waiting.py) — по теории, раздел 4, с параметром ignore=(исключения,).
    Тесты без браузера: условие становится True на 3-й попытке — проходит;
    никогда не True — AssertionError с твоим сообщением; исключение из ignore — считается «ещё нет».

Задача 3. Данные (data/).
    generators.py: unique_email (перенеси из fixtures/data.py — фикстура user_email пусть использует его),
                   isolated_price(low, high) с комментарием, зачем.
    models.py: OrderData (frozen dataclass) с полем-свойством cost.
    Тест через UI: BUY OrderData(price="100.5", quantity="2") → заблокировано USDT == format_amount(order.cost),
    доступно == format_amount(1000 - order.cost). Пополнение 1000 — маркером balance из U4.3.

Задача 4. Allure-шаги.
    @allure.step с параметрами на публичных методах AuthPage, DashboardPage и компонентов-форм/строки.
    Пароль в шаг не должен попасть — проверь в отчёте.
    В тестах — with allure.step(...) для блоков проверок.

Задача 5. Скриншот и URL при падении (fixtures/reporting.py, подключи через pytest_plugins).
    Тест, который падает специально, под @pytest.mark.xfail(strict=True):
    в отчёте у него есть screenshot и url. Посмотри в allure serve.

Задача 6. Метки.
    На тесты задач 3 и 7: epic/feature/story/title/severity. Для xfail из задачи 5 — allure.issue("DEMO-1").
    В отчёте открой вкладку Behaviors: как сгруппировались тесты?

Задача 7. parametrize + allure.dynamic.
    Неверные суммы пополнения ("0", "-5", "abc") — один тест; allure.dynamic.title с суммой в названии.

Задача 8. environment.properties.
    pytest_sessionstart в reporting.py: env и base_url из Settings в allure-results.
    Проверь на главной отчёта для ENV=docker и ENV=stage.

Задача 9. Логирование.
    Логгер "ui" в DepositForm и OrderForm (INFO: что отправили, что ответил сервер — статус и id).
    Запусти один тест с --log-cli-level=INFO -s — что видно? Пароль/токен не должен печататься.

Задача 10. Структура (письменно в «Ответах»).
    Нарисуй дерево своего ui_framework/ и tests/ после U4.1–U4.4. Для каждой папки — одна строка «зачем».
    Найди хотя бы одну зависимость «не в ту сторону» (компонент импортирует страницу, utils знает про page…)
    и исправь, если есть.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как устроен твой UI-фреймворк целиком?
    2. Что кладёшь в utils, а что нет?
    3. Как работаешь с деньгами в тестах?
    4. Как делаешь шаги и вложения в Allure?
    5. Как прикрепить скриншот к упавшему тесту?
    6. Зачем модели тестовых данных?
```

<a id="u4-5"></a>

## U4.5 Screenplay, собес по модулю U4 и каркас фреймворка

*Теория: `practice/u4_05_screenplay_interview.md`*

Задания: `tests/ui/test_u4_05_screenplay_framework.py`, код — `ui_framework/screenplay/`.

План: что такое Screenplay и чем он отличается от Page Object; мини-реализация поверх наших PO;
когда что выбирать; чек-лист готового каркаса UI-фреймворка; шпаргалка и банк вопросов по модулю U4.

---

#### 1. Screenplay: идея

Page Object отвечает на вопрос «**что есть на экране** и что с ним можно сделать».
Screenplay — на вопрос «**кто** что делает и **зачем**». Сценарий описывается через участников:

| Понятие | Что это | Пример на стенде |
|---|---|---|
| **Actor** | участник сценария | продавец Алиса, покупатель Боб |
| **Ability** | что актор умеет — обёртка над инструментом | `BrowseTheWeb(page)`, `CallTheApi(client)` |
| **Task** | бизнес-действие из нескольких шагов | `Register`, `Deposit`, `PlaceOrder` |
| **Interaction** | одно низкоуровневое действие | `Click`, `Fill` (часто — методы PO) |
| **Question** | что актор может узнать о системе | `AvailableBalance("USDT")`, `OrderStatus(id)` |

Тест читается как история:

```python
alice = Actor("Алиса").can(BrowseTheWeb(seller_page))
bob = Actor("Боб").can(BrowseTheWeb(buyer_page))

alice.attempts_to(Register(), Deposit("ETH", "1"), PlaceOrder("SELL", price, "1"))
bob.attempts_to(Register(), Deposit("USDT", "1000"), PlaceOrder("BUY", price, "1"))

expect(alice.asks_for(LastOrderStatus())).to_have_text("FILLED", timeout=15_000)
expect(bob.asks_for(AvailableBalance("ETH"))).to_have_text("1")
```

Классическое изложение — Serenity BDD (Java/JS); в Python есть библиотека `screenpy`. На собесе
спрашивают **идею и сравнение с PO**, а не конкретную библиотеку.

---

#### 2. Мини-реализация поверх Page Object

Screenplay не заменяет PO целиком: **interactions** и **questions** удобно строить на методах
страниц и компонентов. Минимум кода:

```python
# ui_framework/screenplay/actor.py
from typing import Protocol, TypeVar

T = TypeVar("T")


class Performable(Protocol):
    def perform_as(self, actor: "Actor") -> None: ...


class Answerable(Protocol[T]):
    def answered_by(self, actor: "Actor") -> T: ...


class Actor:
    def __init__(self, name: str):
        self.name = name
        self._abilities: dict[type, object] = {}
        self.memory: dict[str, object] = {}          # что актор запомнил: email, id ордера

    def can(self, *abilities: object) -> "Actor":
        for ability in abilities:
            self._abilities[type(ability)] = ability
        return self

    def ability_to(self, kind: type[T]) -> T:
        try:
            return self._abilities[kind]
        except KeyError:
            raise AssertionError(f"{self.name} не умеет {kind.__name__}") from None

    def attempts_to(self, *tasks: Performable) -> None:
        for task in tasks:
            task.perform_as(self)

    def asks_for(self, question: "Answerable[T]") -> T:
        return question.answered_by(self)
```

```python
# ui_framework/screenplay/abilities.py
class BrowseTheWeb:
    def __init__(self, page: Page):
        self.page = page
        self.auth = AuthPage(page)
        self.dashboard = DashboardPage(page)
```

```python
# ui_framework/screenplay/tasks.py
class Register:
    def __init__(self, email: str | None = None):
        self.email = email

    def perform_as(self, actor: Actor) -> None:
        web = actor.ability_to(BrowseTheWeb)
        email = self.email or unique_email(actor.name)
        web.auth.open().register(email, PASSWORD)
        actor.memory["email"] = email


class PlaceOrder:
    def __init__(self, side: str, price: str, quantity: str, symbol: str = "ETH-USDT"):
        self.order = OrderData(side, price, quantity, symbol)

    def perform_as(self, actor: Actor) -> None:
        web = actor.ability_to(BrowseTheWeb)
        created = web.dashboard.order_form.place(**asdict(self.order))
        actor.memory["last_order_id"] = created["id"]
```

```python
# ui_framework/screenplay/questions.py
class AvailableBalance:
    def __init__(self, asset: str):
        self.asset = asset

    def answered_by(self, actor: Actor) -> Locator:
        return actor.ability_to(BrowseTheWeb).dashboard.balances.available(self.asset)


class LastOrderStatus:
    def answered_by(self, actor: Actor) -> Locator:
        order_id = actor.memory["last_order_id"]
        return actor.ability_to(BrowseTheWeb).dashboard.orders.row(order_id).status
```

Question возвращает **Locator** — проверку делает тест через `expect` (как в PO, U4.1).
В «настоящем» Screenplay есть ещё `actor.should_see_the(question, matcher)` — для Playwright
естественнее оставить `expect`.

`actor.memory` — место, где актор хранит то, что узнал по ходу: id ордера, email. В PO состояние —
антипаттерн (U4.1), а в Screenplay это **память участника**, и она явная: задача пишет, вопрос читает.

---

#### 3. Сила Screenplay: несколько каналов и участников

Ability можно добавить любую:

```python
alice = Actor("Алиса").can(BrowseTheWeb(page), CallTheApi(api_client))

alice.attempts_to(RegisterViaApi(), DepositViaApi("USDT", "1000"))   # подготовка через API — быстро
alice.attempts_to(PlaceOrder("BUY", "100", "1"))                     # проверяемое действие — через UI
```

Задачи, которым всё равно, UI это или API, переиспользуются; сценарии с несколькими пользователями
читаются естественно. (API внутри Playwright — U5.)

---

#### 4. Page Object или Screenplay

| | Page Object | Screenplay |
|---|---|---|
| Единица | экран / компонент | задача, вопрос, участник |
| Порог входа | низкий, знают все | выше: больше классов, нужно договориться о стиле |
| Код | меньше | больше: класс на задачу и вопрос |
| Несколько пользователей | несколько PO / context — ок, но тест знает про страницы | естественно: акторы |
| UI + API в одном сценарии | отдельные клиенты рядом с PO | способности одного актора |
| Переиспользование | на уровне экранов | на уровне бизнес-действий |
| Риск | «God object», раздутые страницы | взрыв мелких классов, «архитектура ради архитектуры» |

Практичный ответ на собесе: **PO — основа**, она есть почти в каждом проекте. Screenplay —
когда сценарии многошаговые, участников несколько и действия идут через разные каналы. Часто
делают гибрид: PO и компоненты внизу, поверх — слой бизнес-шагов (по сути tasks), а тесты
используют шаги.

Наш фреймворк уже «гибридный»: фикстуры (`dashboard`, `new_dashboard`) и хелперы сценариев —
это и есть слой задач, только без классов.

---

#### 5. Каркас UI-фреймворка: чек-лист готовности

Это артефакт модуля U4 — то, что показываешь на собесе («расскажите про ваш фреймворк»)
и что должно работать у другого человека с нуля.

**Запуск**
- [ ] README фреймворка: установка (`uv sync`, `playwright install` / `--browser-channel chrome`),
      запуск стенда, запуск тестов, окружения, Allure;
- [ ] `uv run pytest tests/ui` зелёный на docker;
- [ ] `ENV=stage uv run pytest tests/ui -m smoke` — запускается (падения от 5% сбоев допустимы и объяснимы);
- [ ] отчёт Allure собирается: шаги, скриншот при падении, окружение.

**Структура**
- [ ] `config/`, `pages/`, `components/`, `fixtures/`, `data/`, `utils/` — каждая папка с понятной ролью;
- [ ] зависимости в одну сторону (U4.4, раздел 7), нет циклических импортов;
- [ ] фикстуры фреймворка подключены через `pytest_plugins`, conftest тестов маленький.

**Page Object и компоненты**
- [ ] в тестах нет `page.get_by_*` / `page.locator`;
- [ ] в PO нет бизнес-проверок; методы для проверок отдают Locator;
- [ ] компоненты ищут только внутри root;
- [ ] переходы между экранами возвращают PO.

**Данные и стабильность**
- [ ] уникальные данные на тест; цены не пересекаются с чужими ордерами;
- [ ] уборка за собой; уборка не падает на «уже убрано»;
- [ ] нет `sleep`, `networkidle`, `force=True`; хелперы ждут ответ сервера, а не тост (U2.1);
- [ ] `--count 5` на ключевых тестах — зелёный.

**Конфиг и секреты**
- [ ] адреса и таймауты — в env-файлах; секретов нет в git;
- [ ] `--base-url` перекрывает конфиг.

**Отчёт**
- [ ] `@allure.step` на методах PO, без паролей; метки feature/story/severity на тестах.

---

#### 6. Шпаргалка по модулю U4

- **PO (U4.1)**: класс на экран; «как» в PO, «что» в тесте; локаторы атрибутами (ленивые);
  переходы возвращают PO; проверки — Locator для `expect`; в PO только синхронизация и проверка
  своего действия; отдельные методы для негативных сценариев.
- **Компоненты (U4.2)**: root-локатор, поиск только внутри; страница = композиция; строка таблицы —
  компонент; общая `Table` с колонкой по заголовку; компоненты не знают о страницах; модалка —
  компонент, метод открытия возвращает его.
- **Фикстуры и конфиг (U4.3)**: фикстуры страниц и фабрики; `yield`-уборка в обратном порядке;
  `request` и маркеры с данными; параметризованные фикстуры и `indirect`; autouse — только настройка;
  фикстуры в пакете через `pytest_plugins`; pydantic-settings, `ENV`, env-файлы, приоритет источников,
  `SecretStr`; перекрытие `base_url`.
- **Утилиты и отчёт (U4.4)**: utils не знают о page; Decimal из строки; `format_amount` как сервер;
  frozen dataclass для данных; `wait_until` на monotonic; Allure — шаги декоратором, скриншот хуком,
  метки, окружение; зависимости в одну сторону.
- **Screenplay (U4.5)**: актор, способности, задачи, вопросы; сила — несколько участников и каналов;
  PO — основа, Screenplay или гибрид — по сложности сценариев.

---

#### Собес: банк вопросов по модулю U4

Весь банк модуля — разделы «Собес» уроков U4.1 (7 вопросов), U4.2 (6), U4.3 (7), U4.4 (6) и новые ниже (5).

**1. Что такое Screenplay и чем он отличается от Page Object?**
> Screenplay описывает сценарий через участников: актор со способностями — браузер, API — выполняет
> задачи, то есть бизнес-действия, и задаёт вопросы о состоянии системы. Page Object описывает экраны.
> PO проще и меньше кода; Screenplay лучше масштабируется на многошаговые сценарии с несколькими
> участниками и каналами — UI и API в одном тесте, — и переиспользует бизнес-действия, а не экраны.
> Цена — больше классов и выше порог входа.

**2. Что выберешь для нового проекта?**
> Page Object с компонентами как основу — его знает любой в команде. Поверх, когда сценарии становятся
> длинными, — слой бизнес-шагов. Полный Screenplay — если много ролей и сценариев «UI плюс API»,
> и команда готова поддерживать больше абстракций. Решаю по сложности сценариев, а не по моде.

**3. Расскажи про свой UI-фреймворк** (главный вопрос, 2–3 минуты).
> План ответа: стек (Python, pytest, Playwright, pydantic-settings, Allure) → слои снизу вверх
> (конфиг, утилиты и данные, компоненты, страницы, фикстуры, тесты) → как обеспечена стабильность
> (web-first проверки, хелперы ждут ответ сервера, изоляция данных, уборка) → окружения и секреты →
> отчётность → одно решение, которым гордишься, и одно, которое переделал бы.
> Готовая версия — твоя, в задаче 6.

**4. Как добавить в фреймворк новую страницу?**
> Если есть повторяющиеся блоки — сначала компоненты с root. Потом PO страницы: path, root, компоненты,
> переходы, `wait_loaded`. Фикстура страницы в `fixtures/pages.py`. Шаги Allure на публичных методах.
> Тест — только через PO. Если страница открывается из другой — метод перехода возвращает новый PO.

**5. Как поймёшь, что Page Object стал плохим?**
> Сотни строк и десятки методов, методы на каждый клик или наоборот на целый тест, проверки внутри,
> состояние, зашитые данные, тесты лезут в `page` мимо PO, правка одной кнопки ломает много мест.
> Лечу разбиением на компоненты и разделением экранов.

### Задания — `tests/ui/test_u4_05_screenplay_framework.py`

```text
U4. Урок 5 — Screenplay, собес по модулю U4 и каркас фреймворка.

Теория и банк вопросов: practice/u4_05_screenplay_interview.md
Код: ui_framework/screenplay/{actor,abilities,tasks,questions}.py (заготовки есть).
Запуск:
    uv run pytest tests/ui/test_u4_05_screenplay_framework.py -v

Задача 1. Ядро (actor.py, abilities.py).
    Actor: can(...), ability_to(kind), attempts_to(*tasks), asks_for(question), memory.
    BrowseTheWeb(page): auth и dashboard — твои PO из U4.1–U4.2.

Задача 2. Задачи и вопросы (tasks.py, questions.py).
    Tasks: Register(email=None), Deposit(asset, amount), PlaceOrder(side, price, quantity, symbol),
           CancelOrder(order_id=None — если None, отменить последний из памяти).
    Questions: AvailableBalance(asset), LockedBalance(asset), LastOrderStatus() — возвращают Locator.
    Используй OrderData и unique_email из U4.4.

Задача 3. Сделка двух участников в стиле Screenplay.
    Фикстура actor_factory(name) -> Actor: новый context (new_context), BrowseTheWeb.
    Алиса продаёт ETH, Боб покупает по той же цене (isolated_price из U4.4).
    Проверь статусы и балансы обоих через asks_for + expect (таймаут — из settings).

Задача 4. Тот же сценарий на PO.
    Перепиши задачу 3 только через new_dashboard и PO (без screenplay).
    В «Ответах»: сравни два теста — строки, читаемость, что пришлось написать дополнительно,
    что проще поменять, если подготовку (регистрацию и пополнение) перенести на API.

Задача 5. Чек-лист каркаса.
    Пройди чек-лист из теории (раздел 5) по своему ui_framework/ — отметь в «Ответах» каждый пункт:
    ✅ / ❌ + что сделаешь. Исправь всё, что можно исправить за 30 минут.
    Обязательно: ui_framework/README.md (установка, стенд, запуск, окружения, Allure, структура,
    «как добавить страницу»).

Задача 6. Рассказ про фреймворк.
    Напиши в «Ответах» свой ответ на вопрос 3 банка («Расскажи про свой UI-фреймворк») по плану из теории.
    Потом расскажи его вслух под диктофон за 2–3 минуты, прослушай, сократи лишнее.

Задача 7. Лайвкодинг — 25 минут.
    «Добавь в фреймворк проверку частичного исполнения»:
    продавец SELL ETH-USDT кол-во 2, покупатель BUY кол-во 1 по той же цене.
    У продавца статус PARTIALLY_FILLED, исполнено 1, заблокировано ETH 1; фильтр «Статус» =
    PARTIALLY_FILLED показывает одну строку. Только через фреймворк (PO или screenplay — на выбор).
    Засеки время; что не успел — в «Ответах».

Задача 8. Устный собес по модулю U4.
    10 случайных вопросов из банка (U4.1–U4.5, всего 31), 40–90 с на ответ, вслух, без подглядывания.
    В «Ответах» — номера, на которых «поплыл».
```


---

# U5. Данные, авторизация и API внутри Playwright

<a id="u5-1"></a>

## U5.1 API внутри Playwright

*Теория: `practice/u5_01_api_in_playwright.md`*

Задания: `tests/ui/test_u5_01_api_in_playwright.py`, код — `ui_framework/api/`.

План: зачем UI-тестам API; `APIRequestContext` — откуда взять и чем отличаются варианты; запросы
и ответы; авторизация на стенде; тонкий API-клиент; подготовка через API → проверка в UI
(как «залогинить» браузер токеном); проверка UI-действия через API; уборка через API; ретраи
с ключом идемпотентности; ловушки.

Модуль U5: U5.1 API внутри Playwright → U5.2 тестовые данные → U5.3 storage_state, роли, изоляция
и параллельный запуск → U5.4 собес.

---

#### 1. Зачем UI-тесту API

Тест «отмена ордера» через UI: регистрация (форма), пополнение (форма), ордер (форма), отмена,
проверки. Проверяется только **отмена** — всё остальное подготовка, которая:
- **медленная**: каждый шаг через UI — секунды (задача 5 — замерь сам);
- **хрупкая**: упала форма пополнения — упал тест про отмену, хотя отмена работает;
- **дублирует** тесты, которые уже проверяют регистрацию и пополнение.

Правило: **через UI — то, что тест проверяет; всё остальное — через API**. Плюс уборка через API.

---

#### 2. APIRequestContext: три способа получить

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

#### 3. Запросы и ответы

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

##### Ловушка `base_url` с путём

`base_url="http://host/api"` + `api.get("/orders")` → `http://host/orders`: путь с ведущим `/`
**заменяет** путь из base_url (правила URL). Для base_url с путём — слеш в конце и относительный путь:
`base_url="http://host/api/"`, `api.get("orders")`. У нашего стенда base_url без пути — проблемы нет.

---

#### 4. Авторизация на стенде

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

#### 5. Тонкий API-клиент

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

#### 6. Подготовка через API → проверка в UI

Пользователь создан и пополнен через API. Как открыть **браузер** уже залогиненным? Фронтенд
при загрузке читает `localStorage["token"]` и `["email"]` (`app.js`). Значит, нужно положить их
в localStorage **до** загрузки страницы.

##### Через storage_state (рекомендуется)

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

##### Через add_init_script (хуже)

```python
context.add_init_script(f"localStorage.setItem('token', '{token}')")
```

Скрипт выполняется **при каждой** загрузке страницы. Тест нажал «Выйти», сделал `reload` — и снова
залогинен (проверено на стенде). Тест логаута становится невозможным, поведение неочевидно.

##### Через UI-логин (медленно)

Один логин через форму — нормально для теста **логина**. Для остальных — API + storage_state.

##### После API-действия UI обновится не сразу

UI опрашивает сервер раз в 2 с (U2.1). Отменил ордер через API, пока страница открыта, — `expect`
дождётся следующего опроса. Либо `page.reload()`, если опроса нет.

---

#### 7. Действие в UI → проверка через API

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

#### 8. Уборка через API

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

#### 9. Ретраи подготовки и ключ идемпотентности

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

#### 10. Ловушки

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

#### Собес: вопросы и ответы

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

### Задания — `tests/ui/test_u5_01_api_in_playwright.py`

```text
U5. Урок 1 — API внутри Playwright.

Теория: practice/u5_01_api_in_playwright.md
Код: ui_framework/api/client.py, ui_framework/fixtures/api.py (заготовки есть; подключи в pytest_plugins).
Запуск:
    uv run pytest tests/ui/test_u5_01_api_in_playwright.py -v -s

Правило урока: через UI — только то, что тест проверяет. Регистрация, пополнение, ордера для подготовки —
через API. Проверки экрана — через PO (U4).

Задача 1. ExchangeApi (api/client.py).
    register, login (запоминает токен), deposit, place_order (принимает и OrderData из U4.4), cancel_order,
    orders(status=None), balances(). На не-2xx — AssertionError с URL, статусом и телом.
    Параметр idempotency_key у place_order — передаёт заголовок Idempotency-Key.

Задача 2. Фикстуры (fixtures/api.py).
    api_context — session, playwright.request.new_context(base_url=...), dispose в teardown.
    api_user — фабрика: каждый вызов создаёт пользователя через API и возвращает (email, ExchangeApi);
               после теста отменяет все открытые ордера (NEW и PARTIALLY_FILLED) всех созданных пользователей.

Задача 3. Браузер, залогиненный токеном.
    Функция или фикстура login_in_browser(email, client) -> DashboardPage:
    новый context со storage_state (localStorage: token, email), открыть кабинет, wait_loaded.
    Тест: пользователь из api_user → в шапке его email, форма входа не показывалась.

Задача 4. Подготовка через API, проверка в UI.
    Через API: пополнить USDT 1000, три BUY-ордера (цены 10, 20, 30, кол-во 1).
    В UI: строк 3, колонка «Цена» == ["30", "20", "10"], заблокировано USDT 60, доступно 940.

Задача 5. Сколько экономим.
    Замерь time.perf_counter(): (а) регистрация + пополнение через UI (PO), (б) то же через API +
    открытие кабинета токеном. Выведи оба числа (-s). Запиши в «Ответах» и посчитай, сколько сэкономит
    набор из 200 тестов.

Задача 6. API-действие при открытом UI.
    Кабинет открыт, ордер создан через API и виден в таблице. Отмени его через API.
    Без reload: статус в UI станет CANCELED (опрос раз в 2 с), заблокировано 0.

Задача 7. UI-действие, проверка через API.
    В UI размести BUY цена "100.50" кол-во "0.5". Через API: ордер есть, price == "100.5",
    quantity == "0.5", status NEW; заблокировано в API-балансе == то, что показывает UI.

Задача 8. Токен истёк.
    Подложи в localStorage мусорный токен (storage_state) и открой кабинет.
    Ожидание: фронт получил 401, сам разлогинился — видна форма входа, token в localStorage пропал.
    Подумай: почему так можно тестировать «истёкший токен», не ожидая 15 минут?

Задача 9. Ретрай с ключом идемпотентности (stage, 5% сбоев: docker compose --profile stage up -d --build).
    Против stage (--base-url http://localhost:8081): разместить 20 ордеров через API с ретраем на 503
    (до 3 попыток, свой Idempotency-Key на каждый ордер). В конце через API ордеров ровно 20.
    Вторая версия — ретрай БЕЗ ключа: сколько получилось? Запусти пару раз. Объясни в «Ответах».
    (Пополнение баланса тоже может упасть на 503 — подумай, как не задвоить его: проверить баланс
    перед повтором.)

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Зачем в UI-тестах API?
    2. Как сделать API-запрос из Playwright на Python?
    3. Как открыть браузер уже залогиненным, если пользователь создан через API?
    4. Когда проверять результат UI-действия через API?
    5. Как убираешь тестовые данные?
    6. Подготовка через API падает на нестабильном стенде. Что делать?
```

<a id="u5-2"></a>

## U5.2 Тестовые данные

*Теория: `practice/u5_02_test_data.md`*

Задания: `tests/ui/test_u5_02_test_data.py`, код — `ui_framework/data/`, `tests/ui/data/`.

План: стратегии данных (seed или генерация на тест); Faker и его ловушки; фабрики «пользователь /
пользователь с балансом / с ордерами»; builder; уникальность при параллельном запуске и префикс
прогона; данные из JSON/CSV для `parametrize`; уборка — через API, по префиксу через SQL;
файлы и `tmp_path`; общий стенд с чужими данными.

---

#### 1. Стратегии данных

| | Статичные (seed) | Генерируемые на тест |
|---|---|---|
| Что | заранее созданные пользователи и справочники | тест создаёт всё, что ему нужно |
| Плюсы | быстро; есть «тяжёлые» данные (история за год) | изоляция; тесты независимы; можно параллельно |
| Минусы | тесты делят данные → ломают друг друга; seed «портится» | дольше (лечится API); мусор (лечится уборкой) |
| Когда | **только чтение**: справочники, отчёты, большие объёмы | **всё, что меняет состояние** |

Правило по умолчанию: **каждый тест создаёт своё**. Seed — осознанное исключение для read-only тестов.

##### Seed должен быть идемпотентным

Запускается перед каждым прогоном и не должен ломаться от того, что данные уже есть:

```python
def ensure_user(api, email, password) -> ExchangeApi:
    r = api.ctx.post("/auth/register", data={"email": email, "password": password})
    if r.status not in (201, 409):                 # 409 email_taken — уже есть, это ок
        raise AssertionError(r.text())
    api.login(email, password)
    return api


def ensure_balance(api, asset, target: Decimal) -> None:
    current = next(to_decimal(b["available"]) for b in api.balances() if b["asset"] == asset)
    if current < target:
        api.deposit(asset, str(target - current))  # довести до нужного, а не «добавить ещё»
```

«Довести до» вместо «добавить» — иначе каждый прогон увеличивает баланс seed-пользователя.

---

#### 2. Faker

```python
from faker import Faker

fake = Faker("ru_RU")
fake.name(), fake.email(), fake.password(length=12), fake.date_of_birth(), fake.city()
```

##### Ловушка 1: плагин pytest сидирует каждый тест одинаково

Faker ставит **pytest-плагин** с фикстурой `faker`. Он сидирует генератор **нулём перед каждым тестом**
— поэтому значения в разных тестах **совпадают**. Проверено у нас:

```
test_a: achang@example.org  tn8Em4__*%zP
test_b: achang@example.org  tn8Em4__*%zP
```

Второй тест регистрации получит 409. Сид меняется фикстурой `faker_seed`, но для уникальных полей
это не решение.

##### Ловушка 2: Faker не гарантирует уникальность

Даже без сида — на тысячах прогонов будут повторы. `fake.unique.email()` уникален только **внутри
одного процесса** и падает, когда варианты кончаются.

Итого: **уникальное поле — из uuid** (с читаемым префиксом), Faker — для «декоративных» полей,
где совпадение ничего не ломает. Воспроизводимость Faker (сид) полезна, когда нужно повторить
упавший тест с теми же данными — тогда сид печатают в лог.

---

#### 3. Фабрики

Фабрика — функция, которая создаёт **готовый объект нужного состояния** со значениями по умолчанию:

```python
@dataclass
class Trader:
    email: str
    password: str
    api: ExchangeApi
    orders: list[dict] = field(default_factory=list)


def create_trader(ctx, password, balance: dict[str, str] | None = None,
                  orders: list[OrderData] = ()) -> Trader:
    email = unique_email("trader")
    api = ExchangeApi(ctx)
    api.register(email, password)
    api.login(email, password)
    for asset, amount in (balance or {}).items():
        api.deposit(asset, amount)
    created = [api.place_order(o) for o in orders]
    return Trader(email, password, api, created)


trader = create_trader(ctx, pw)                                         # просто пользователь
rich = create_trader(ctx, pw, balance={"USDT": "1000"})                 # с балансом
busy = create_trader(ctx, pw, balance={"USDT": "1000"},
                     orders=[OrderData(price="10"), OrderData(price="20")])   # с ордерами
```

Как фикстура — фабрика с уборкой (U4.3, U5.1): запоминает созданных и после теста отменяет их ордера.

Библиотеки: `factory_boy`, `polyfactory` — генерируют модели по описанию. Для API-подготовки
часто проще своя функция, как выше.

---

#### 4. Builder

Когда вариантов много и важен порядок шагов, фабрика с десятком аргументов становится нечитаемой.
Builder — пошаговая сборка:

```python
class TraderBuilder:
    def __init__(self, ctx, password):
        self._ctx, self._password = ctx, password
        self._balance: dict[str, str] = {}
        self._orders: list[OrderData] = []

    def with_balance(self, asset: str, amount: str) -> "TraderBuilder":
        self._balance[asset] = amount
        return self

    def with_order(self, order: OrderData) -> "TraderBuilder":
        self._orders.append(order)
        return self

    def create(self) -> Trader:
        return create_trader(self._ctx, self._password, self._balance, self._orders)


seller = (TraderBuilder(ctx, pw)
          .with_balance("ETH", "2")
          .with_order(OrderData(side="SELL", price="350", quantity="2"))
          .create())
```

| | Фабрика с kwargs | Builder |
|---|---|---|
| Мало вариантов | ✅ проще | лишний класс |
| Много опций, шаги в порядке | аргументов слишком много | ✅ читается как описание |
| Python-идиома | ✅ значения по умолчанию, `replace()` | реже, но уместен для сложных объектов |

---

#### 5. Уникальность при параллельном запуске и префикс прогона

uuid уникален и в параллели. Но для отладки и уборки полезен **читаемый префикс**:

```python
RUN_ID = os.getenv("TEST_RUN_ID") or datetime.now().strftime("%m%d%H%M%S")
WORKER = os.getenv("PYTEST_XDIST_WORKER", "gw0")        # при запуске через xdist (U5.3)


def unique_email(role: str = "user") -> str:
    return f"ui_{RUN_ID}_{WORKER}_{role}_{uuid4().hex[:6]}@test.com"
```

- по email сразу видно: какой прогон, какой воркер, какая роль;
- по префиксу `ui_{RUN_ID}_` можно найти и удалить **все** данные прогона;
- `RUN_ID` в CI задают снаружи (номер сборки), чтобы все воркеры использовали **один**.
  Без этого каждый процесс xdist посчитает своё время запуска.

---

#### 6. Данные из JSON / CSV для parametrize

Табличные кейсы удобнее держать файлом — их правит и аналитик, и тестировщик без кода:

`tests/ui/data/invalid_orders.json`:

```json
[
  {"id": "пустая цена",          "price": "",    "quantity": "1", "field": "price"},
  {"id": "отрицательная цена",   "price": "-1",  "quantity": "1", "field": "price"},
  {"id": "нулевое количество",   "price": "10",  "quantity": "0", "field": "quantity"}
]
```

```python
DATA = Path(__file__).parent / "data"


def load_cases(name: str) -> list:
    cases = json.loads((DATA / name).read_text(encoding="utf-8"))
    return [pytest.param(c, id=c["id"]) for c in cases]


@pytest.mark.parametrize("case", load_cases("invalid_orders.json"))
def test_invalid_order(dashboard, case): ...
```

CSV — `csv.DictReader`; все значения придут **строками** (для нашего стенда это даже удобно — суммы и так строки).

Где лежат: файлы **кейсов** конкретных тестов — рядом с тестами (`tests/ui/data/`); **модели**
и генераторы — во фреймворке (`ui_framework/data/`). Загрузка — при сборке тестов (на уровне модуля),
поэтому `tmp_path` и фикстуры тут недоступны.

---

#### 7. Уборка

| Способ | Когда |
|---|---|
| через API в `yield`-фикстуре | основной: тест убирает своё (U5.1) |
| «каждый тест создаёт своё» + уникальные данные | мусор остаётся, но не мешает — если ресурс не общий |
| **по префиксу** после прогона | когда API удаления нет, или тест упал до уборки |
| пересоздание окружения | эфемерный стенд на прогон — лучший вариант, если есть |

##### По префиксу через SQL

У стенда нет API удаления пользователя. Тестовое окружение — наше, база доступна
(`postgresql://exchange:exchange@localhost:5432/exchange`, модуль F3). Внешние ключи **без каскада**,
поэтому порядок важен — сначала зависимые таблицы:

```python
def delete_users_by_prefix(dsn: str, prefix: str) -> int:
    pattern = prefix + "%"
    with psycopg.connect(dsn) as conn:
        ids = "SELECT id FROM users WHERE email LIKE %s"
        for table in ("idempotency_keys", "orders", "balances"):
            conn.execute(f"DELETE FROM {table} WHERE user_id IN ({ids})", (pattern,))
        return conn.execute("DELETE FROM users WHERE email LIKE %s", (pattern,)).rowcount
```

Правила: **только** в окружениях, где это разрешено (docker, local — да; общий stage — нет:
флаг в Settings); префикс должен быть **достаточно узким** — `ui_0910153000_`, а не `ui_`;
вызывать в session-teardown или отдельной командой. Значения — параметрами (`%s`), не f-строкой.

---

#### 8. Файлы и `tmp_path`

```python
def test_export(tmp_path):                         # своя временная папка на тест
    path = tmp_path / "orders.csv"
    ...


@pytest.fixture(scope="session")
def shared_dir(tmp_path_factory):                  # на весь прогон
    return tmp_path_factory.mktemp("exports")
```

- pytest создаёт папку сам, хранит последние 3 прогона (`/tmp/pytest-of-<user>/`), чистить руками не нужно;
- в папку проекта файлы тестов **не пишут** — мусор в git, конфликты в параллели;
- генерация файлов для загрузки: CSV — модуль `csv`; картинка — `page.screenshot(path=...)` или
  Pillow; большой файл — `path.write_bytes(os.urandom(5 * 1024 * 1024))`.
  Загрузка через `set_input_files` — в U3 (на стенде загрузки нет).

---

#### 9. Общий стенд с чужими данными

То, что мы видели в U1.4: в стакане висят чужие ордера, наш исполнился об них.
- не полагаться на «пусто»: проверять **свои** данные (свой пользователь, свой id), а не «в системе 0 ордеров»;
- данные, которые **не пересекаются** с чужими: уникальные имена, цены в «своём» диапазоне;
- если пересечение неизбежно — изолированное окружение (своя база, docker на прогон) или
  отдельный тенант / префикс;
- убирать за собой — чтобы не быть «чужими данными» для других.

---

#### Собес: вопросы и ответы

**1. Как вы готовите тестовые данные?**
> По умолчанию каждый тест создаёт своё через API: фабрики «пользователь», «с балансом», «с ордерами»,
> уникальные поля из uuid с префиксом прогона. Статичный seed — только для read-only тестов и идемпотентный:
> «создать, если нет» и «довести до нужного значения». Табличные кейсы — в JSON/CSV для parametrize.

**2. Как чистите данные?**
> Тест убирает своё через API в teardown фикстуры. Если удалить через API нельзя или тест упал до уборки —
> уборка по префиксу прогона после завершения, на тестовом окружении можно напрямую в базе с учётом
> внешних ключей. Лучший вариант — эфемерное окружение на прогон, которое просто удаляется.

**3. Общий стенд с чужими данными — что делать?**
> Не полагаться на пустое состояние, проверять только свои сущности по id. Делать данные, которые не
> пересекаются с чужими. Убирать за собой. Если этого мало — добиваться изолированного окружения
> или отдельного тенанта.

**4. Faker — плюсы и подводные камни?**
> Удобно генерировать правдоподобные данные и локали. Но уникальность он не гарантирует, а pytest-плагин
> по умолчанию сидирует каждый тест одинаково — значения в разных тестах совпадают. Поэтому ключевые поля
> делаю из uuid, Faker — для декоративных, сид печатаю, если нужна воспроизводимость.

**5. Фабрика или builder?**
> Для небольшого числа вариантов — функция-фабрика со значениями по умолчанию, это идиоматично для Python.
> Builder — когда опций много и важна последовательность шагов: читается как описание объекта.

**6. Как обеспечить уникальность при параллельном запуске?**
> uuid в ключевых полях. Плюс читаемый префикс: id прогона, общий для всех воркеров, и id воркера —
> чтобы по данным было видно, откуда они, и чтобы можно было убрать всё за прогон.
> Никаких общих фиксированных имён и счётчиков в файлах.

**7. Где хранить данные для параметризации?**
> Кейсы — в JSON или CSV рядом с тестами, загружаю при сборке и превращаю в `pytest.param` с читаемыми id.
> Модели и генераторы — во фреймворке. Временные файлы — в `tmp_path`, не в папке проекта.

### Задания — `tests/ui/test_u5_02_test_data.py`

```text
U5. Урок 2 — тестовые данные.

Теория: practice/u5_02_test_data.md
Код: ui_framework/data/{factories,seed,generators}.py, ui_framework/utils/db_cleanup.py,
     файлы кейсов — tests/ui/data/ (папка создана, файлы пишешь сам).
Запуск:
    uv run pytest tests/ui/test_u5_02_test_data.py -v -s

Задача 1. Ловушка Faker.
    Два теста, оба берут фикстуру faker и регистрируют через API пользователя с faker.email().
    Запусти вместе — второй получит 409. Почему? Исправь генератор так, чтобы email был уникальным,
    а Faker остался для пароля. Объясни в «Ответах».

Задача 2. Фабрика (factories.py).
    Trader (dataclass: email, password, api, orders) и create_trader(ctx, password, balance=None, orders=()).
    Фикстура trader_factory — с уборкой открытых ордеров (переиспользуй api_user из U5.1 или замени им).
    Тест: пользователь с балансом USDT 1000 и двумя ордерами — открыть кабинет токеном (U5.1),
    в таблице 2 строки, заблокировано == сумма cost ордеров (format_amount из U4.4).

Задача 3. Builder.
    TraderBuilder: with_balance, with_order, create. Тест — сделка: продавец (builder) с SELL,
    покупатель (builder) с BUY по той же цене (isolated_price). Через UI проверь, что у обоих FILLED.
    В «Ответах»: фабрика или builder для твоих сценариев — что выберешь и почему.

Задача 4. Идемпотентный seed (seed.py).
    ensure_user(ctx, email, password) и ensure_balance(api, asset, target).
    Session-фикстура seed_trader: email фиксированный (из Settings, например seed_trader@test.com),
    баланс USDT доведён до 5000.
    Тест (read-only!): кабинет seed-пользователя токеном, доступно USDT 5000.
    Запусти дважды подряд — баланс не вырос, 409 не уронил подготовку.
    В «Ответах»: почему этот пользователь годится только для read-only тестов.

Задача 5. Кейсы из файлов.
    а) tests/ui/data/invalid_orders.json — минимум 5 кейсов (id, price, quantity, field).
       Один UI-тест с parametrize из файла: ошибка формы ордера содержит field. Читаемые id в отчёте.
    б) tests/ui/data/deposit_amounts.csv (amount,valid) — валидные и невалидные суммы пополнения;
       тест через API: валидные → 200, невалидные → 422.

Задача 6. Префикс прогона и уборка по нему.
    generators.unique_email(role): ui_<RUN_ID>_<WORKER>_<role>_<uuid6>@test.com (раздел 5 теории).
    db_cleanup.delete_users_by_prefix(dsn, prefix) — с правильным порядком таблиц.
    Settings: db_dsn и флаг allow_db_cleanup (true для docker/local, false для stage).
    Session-фикстура в tests/conftest.py: после прогона удаляет пользователей своего RUN_ID, если разрешено,
    и печатает, сколько удалила. Проверь в psql, что чужие (не этого прогона) пользователи на месте.

Задача 7. tmp_path.
    Пользователь с тремя ордерами (через фабрику). Выгрузи ордера через API в CSV в tmp_path
    (колонки как в UI: Пара, Сторона, Цена, Кол-во, Статус). Прочитай CSV обратно и сравни
    с таблицей в UI (колонки через компонент Table из U4.2). Путь к файлу выведи (-s) — где он лежит?

Задача 8. Письменно в «Ответах».
    Команда делит один stage с другой командой; их тесты создают ордера в том же стакане, иногда
    исполняя ваши. Предложи 3 решения — от быстрого к правильному, с плюсами и минусами.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как вы готовите тестовые данные?
    2. Как чистите данные?
    3. Общий стенд с чужими данными — что делать?
    4. Faker — плюсы и подводные камни?
    5. Фабрика или builder?
    6. Как обеспечить уникальность при параллельном запуске?
    7. Где хранить данные для параметризации?
```

<a id="u5-3"></a>

## U5.3 Storage_state, роли, изоляция и параллельный запуск

*Теория: `practice/u5_03_storage_state_parallel.md`*

Задания: `tests/ui/test_u5_03_storage_state_parallel.py`, код — `ui_framework/fixtures/auth.py`.

План: три уровня «не логиниться в каждом тесте»; логин один раз на сессию, на воркер, на все
воркеры (filelock); истечение токена; роли; несколько пользователей в тесте; что изолирует context,
а что нет; pytest-xdist — запуск, распределение, хуки; гонки данных в параллели (проверено на стенде);
что не параллелить.

---

#### 1. Три уровня: как не логиниться в каждом тесте

| Уровень | Как | Скорость | Изоляция данных |
|---|---|---|---|
| UI-логин в каждом тесте | форма входа (U1.4 `logged_in_page`) | медленно | полная |
| **API-логин в каждом тесте** | пользователь и токен через API → storage_state (U5.1) | быстро | **полная** |
| **общий state на сессию** | один пользователь, токен получен один раз | быстрее всего | **общая**: тесты делят данные пользователя |

Для нашего стенда API-логин стоит ~100 мс — второй уровень почти всегда достаточен и не создаёт
общих данных. Третий — когда логин дорогой (SSO, 2FA, капча) или нужен «тяжёлый» seed-пользователь
для read-only тестов.

---

#### 2. Логин один раз

##### На сессию (без xdist)

```python
@pytest.fixture(scope="session")
def trader_state(api_context, settings) -> dict:
    api = ensure_user(api_context, settings.seed_email, settings.user_password.get_secret_value())
    return token_state(settings.base_url, api.token, settings.seed_email)   # dict для storage_state


@pytest.fixture
def trader_page(new_context, trader_state) -> DashboardPage:
    page = new_context(storage_state=trader_state).new_page()   # context НОВЫЙ, общий только токен
    return DashboardPage(page).open().wait_loaded()
```

Session-фикстура не может взять `page` или `new_context` (function-scope, `ScopeMismatch`, U1.4) —
поэтому она готовит только **данные** (dict), а context создаёт function-фикстура.

##### На воркер (xdist)

Каждый воркер xdist — **отдельный процесс** со своей сессией pytest. Session-фикстура выполнится
**на каждом** воркере: при `-n 4` — 4 логина. Обычно это нормально.

##### На все воркеры: filelock

Если логин дорогой — один воркер логинится, остальные читают файл:

```python
from filelock import FileLock


@pytest.fixture(scope="session")
def trader_state(tmp_path_factory, api_context, settings) -> dict:
    root = tmp_path_factory.getbasetemp().parent         # общая папка всех воркеров прогона
    path = root / "trader_state.json"
    with FileLock(str(path) + ".lock"):
        if path.is_file():
            return json.loads(path.read_text())
        state = ...                                       # логин
        path.write_text(json.dumps(state))
        return state
```

Проверено на стенде: 4 воркера, 8 тестов — логин выполнился **один раз** (на gw2), остальные
прочитали готовый state. Это рецепт из документации pytest-xdist. Без xdist `getbasetemp().parent`
тоже работает — просто воркер один.

---

#### 3. Истечение токена

Токен стенда живёт **15 минут**. Session-state на прогон длиной 40 минут — через 15 минут фронт
получит 401 и сам разлогинится (U5.1, задача 8): тесты начнут падать «на форме входа».

Решения:
- **проверять срок** перед выдачей state и перелогиниваться:
  ```python
  def token_expires_in(token: str) -> float:
      payload = token.split(".")[1]
      payload += "=" * (-len(payload) % 4)                 # base64url без выравнивания
      exp = json.loads(base64.urlsafe_b64decode(payload))["exp"]
      return exp - time.time()
  ```
  Подпись не проверяем — нам нужен только `exp`; секрет тестам не нужен;
- state на **модуль** вместо сессии — если модуль короче TTL;
- API-логин на каждый тест — проблемы нет вовсе.

---

#### 4. Роли

На реальных проектах: гость, пользователь, менеджер, админ. Каждой роли — свой state:

```python
ROLES = {
    "trader": lambda api, s: ensure_user(api, s.seed_email, ...),      # seed с балансом, read-only
    "newbie": lambda api, s: fresh_user(api, s),                       # новый пользователь без денег
}


@pytest.fixture
def page_as(new_context, role_states):
    def _open(role: str) -> DashboardPage:
        page = new_context(storage_state=role_states[role]).new_page()
        return DashboardPage(page).open().wait_loaded()
    return _open


def test_two_roles(page_as):
    trader = page_as("trader")
    newbie = page_as("newbie")
```

Или маркером: `@pytest.mark.role("admin")` → фикстура читает `request.node.get_closest_marker("role")`
(U4.3). Файлы state на диске — `.auth/<role>.json` (в `.gitignore`, U2.3).

На нашем стенде ролей нет — «роли» это разные виды пользователей: богатый seed, новый пустой.

---

#### 5. Что изолирует context, а что нет

| Изолировано новым context | НЕ изолировано |
|---|---|
| cookies, localStorage, кэш, вкладки | **данные пользователя на сервере**: баланс, ордера |
| настройки (viewport, locale) | **общие ресурсы**: стакан ордеров, справочники |
| | сам токен — если state общий |

Общий state = общий пользователь. Два теста под ним одновременно: первый отменяет «все ордера»,
второй в это время проверяет «у меня 3 ордера». Правило: под общим пользователем — **только чтение**,
или тесты, которые проверяют **свои** сущности по id и терпимы к чужим.

---

#### 6. pytest-xdist

```bash
uv run pytest tests/ui -n 4                 # 4 процесса
uv run pytest tests/ui -n auto              # по числу ядер
uv run pytest tests/ui -n 4 --dist loadfile # файл целиком на одном воркере
```

| `--dist` | Как распределяет |
|---|---|
| `load` (по умолч.) | по одному тесту свободному воркеру |
| `loadscope` | тесты одного модуля/класса — на одном воркере (module-фикстуры не дублируются) |
| `loadfile` | файл целиком на одном воркере |
| `loadgroup` | по `@pytest.mark.xdist_group("name")` — группа на одном воркере |

Полезное:
- фикстура `worker_id` — `"gw0"`, `"gw1"`… или `"master"` без xdist;
- переменная `PYTEST_XDIST_WORKER` — то же в окружении (U5.2, префикс email);
- `testrun_uid` — общий id прогона у всех воркеров;
- код только на **контроллере** (не на воркерах): `if not hasattr(config, "workerinput"):` в `pytest_configure`;
- `-s` / `print` из воркеров не видно в консоли — логируй или смотри отчёт;
- pytest-playwright работает с xdist: у каждого воркера свой браузер.

##### Ловушка: `base_url` из `pyproject.toml` под xdist

Проверено у нас: `uv run pytest tests/ui/test_u1_04_context_pytest.py -n 4` → все тесты падают с
`Cannot navigate to invalid URL`. Причина — в `pytest-base-url`: его `pytest_configure` **сразу выходит
на воркерах**, и значение из ini до них не доходит. `--base-url` в командной строке передаётся воркерам —
с ним 9/9 зелёные. Своя фикстура `base_url` из Settings (U4.3) решает это насовсем.

---

#### 7. Гонки данных в параллели

##### Seed без блокировки

Проверено на стенде: 4 воркера одновременно выполняют «довести баланс seed-пользователя до 5000».
Каждый прочитал 0, каждый пополнил на 5000 → **10000**. Идемпотентный seed (U5.2) идемпотентен
только при **последовательном** запуске.

Решения:
- seed на **контроллере** до старта воркеров (`pytest_configure` без `workerinput`) или отдельной командой
  перед прогоном (в CI — отдельный шаг);
- seed под `FileLock`, как общий state.

##### Общий стакан

`isolated_price()` (U5.2) брал случайную цену 300–499. В параллели **свои же** тесты сделок могут
выбрать одну цену — продавец теста A исполнится с покупателем теста B. Шанс на прогон мал, но на
сотнях прогонов это флейк «раз в неделю».

Решение для нашего стенда — уникальная дробная часть цены. Стенд принимает до 18 знаков после запятой:

```python
def isolated_price(low: int = 300, high: int = 499) -> str:
    return f"{random.randint(low, high)}.{uuid4().int % 10**9:09d}"     # 350.123456789
```

Совпадение двух цен — один на миллиард. Сумма сделки посчитается в Decimal (U4.4) — проверки
балансов остаются точными.

##### Что не параллелить

- тесты, меняющие **глобальное** состояние (настройки системы, общие справочники, курсы);
- тесты, которые проверяют «в системе всего N…»;
- тяжёлые сценарии, которые сами по себе нагружают стенд.

Их — в `xdist_group` (на один воркер) или отдельным последовательным прогоном с маркером.

---

#### Собес: вопросы и ответы

**1. Как не логиниться в каждом тесте?**
> Логин через API вместо UI и storage_state: браузер стартует уже залогиненным. Если логин дорогой —
> один раз на сессию, а в параллели — один раз на все воркеры через файл с блокировкой. Context при этом
> новый на каждый тест, общий только токен. Помню про истечение токена: проверяю срок и перелогиниваюсь.
> Тесты логина и логаута идут без сохранённого state.

**2. Как готовить данные быстрее, чем через UI?**
> Через API: пользователь, баланс, ордера — миллисекунды вместо секунд. Через UI — только то, что
> проверяется. Для read-only тестов — заранее подготовленный seed. Уборка тоже через API.

**3. Как работать с ролями?**
> State на каждую роль, получается через API один раз. Фикстура-фабрика `page_as(role)` или маркер
> `role` на тесте. Файлы state — вне git. Несколько ролей в одном тесте — несколько context.

**4. Чем рискуешь, когда тесты делят одного пользователя?**
> Context изолирует браузер, но не данные на сервере. Тесты под одним пользователем видят и меняют
> общий баланс и ордера — особенно в параллели. Под общим пользователем — только чтение или проверки
> строго своих сущностей по id.

**5. Как запускаешь UI-тесты параллельно?**
> pytest-xdist: `-n auto`, каждый воркер — отдельный процесс со своим браузером и своей session-областью.
> Распределение — load по умолчанию, loadscope или loadgroup, когда тесты должны держаться вместе.
> Seed — на контроллере или под блокировкой. Данные — уникальные, с id воркера в префиксе.
> Тесты на глобальное состояние — в отдельной группе или последовательно.

**6. Какие проблемы появляются при параллельном запуске?**
> Гонки на общих данных: два воркера одновременно «доводят» seed — данные задваиваются; общие ресурсы —
> сделки между ордерами разных тестов. Session-фикстуры выполняются на каждом воркере. Настройки, которые
> плагины применяют только на контроллере, — как base_url из ini у pytest-base-url. Вывод print не виден.
> Лечится изоляцией данных, блокировками и проверкой, что тесты не зависят друг от друга.

### Задания — `tests/ui/test_u5_03_storage_state_parallel.py`

```text
U5. Урок 3 — storage_state, роли, изоляция и параллельный запуск.

Теория: practice/u5_03_storage_state_parallel.md
Код: ui_framework/fixtures/auth.py (заготовка; подключи в pytest_plugins).
Подготовка: uv sync (поставит pytest-xdist и filelock).
Запуск:
    uv run pytest tests/ui/test_u5_03_storage_state_parallel.py -v
    uv run pytest tests/ui/test_u5_03_storage_state_parallel.py -n 4

Задача 1. token_state(base_url, token, email) -> dict для storage_state (обобщи код из U5.1).
    token_expires_in(token) -> секунды до истечения (раздел 3 теории).
    Тест без браузера: свежий токен живёт ~900 с (допуск ±30).

Задача 2. Session-state.
    trader_state (session): seed-пользователь (ensure_user из U5.2), токен — через FileLock,
    чтобы при -n 4 логин был один. Запиши каждый реальный логин в лог-файл рядом со state
    (имя воркера, worker_id) — так проверишь, сколько было логинов.
    trader_page (function): новый context с trader_state → DashboardPage.
    Три read-only теста под trader_page. Прогони с -n 3: сколько строк в логе логинов?
    Если state протух (token_expires_in < 60) — перелогиниться.

Задача 3. Роли.
    page_as(role) — роли "trader" (seed, read-only) и "newbie" (новый пользователь через api_user).
    Тест: под trader доступно USDT == seed-баланс, под newbie — 0; оба в одном тесте, разные context.
    Вариант с маркером @pytest.mark.role("newbie") для фикстуры role_page — зарегистрируй маркер.

Задача 4. Что не изолирует context.
    Два теста под trader_page: первый создаёт и сразу отменяет ордер (уборка за собой обязательна),
    второй проверяет «у seed-пользователя 0 открытых ордеров». Запусти их вместе с -n 2 несколько раз
    (--count 5 из U2.4). Что видишь? Объясни в «Ответах» и почисти: что должно быть в тестах под общим
    пользователем, а что — нет. Убери нарушающий тест в xdist_group или переделай на своего пользователя.

Задача 5. base_url под xdist.
    Временно отключи свою фикстуру base_url (U4.3) и верни base_url в pyproject.
    uv run pytest tests/ui/test_u1_04_context_pytest.py -n 2 — что случилось? С --base-url? Почему?
    (Ответ в теории, раздел 6, — сначала попробуй объяснить сам, потом сверься.) Верни как было.

Задача 6. Гонка seed.
    Тест-демонстрация: 4 параллельных теста (parametrize range(4)), каждый «доводит баланс USDT»
    одного и того же нового пользователя (email — общий для прогона, через testrun_uid) до 5000
    функцией ensure_balance из U5.2. Запусти -n 4: какой баланс в итоге?
    Исправь: seed под FileLock. Снова -n 4 — ровно 5000.

Задача 7. Цена без пересечений.
    Обнови isolated_price (U5.2) по теории (уникальная дробная часть). Тест сделки (U5.2, задача 3)
    с parametrize range(6) и -n 3: все 6 зелёные, балансы точные (Decimal, format_amount).

Задача 8. Ускорение.
    Замерь весь набор tests/ui/test_u4_0*.py tests/ui/test_u5_0*.py: последовательно, -n 2, -n 4, -n auto.
    Запиши время в «Ответы». Почему ускорение не линейное?

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как не логиниться в каждом тесте?
    2. Как готовить данные быстрее, чем через UI?
    3. Как работать с ролями?
    4. Чем рискуешь, когда тесты делят одного пользователя?
    5. Как запускаешь UI-тесты параллельно?
    6. Какие проблемы появляются при параллельном запуске?
```

<a id="u5-4"></a>

## U5.4 Собес по модулю U5

*Теория: `practice/u5_04_interview.md`*

Задания: `tests/ui/test_u5_04_livecoding.py`, ревью — `practice/u5_04_review_me.py`.

План: шпаргалка по модулю; банк вопросов (ссылки на разделы «Собес» U5.1–U5.3 плюс новые
вопросы-сценарии и вопрос на проектирование); ключевые ответы на английском; на что смотреть
при ревью кода подготовки данных.

---

#### 1. Шпаргалка по модулю U5

**API внутри Playwright (U5.1)**
- через UI — только проверяемое; подготовка и уборка — через API;
- `playwright.request.new_context(base_url=...)` — отдельный клиент; `page.request` / `context.request` — делит cookies
  с браузером; в pytest `request` — это `FixtureRequest`, не HTTP-клиент;
- `data=dict` → JSON; `dispose()` в teardown;
- токен стенда в localStorage → `page.request` даёт 401; браузер логиним через **storage_state** с localStorage;
  `add_init_script` ломает логаут;
- UI-действие → проверка API: то, чего нет на экране, локализация фронт/бэк;
- повтор POST — только с `Idempotency-Key` (у стенда — `POST /orders`).

**Тестовые данные (U5.2)**
- по умолчанию «каждый тест создаёт своё»; seed — только read-only и идемпотентный («довести до»);
- Faker: плагин сидирует каждый тест одинаково, уникальность не гарантирует → ключевые поля из uuid;
- фабрики со значениями по умолчанию, builder — для многошаговой сборки;
- префикс `ui_<RUN_ID>_<WORKER>_<role>_<uuid>` — отладка и уборка за прогон;
- кейсы — в JSON/CSV рядом с тестами → `pytest.param(..., id=...)`;
- уборка: API в teardown → по префиксу (SQL, порядок FK, только где разрешено) → эфемерное окружение;
- `tmp_path` / `tmp_path_factory` для файлов.

**storage_state и параллель (U5.3)**
- API-логин на тест (~100 мс) — обычно достаточно; общий state — для дорогого логина и read-only;
- session-фикстура готовит dict, function-фикстура создаёт context;
- под xdist session = на воркер; на все воркеры — `FileLock` в `getbasetemp().parent`;
- токен 15 минут: `exp` из payload, перелогин;
- context не изолирует данные на сервере;
- xdist: `-n auto`, `--dist load/loadscope/loadfile/loadgroup`, `worker_id`, `testrun_uid`, контроллер vs воркер;
- ловушки: `base_url` из ini не доходит до воркеров (pytest-base-url), seed без блокировки задваивает,
  общий стакан — уникальная дробная часть цены.

---

#### 2. Банк вопросов

Вопросы с ответами в уроках: U5.1 — 6, U5.2 — 7, U5.3 — 6. Ниже — новые: сценарии и проектирование.
На собесе их задают именно так — «вот ситуация, что будешь делать».

**1. Набор из 300 UI-тестов идёт 50 минут. Как ускорить, не теряя покрытия?**
> Сначала измерю, на что уходит время: подготовка, ожидания, сами проверки. Обычно основное — подготовка
> через UI: перевожу регистрацию, пополнение, создание сущностей на API, браузер логиню storage_state.
> Убираю sleep и лишние перезагрузки. Потом параллель — xdist с изоляцией данных. Тесты, которые проверяют
> одно и то же на разных данных, — в API-уровень, в UI оставляю пользовательские сценарии.
> Smoke-набор на каждый PR, полный — ночью.

**2. Тесты зелёные по одному, а с `-n 4` падают случайные. Что проверишь?**
> Общие данные: один пользователь или seed на несколько тестов, фиксированные имена, общие ресурсы вроде
> стакана. Session-фикстуры, которые должны выполняться один раз, а выполняются на каждом воркере, — гонки
> при создании. Зависимость от порядка. Настройки, которые не доходят до воркеров. Запущу проблемный тест
> вместе с подозреваемыми соседями, посмотрю trace и данные по префиксу воркера.

**3. На CI через 15–20 минут прогона тесты начинают падать на форме входа. Почему?**
> Похоже на истечение токена в общем storage_state: получили один раз в начале, а он живёт 15 минут.
> Проверю exp в токене. Решения — перелогин при скором истечении, state на модуль, или API-логин
> на каждый тест — он дешёвый.

**4. Подготовка данных через API на stage иногда падает с 503. Что делать?**
> Различать идемпотентные и нет. GET и запросы с ключом идемпотентности повторяю с паузой из Retry-After.
> POST без ключа не повторяю вслепую: если ответ потерялся после обработки, повтор задвоит данные — сначала
> проверяю состояние (создалось ли), потом решаю. Если сбоев много — это проблема окружения, сообщаю,
> а не прячу ретраями.

**5. Чужая команда на общем stage удаляет «лишних» пользователей, и ваши тесты падают посреди прогона.**
> Краткосрочно — свой префикс и договорённость, что чужие префиксы не трогают; пользователь создаётся
> на тест и живёт секунды, а не весь прогон. Правильно — изолированное окружение или тенант на команду,
> или эфемерный стенд на прогон. Это вопрос к процессу, не только к тестам.

**6. Спроектируй подготовку данных для UI-тестов биржи (вопрос на проектирование, 5–7 минут).**
> План ответа:
> 1) принципы: каждый тест создаёт своё через API, UI — только проверяемое;
> 2) слой: API-клиент → фабрики (пользователь, с балансом, с ордерами), builder для сделок;
>    модели на dataclass; генераторы с префиксом прогона;
> 3) авторизация: API-логин → storage_state; дорогие роли — один раз на воркер/прогон с блокировкой;
>    контроль срока токена;
> 4) параллель: xdist, уникальные данные, общий стакан — непересекающиеся цены; seed на контроллере;
> 5) уборка: API в teardown, по префиксу после прогона, флаг «можно ли» в конфиге окружения;
> 6) нестабильность: ретраи только идемпотентных, ключи идемпотентности;
> 7) что показал бы в отчёте: id прогона, пользователи теста, ответы API при падении.

**7. Что лучше — один длинный E2E-тест «зарегистрироваться → пополнить → торговать → вывести»
или несколько коротких?**
> Несколько коротких с подготовкой через API: каждый проверяет одно, падение сразу указывает место,
> они параллелятся. Один-два длинных сквозных сценария оставляю как smoke пользовательского пути —
> но их немного и они не заменяют короткие.

---

#### 3. Ключевые ответы на английском

**How do you prepare test data for UI tests?**
> Each test creates its own data through the API: users, balances, orders. The UI is used only for
> the part the test actually verifies. Unique values come from UUIDs with a run prefix, so tests can run
> in parallel and data can be cleaned up per run. Static seed data is only for read-only tests.

**How do you avoid logging in through the UI in every test?**
> I log in through the API and pass the token to the browser via storage state, so the page opens
> already authenticated. For expensive logins I do it once per worker or once per run with a file lock,
> and I check token expiry.

**How do you clean up test data?**
> In fixture teardown through the API. If something can't be deleted through the API, or the test died
> before teardown, there's a cleanup by run prefix after the run. The best option is an ephemeral
> environment per run.

**What breaks when you run UI tests in parallel?**
> Shared data — the same user, seed data, or shared resources like an order book. Session fixtures run
> per worker, so one-time setup can race. I isolate data per test, use locks for shared setup, and keep
> tests that touch global state in a separate serial group.

---

#### 4. Ревью кода подготовки данных: на что смотреть

- [ ] подготовка через UI там, где тест её не проверяет;
- [ ] фиксированные email / имена / цены — коллизии между прогонами и воркерами;
- [ ] Faker для уникальных полей;
- [ ] seed «добавить ещё» вместо «довести до»; seed без блокировки при xdist;
- [ ] общий пользователь в тестах, которые меняют его данные;
- [ ] нет уборки; уборка падает на «уже удалено»; уборка опасным широким префиксом;
- [ ] повтор неидемпотентного POST;
- [ ] `add_init_script` для логина;
- [ ] session-фикстура берёт `page` / `new_context`;
- [ ] токен из session-state без контроля срока;
- [ ] `dispose()` для API-контекста;
- [ ] секреты в коде, в шагах Allure, в логах;
- [ ] SQL с f-строкой вместо параметров.

### Задания — `tests/ui/test_u5_04_livecoding.py`

```text
U5. Урок 4 — собес по модулю U5.

Теория и банк вопросов: practice/u5_04_interview.md
Запуск:
    uv run pytest tests/ui/test_u5_04_livecoding.py -v

Правила лайвкодинга: засекай время; не подглядывай в свои решения U5.1–U5.3 до конца задачи;
фреймворк (PO, API-клиент, фабрики, фикстуры) использовать можно и нужно — так и на собесе:
«вот наш фреймворк, допиши тест».

Задача 1. Ревью — 15 минут.
    practice/u5_04_review_me.py — минимум 12 проблем (строка, что не так, чем грозит, как исправить).
    НЕ запускай этот файл (предупреждение внутри). Ответы — в том файле.

Задача 2. Лайвкодинг «отмена ордера» — 15 минут.
    Подготовка ТОЛЬКО через API: пользователь с USDT 1000 и ордером BUY (цена — isolated_price) кол-во 2.
    Через UI: открыть кабинет токеном, отменить ордер кнопкой в его строке.
    Проверки: в UI статус CANCELED и кнопки нет, заблокировано 0, доступно 1000;
    через API — ордер CANCELED. Уборка — фикстурой.

Задача 3. Лайвкодинг «частичное исполнение» — 20 минут.
    Два пользователя через фабрику/builder: продавец SELL кол-во 3, покупатель BUY кол-во 1 по той же цене.
    У продавца в UI: PARTIALLY_FILLED, исполнено 1; затем покупатель через API докупает ещё 2 —
    у продавца в UI (без reload) FILLED. Балансы продавца в конце — проверь точно (Decimal).
    Должно быть зелёным при -n 3 и --count 3.

Задача 4. Лайвкодинг «таблица кейсов» — 10 минут.
    tests/ui/data/order_validation.csv: price, quantity, expected_status (201 / 422), id.
    Минимум 6 строк, включая границы (18 знаков после запятой — ок, 19 — нет; 0; отрицательное).
    Один API-тест с parametrize из CSV; читаемые id.

Задача 5. Устный собес — 25 минут.
    Диктофон. Вопросы 1–7 из раздела 2 теории + 5 случайных из «Собес» U5.1–U5.3.
    Вопрос 6 (проектирование) — 5–7 минут, по плану из теории, можно рисовать на бумаге.
    Затем 4 ответа из раздела 3 — на английском, вслух.
    В «Ответах» — номера, на которых «поплыл», и что добавить в ответ.

Задача 6. Итог модуля (письменно).
    Обнови ui_framework/README.md (U4.5): раздел «Данные и авторизация» — как устроены фабрики,
    логин токеном, уборка, запуск в параллели, ограничения (что нельзя параллелить, где нельзя
    чистить SQL).
```

### Файл для ревью — `practice/u5_04_review_me.py`

```python
"""U5.4, задача 1 — ревью conftest от «коллеги».

⚠️ НЕ ЗАПУСКАТЬ и не копировать в tests/: уборка в конце удаляет ВСЕХ пользователей стенда
с адресом на test.com (это одна из ошибок, которые надо найти). Только читать.

Это фикстуры подготовки данных для UI-тестов биржи. Работает «у него на машине».
Найди минимум 12 проблем: строка, что не так, чем грозит, как исправить.
Чек-лист — раздел 4 теории (practice/u5_04_interview.md). Ответы — внизу файла.
"""

import time

import pytest
from faker import Faker
from playwright.sync_api import Page

API = "http://localhost:8080"
DB = "postgresql://exchange:exchange@localhost:5432/exchange"
SEED_EMAIL = "seed@test.com"
PASSWORD = "Qwerty123!"


@pytest.fixture(scope="session")
def seed_user(page: Page):
    page.goto(f"{API}/app/")
    page.get_by_label("Email").fill(SEED_EMAIL)
    page.get_by_label("Пароль").fill(PASSWORD)
    page.get_by_role("button", name="Зарегистрироваться").click()
    time.sleep(3)
    return SEED_EMAIL


@pytest.fixture(scope="session")
def token(playwright):
    api = playwright.request.new_context(base_url=API)
    r = api.post("/auth/login", data={"email": SEED_EMAIL, "password": PASSWORD})
    print("logged in with", PASSWORD, r.json())
    return r.json()["access_token"]


@pytest.fixture
def rich_user(playwright, token):
    api = playwright.request.new_context(base_url=API)
    api.post(
        "/balances/deposit",
        data={"asset": "USDT", "amount": "1000"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return SEED_EMAIL


@pytest.fixture
def new_user(playwright, faker: Faker):
    api = playwright.request.new_context(base_url=API)
    email = faker.email()
    api.post("/auth/register", data={"email": email, "password": PASSWORD})
    return email


@pytest.fixture
def order(playwright, token):
    api = playwright.request.new_context(base_url=API)
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(3):
        r = api.post(
            "/orders",
            data={"symbol": "ETH-USDT", "side": "BUY", "price": "100", "quantity": "1"},
            headers=headers,
        )
        if r.status == 201:
            break
    yield r.json()
    api.delete(f"/orders/{r.json()['id']}", headers=headers)


@pytest.fixture
def browser_as_seed(context, token):
    context.add_init_script(f"localStorage.setItem('token', '{token}')")
    page = context.new_page()
    page.goto(f"{API}/app/")
    return page


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    import psycopg

    with psycopg.connect(DB) as conn:
        prefix = "%test.com"
        conn.execute(f"DELETE FROM orders WHERE user_id IN (SELECT id FROM users WHERE email LIKE '{prefix}')")
        conn.execute(f"DELETE FROM users WHERE email LIKE '{prefix}'")


# Ответы
"""
"""
```


---

# U6. Сеть и окружение браузера

<a id="u6-1"></a>

## U6.1 Перехват сети: page.route и моки

*Теория: `practice/u6_01_route_mocks.md`*

Задания: `tests/ui/test_u6_01_route_mocks.py`, код — `ui_framework/network/`.

План: зачем подменять бэкенд в UI-тестах; `page.route` / `context.route` и четыре ответа обработчика
(`fulfill`, `continue_`, `fallback`, `abort`); сопоставление URL (ловушка с query — проверено);
порядок обработчиков; моки ошибок, пустых и «невозможных» данных; изменение запроса и ответа «на лету»;
задержка и «придержанный» запрос; уборка моков; что мокать, а что нет.

Модуль U6: U6.1 page.route и моки → U6.2 HAR и page.clock → U6.3 окружение браузера и собес.

---

#### 1. Зачем подменять бэкенд

UI-тест на реальном бэкенде проверяет связку целиком, но некоторые состояния так не получить:

| Нужно проверить | Через реальный бэкенд | С моком |
|---|---|---|
| UI при 500 / 503 от сервера | ждать сбоя или ломать стенд | один `fulfill(status=500)` |
| сообщение при неизвестной ошибке (HTML вместо JSON) | почти никогда | `fulfill(body="<html>...")` |
| пустой список, 1000 строк, длинные значения | долго готовить | вернуть любой JSON |
| состояние, которое бэкенд не даёт создать (`PARTIALLY_FILLED` у BTC за секунду) | сделка двух пользователей | одна строка JSON |
| disabled-кнопка / спиннер во время запроса | запрос слишком быстрый | придержать запрос |
| нет сети | выключать сеть | `abort()` |

Это **тесты фронтенда в изоляции**: проверяем, как UI реагирует на ответ, а не что бэкенд ответит.

---

#### 2. page.route: обработчик и четыре ответа

```python
def handler(route: Route) -> None:
    route.fulfill(status=500, json={"error": {"code": "internal", "message": "Internal error"}})

page.route("**/orders", handler)
```

Обработчик **обязан** что-то сделать с `route` — иначе запрос висит (иногда это и нужно — раздел 6):

| Метод | Что делает |
|---|---|
| `route.fulfill(...)` | ответить **сам**, сервер не увидит запрос: `status`, `json=`, `body=`, `headers=`, `content_type=`, `path=` (файл) |
| `route.continue_(...)` | отправить на сервер, можно изменить `url`, `method`, `headers`, `post_data` |
| `route.fallback(...)` | передать **следующему** подходящему обработчику (а если их нет — на сервер) |
| `route.abort("failed")` | оборвать: для страницы это ошибка сети (`connectionrefused`, `timedout`, …) |
| `route.fetch()` | выполнить запрос на сервер и **получить ответ в тест**, чтобы изменить его и отдать через `fulfill(response=..., json=...)` |

`context.route(...)` — то же для всех страниц context (включая будущие вкладки). `page.route` — одна страница.

Обработчик ловит **все** методы: на `**/orders` попадают и `GET` опроса, и `POST` создания.
Фильтруй внутри:

```python
def only_post(route: Route) -> None:
    if route.request.method != "POST":
        return route.fallback()
    route.fulfill(status=500, json=...)
```

---

#### 3. Сопоставление URL

```python
page.route("**/orders", h)                      # glob
page.route(re.compile(r"/orders(\?|$)"), h)     # регулярка (search по полному URL)
page.route(lambda url: "/orders" in url, h)     # функция от строки URL
```

##### Ловушка: glob и query-строка

Проверено на стенде: после выбора фильтра «Статус» опрос идёт на `/orders?status=NEW`, и
обработчик `"**/orders"` его **не ловит**. Glob сопоставляется со **всем** URL, включая query.

| Шаблон | `/orders` | `/orders?status=NEW` |
|---|---|---|
| `"**/orders"` | ✅ | ❌ |
| `"**/orders?*"` | ❌ | ✅ |
| `re.compile(r"/orders(\?\|$)")` | ✅ | ✅ |

Мок «пустого списка» на `"**/orders"` перестанет работать, как только тест выберет фильтр, —
и тест неожиданно увидит настоящие данные.

`**` — любые символы включая `/`, `*` — любые кроме `/`. Правила glob у Playwright менялись между
версиями (особенно для `?` и `[]`), поэтому для всего, что сложнее `**/путь`, бери **регулярку** —
её поведение однозначно.

##### Порядок обработчиков

Подходят несколько — первым вызывается **последний зарегистрированный**. `fallback()` передаёт
предыдущему. Проверено: три обработчика на один URL — регулярка (зарегистрирована последней) видела
все запросы, glob'ы — только свои.

Это позволяет делать «базовый мок на весь тест + точечную замену для одного шага».

---

#### 4. Моки ответов на стенде

##### Ошибка сервера

```python
page.route("**/orders", lambda r: r.fulfill(
    status=500, json={"error": {"code": "internal", "message": "Internal error"}}
) if r.request.method == "POST" else r.fallback())
```

Как реагирует фронт (`app.js`, функция `errorText`) — проверено:

| Ответ | Что видит пользователь в форме ордера |
|---|---|
| 500 с JSON `{"error": {"message": "Internal error"}}` | `Internal error` |
| 502 с HTML `<html>Bad Gateway</html>` | `Что-то пошло не так` |
| 422 с `details` | `price: ...; quantity: ...` |

Отсюда тесты на **понятность ошибок**: что пользователь увидит, если бэкенд ответит неожиданно.

##### Пустой и «невозможный» список

```python
FAKE_ORDER = {
    "id": "fake-1", "symbol": "BTC-USDT", "side": "SELL", "type": "LIMIT",
    "price": "65000", "quantity": "0.5", "filled_quantity": "0.25",
    "status": "PARTIALLY_FILLED", "created_at": "...", "updated_at": "...",
}
page.route(re.compile(r"/orders(\?|$)"),
           lambda r: r.fulfill(json=[FAKE_ORDER]) if r.request.method == "GET" else r.fallback())
```

Мок должен соответствовать **контракту** API: все поля, правильные типы (суммы — строки).
Мок, который отличается от реального ответа, тестирует несуществующий бэкенд. Готовые ответы берут
из реальных (записать, `route.fetch()`, HAR — U6.2) или из схемы OpenAPI (`/openapi.json`).

##### Обрыв сети

```python
page.route("**/balances", lambda r: r.abort())
```

Проверено: фронт стенда **молча** оставляет старые балансы, в консоли — `Failed to load resource`
и необработанная ошибка `Failed to fetch`. Пользователь не узнает, что данные устарели. Такие находки —
повод для баг-репорта / UX-задачи.

Слушать ошибки страницы в тесте:

```python
errors = []
page.on("pageerror", lambda e: errors.append(str(e)))
page.on("console", lambda m: m.type == "error" and errors.append(m.text))
```

---

#### 5. Изменение запроса и ответа «на лету»

##### Изменить запрос

```python
def change_price(route: Route) -> None:
    if route.request.method != "POST":
        return route.fallback()
    body = route.request.post_data_json
    body["price"] = "2"
    route.continue_(post_data=json.dumps(body))
```

Проверено: пользователь ввёл 1, сервер получил 2, таблица показала 2. Применение: проверить,
что **бэкенд** валидирует то, что фронт не даёт ввести (обход фронтовой валидации), — граница с
API-тестами; добавить заголовок (`headers={**route.request.headers, "X-Debug": "1"}`).

##### Изменить ответ

```python
def all_filled(route: Route) -> None:
    if route.request.method != "GET":
        return route.fallback()
    response = route.fetch()                        # настоящий ответ сервера
    data = response.json()
    for order in data:
        order["status"] = "FILLED"
    route.fulfill(response=response, json=data)     # заголовки и статус — от настоящего
```

Половина данных настоящая, одно поле подменено — удобно, когда собрать мок целиком тяжело.

---

#### 6. Задержка и «придержанный» запрос

Как проверить, что кнопка `disabled`, пока идёт запрос (U2.1, ловушка 3)? Запрос слишком быстрый.

**Не надо** `time.sleep()` внутри обработчика: в синхронном API обработчик выполняется в том же потоке,
что и тест, — заблокируется всё.

**Придержать запрос**: обработчик ничего не делает с route, а запоминает его; тест проверяет
промежуточное состояние и сам отпускает запрос:

```python
held: list[Route] = []
page.route("**/balances/deposit", held.append)

deposit_form.submit_button.click()
expect(deposit_form.submit_button).to_be_disabled()    # запрос висит — кнопка disabled
held[0].continue_()                                     # отпустили
expect(deposit_form.submit_button).to_be_enabled()
```

Проверено на стенде. Детерминированно: никакой гонки «успеем ли увидеть disabled».

Равномерная задержка всех запросов — `slow_network` (U2.1, через CDP).

---

#### 7. Уборка моков

```python
page.unroute("**/orders")                    # снять обработчики по шаблону
page.unroute("**/orders", handler)           # снять конкретный
page.unroute_all(behavior="ignoreErrors")    # снять все; не падать на обработчиках «в полёте»
page.route("**/orders", h, times=1)          # сработать один раз
```

Page и context закрываются после теста — моки с ними. Но внутри теста забытый мок мешает следующим
шагам: «проверить ошибку, потом проверить, что после восстановления работает» — сначала `unroute`.

Фикстура мока — `yield` и `unroute` в teardown, если page живёт дольше теста.

---

#### 8. Где граница: что мокать

| Мокать | Не мокать |
|---|---|
| ошибки сервера и сети — реакция UI | основные пользовательские сценарии (E2E) |
| редкие/трудные состояния данных | то, что проверяют API-тесты (бэкенд-логику) |
| сторонние сервисы (платёжки, карты, аналитика) | — |
| медленные / нестабильные зависимости в тестах фронта | — |

Риск моков — **расхождение с реальным API**: поле переименовали, а мок остался старым — тесты зелёные,
прод сломан. Защита: моки из реальных ответов, проверка схемы, контрактные тесты (часть API курса),
и обязательно часть E2E-тестов на настоящем бэкенде.

---

#### Собес: вопросы и ответы

**1. Как замокать бэкенд в Playwright и зачем?**
> `page.route` или `context.route` с обработчиком: `fulfill` — ответить самому, `continue_` — отправить
> на сервер с изменениями, `fallback` — передать следующему обработчику, `abort` — оборвать.
> Зачем — проверить, как UI реагирует на ответы, которые трудно получить от настоящего бэкенда: ошибки,
> пустые и экстремальные данные, медленный ответ, обрыв сети; изолировать фронт от сторонних сервисов.

**2. Как проверить, что UI показывает понятную ошибку, если API вернул 500 при создании ордера?**
> Мок на POST создания ордера с `fulfill(status=500, json=...)`, фильтрую по методу, чтобы не задеть опрос
> списка. Действие через UI, проверяю текст ошибки в форме, что ордер не появился, кнопка снова доступна.
> Отдельно — ответ не-JSON: фронт должен показать общий текст, а не упасть. После — `unroute` и проверка,
> что повторная попытка на реальном бэкенде проходит.

**3. Какие ловушки при сопоставлении URL?**
> Glob сопоставляется со всем URL, включая query: `**/orders` не поймает `/orders?status=NEW`. Для обоих
> вариантов — регулярка или функция. Обработчик ловит все HTTP-методы — фильтрую по `request.method`.
> При нескольких подходящих обработчиках первым срабатывает последний зарегистрированный.

**4. Как проверить состояние «во время запроса» — disabled, спиннер?**
> Придержать запрос: обработчик запоминает route и не отвечает, тест проверяет промежуточное состояние
> и сам вызывает `continue_` или `fulfill`. Это детерминированно, без гонки. `sleep` в обработчике в
> синхронном API блокирует тест. Альтернатива — эмуляция медленной сети.

**5. Как изменить ответ сервера, не составляя мок целиком?**
> `route.fetch()` — получить настоящий ответ, изменить JSON и отдать через `fulfill(response=..., json=...)`.
> Статус и заголовки остаются настоящими, меняется только нужное поле.

**6. Чем опасны моки?**
> Расхождением с реальным API: мок устарел — тесты зелёные, прод сломан. Поэтому моки беру из настоящих
> ответов или по схеме, проверяю контракт отдельно, и оставляю E2E-тесты на реальном бэкенде.
> Мок — инструмент для тестов фронта и трудных состояний, а не замена бэкенду.

### Задания — `tests/ui/test_u6_01_route_mocks.py`

```text
U6. Урок 1 — перехват сети: page.route и моки.

Теория: practice/u6_01_route_mocks.md
Код: ui_framework/network/mocks.py (заготовка).
Запуск:
    uv run pytest tests/ui/test_u6_01_route_mocks.py -v

Пользователя и данные готовь через API (U5), кабинет — токеном. Проверки — через PO (U4).

Задача 1. Хелперы моков (network/mocks.py).
    mock_error(page, method, url_pattern, status, body=None, content_type=None) — ответить ошибкой
        только на указанный метод, остальное — fallback;
    mock_orders(page, orders: list[dict]) — подменить GET-список ордеров (с query и без — регулярка);
    hold_requests(page, url_pattern) -> list[Route] — придерживать запросы;
    page_errors(page) -> list[str] — собирать pageerror и console.error.

Задача 2. Сценарий из программы: API отдал 500 при создании ордера.
    Мок 500 с JSON-ошибкой на POST /orders. Размести ордер через UI.
    Проверь: в форме ошибка с текстом сервера; ордер не появился в таблице (дождись загрузки, U2.1);
    заблокировано 0; кнопка снова enabled. Сними мок — тот же ордер размещается.

Задача 3. Неожиданный ответ.
    parametrize: 500 JSON с сообщением / 502 HTML / 503 без тела / 422 с details по двум полям.
    Для каждого — какой текст увидит пользователь (сначала посмотри errorText в exchange/web/app.js
    и запиши ожидания, потом проверяй). Читаемые id.

Задача 4. Ловушка query.
    mock_orders с glob "**/orders" и пустым списком; выбери фильтр NEW — что в таблице?
    Перепиши мок на регулярку — пусто при любом фильтре. В «Ответах»: почему.

Задача 5. Невозможные данные.
    Подмени список ордеров одним BTC-USDT SELL PARTIALLY_FILLED (filled 0.25 из 0.5) и одним
    с очень длинной ценой ("123456789012.123456789012345678"). Проверь, что строки отрисованы
    с нужными статусом, исполнением и ценой целиком. Мок построй из НАСТОЯЩЕГО ответа (route.fetch
    или API-клиент), а не по памяти — объясни в «Ответах», зачем.

Задача 6. Обрыв сети.
    abort на GET /balances после того, как балансы загрузились. Дождись следующего опроса
    (как понять, что он был? — page.wait_for_request с предикатом).
    Проверь: в page_errors есть ошибка сети, а таблица балансов показывает старые значения.
    В «Ответах»: это баг? Как бы ты оформил находку (кратко: заголовок, шаги, ожидаемое, фактическое)?

Задача 7. Придержанный запрос.
    hold_requests на POST /balances/deposit: нажми «Пополнить» — кнопка disabled, тоста нет;
    отпусти запрос — кнопка enabled, тост «Баланс USDT пополнен», баланс обновился.
    Тот же приём для «Разместить ордер».

Задача 8. Изменение на лету.
    а) continue_ с изменённым телом: пользователь вводит количество 1, сервер получает 1000 —
       при балансе USDT 100 и цене 1 что ответит сервер, что покажет UI? Это проверка того, что бэкенд
       валидирует сам, а не надеется на фронт.
    б) route.fetch + fulfill(response=...): у всех ордеров в списке filled_quantity == quantity и
       статус FILLED — проверь отображение; сними мок — снова реальные NEW.

Задача 9. Порядок обработчиков.
    Базовый мок «все GET /orders → пустой список» на весь тест, поверх — times=1 мок с одним ордером.
    Что видно после первого опроса и после второго? Объясни через порядок вызова и times.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как замокать бэкенд в Playwright и зачем?
    2. Как проверить, что UI показывает понятную ошибку, если API вернул 500 при создании ордера?
    3. Какие ловушки при сопоставлении URL?
    4. Как проверить состояние «во время запроса» — disabled, спиннер?
    5. Как изменить ответ сервера, не составляя мок целиком?
    6. Чем опасны моки?
```

<a id="u6-2"></a>

## U6.2 HAR и page.clock

*Теория: `practice/u6_02_har_clock.md`*

Задания: `tests/ui/test_u6_02_har_clock.py`.

План: что такое HAR; запись (`route_from_har(update=True)`, `record_har_path`, codegen `--save-har`);
воспроизведение, фильтры и `not_found`; когда HAR полезен и чем опасен; `page.clock` — подмена времени
в браузере: `install`, `pause_at`, `run_for`, `fast_forward`, `set_fixed_time`, `set_system_time`, `resume`;
таймеры стенда (тост 2,5 с, опрос 2 с) — проверено; чего clock не умеет (время сервера).

---

#### 1. HAR

**HAR (HTTP Archive)** — JSON-файл с записью сетевых запросов и ответов: URL, метод, заголовки, тело,
статус, тайминги. Его умеют писать браузеры (DevTools → Network → Save all as HAR), прокси и Playwright.

В тестах HAR используют, чтобы **записать** настоящие ответы бэкенда один раз и **воспроизводить**
их потом без бэкенда — это «мок из реальных данных» целым набором (U6.1, раздел 8).

---

#### 2. Запись

##### route_from_har с update=True — рекомендуемый способ

```python
page.route_from_har(
    "tests/ui/data/orders.har",
    url=re.compile(r"/(orders|balances)(\?|$)"),   # что записывать — только API, без статики
    update=True,                                     # режим записи
    update_content="embed",                          # тела ответов внутри HAR ("attach" — отдельными файлами)
    update_mode="minimal",                           # только то, что нужно для воспроизведения
)
... действия ...
page.context.close()                                 # файл записывается при закрытии context!
```

Проверено на стенде: записали `GET /balances` и `GET /orders` пользователя с ордером; файл появился
после `context.close()`.

##### record_har_path у context

```python
context = browser.new_context(record_har_path="all.har", record_har_url_filter="**/orders*")
```

Пишет весь трафик context (тоже при закрытии). Удобно для отладки «что ходило по сети».

##### codegen

```bash
uv run playwright codegen --channel chrome --save-har=session.har --save-har-glob="**/orders*" http://localhost:8080/app/
```

Пройти сценарий руками — получить HAR (U2.3).

##### Что почистить в записанном HAR

В HAR попадают **заголовки запросов** — включая `Authorization: Bearer <токен>`, cookies.
Перед коммитом: убрать секреты или писать HAR только в `.auth/`-подобную папку вне git. Токены стенда
живут 15 минут, но на реальных проектах в HAR попадают долгоживущие сессии.

---

#### 3. Воспроизведение

```python
page.route_from_har(
    "tests/ui/data/orders.har",
    url=re.compile(r"/(orders|balances)(\?|$)"),
    not_found="fallback",                # нет в HAR → идти на сервер; "abort" (по умолч.) — оборвать
)
page.reload()
```

Проверено: **новый** пользователь с пустым счётом после `route_from_har` видит записанный ордер и
заблокированные 7 USDT — ответы пришли из файла.

Как Playwright ищет ответ: по URL и методу, для POST — ещё по телу запроса. Несколько подходящих
записей — берёт первую. Значит, HAR хорошо воспроизводит **чтение** (GET), а сценарии с изменениями
(«создал ордер → список изменился») воспроизводятся плохо: на тот же `GET /orders` всегда один ответ.

`context.route_from_har(...)` — то же для всех страниц context.

---

#### 4. Когда HAR полезен, чем опасен

| Полезно | Опасно |
|---|---|
| тесты фронта без бэкенда (быстро, стабильно, офлайн) | **устаревает**: API изменился — HAR нет, тесты зелёные |
| воспроизвести баг с данными с прода/стейджа | секреты и персональные данные в файле |
| сторонние API (карты, курсы валют), которые нельзя дёргать в тестах | большие файлы в репозитории |
| много связанных ответов сразу (страница грузит 15 запросов) | плохо подходит для сценариев с изменением данных |

Правило: HAR — **обновляемый артефакт**. Перезапись по расписанию или командой
(`update=True` через флаг окружения), а E2E на настоящем бэкенде — обязательно рядом.

---

#### 5. page.clock — время в браузере

Фронтенд живёт таймерами: тост исчезает через 2,5 с, таблицы обновляются раз в 2 с, сессия
«истекает через 15 минут», баннер «акция до полуночи». Ждать реальное время — медленно (U2.1) и нестабильно.
`page.clock` подменяет в странице `Date`, `setTimeout`, `setInterval`, `requestAnimationFrame`, `performance.now`.

##### Важно: install не останавливает время

```python
page.clock.install()             # подменили часы, но время ИДЁТ как обычно
```

Проверено на стенде: после `install()` тост всё равно исчез через реальные 3 с, опрос продолжался.
Чтобы управлять временем, его нужно **остановить**:

```python
page.clock.install(time="2030-01-01T10:00:00Z")    # до goto: часы с этой даты
page.goto("/app/")
page.clock.pause_at("2030-01-01T10:00:01Z")        # остановить на моменте
```

##### Управление

| Метод | Что делает | Проверено на стенде |
|---|---|---|
| `install(time=...)` | подменить часы (лучше **до** `goto`), время идёт | тост исчез сам через 3 с |
| `pause_at(t)` | перемотать до `t` и остановить | 4 реальные секунды: тост висит, опросов 0 |
| `run_for(ms)` | прокрутить время на `ms`, **выполняя все таймеры** по пути | `run_for(2600)`: тост скрылся, 1 опрос |
| `fast_forward(ms / "mm:ss")` | **прыгнуть** вперёд; просроченные таймеры — по **одному** разу | +10 с: только 1 опрос, не 5 |
| `resume()` | снова пустить время | опросы пошли |
| `set_fixed_time(t)` | `Date.now()` всегда `t`, таймеры работают | |
| `set_system_time(t)` | сменить «текущее время», таймеры не трогать | `new Date()` → 2030-01-01 |

`run_for` vs `fast_forward`: первый — «прожить» отрезок (все тики `setInterval`), второй — «закрыть
ноутбук на час и открыть» (один тик). Для «через 15 минут бездействия разлогинит» — `fast_forward("15:00")`.

##### Тесты на таймеры стенда

```python
page.clock.install()
register(...)                                     # тост «Аккаунт создан»
page.clock.pause_at(...)
expect(toast).to_be_visible()                     # время стоит — тост не исчезнет, пока не скажем
page.clock.run_for(2_500)
expect(toast).to_be_hidden()
```

Теперь можно **детерминированно** проверить «тост показывается 2,5 с» — и «не меньше 2 с»:
`run_for(2_000)` → ещё виден, `run_for(600)` → скрыт.

##### Чего clock не умеет

- **время сервера**: часы подменяются только в странице. JWT на сервере истечёт по **серверным** часам —
  `fast_forward("15:00")` в браузере не сделает токен просроченным. Для «токен истёк» — мусорный токен (U5.1)
  или настройка TTL стенда;
- `expect`-таймауты и `wait_for_timeout` — на стороне теста, clock на них не влияет;
- ответы сети приходят как обычно — clock не ускоряет сервер.

---

#### Собес: вопросы и ответы

**1. Что такое HAR и как используешь его в тестах?**
> Архив сетевого трафика: запросы, ответы, заголовки, тела. Записываю реальные ответы через
> `route_from_har(update=True)` или опцию context, потом воспроизвожу — фронт работает без бэкенда.
> Полезно для тестов фронта, сторонних API и воспроизведения бага с реальными данными.
> Минусы — устаревание и секреты в файле; HAR регулярно перезаписываю и чищу.

**2. Как воспроизвести баг, который проявляется только на данных с прода?**
> Записать HAR нужных запросов (DevTools или Playwright), убрать персональные данные и секреты, и
> воспроизвести через `route_from_har` в тесте — UI получит те же ответы. Если баг в бэкенде — HAR
> поможет сформулировать API-тест с этими данными.

**3. Как тестировать функциональность, зависящую от времени?**
> `page.clock`: установить часы до загрузки страницы, остановить `pause_at`, дальше управлять —
> `run_for` прожить отрезок с выполнением таймеров, `fast_forward` перепрыгнуть, `set_fixed_time` для
> фиксированной даты. Важно: `install` сам время не останавливает. И clock меняет время только
> в браузере — серверные сроки (токены) так не проверить.

**4. Чем run_for отличается от fast_forward?**
> `run_for` прокручивает время и выполняет все таймеры по пути — `setInterval` раз в 2 секунды за 10 секунд
> сработает 5 раз. `fast_forward` прыгает вперёд, и каждый просроченный таймер срабатывает один раз —
> как если бы вкладка спала. Первый — для «прожить время», второй — для «прошло много времени».

**5. Мок, HAR или реальный бэкенд — как выбираешь?**
> Реальный бэкенд — для основных пользовательских сценариев. Точечный мок — для ошибок, трудных
> состояний и состояния «во время запроса». HAR — когда нужно много реальных ответов сразу или
> сторонний сервис. Моки и HAR держу актуальными и не даю им заменить E2E.

### Задания — `tests/ui/test_u6_02_har_clock.py`

```text
U6. Урок 2 — HAR и page.clock.

Теория: practice/u6_02_har_clock.md
Запуск:
    uv run pytest tests/ui/test_u6_02_har_clock.py -v
HAR-файлы пиши в tmp_path или tests/ui/data/har/ (если коммитишь — без токенов, см. задачу 3).

Задача 1. Запись HAR.
    Пользователь через API: USDT 1000, три ордера (10, 20, 30). Открой кабинет токеном.
    route_from_har(update=True, url=регулярка только на /orders и /balances, update_content="embed").
    Перезагрузи страницу, дождись таблиц, закрой context. Прочитай HAR как JSON и проверь:
    есть записи GET /orders и GET /balances, в ответе /orders три ордера.

Задача 2. Воспроизведение.
    Новый пустой пользователь (через API), кабинет токеном, route_from_har из задачи 1 (not_found="fallback").
    В UI: три ордера и заблокировано 60 — хотя у пользователя ничего нет.
    Затем через UI размести ордер — что в таблице после следующего опроса? Объясни (раздел 3 теории).

Задача 3. Секреты в HAR.
    Найди в HAR из задачи 1 заголовок Authorization. Напиши sanitize_har(path) — заменяет значения
    authorization/cookie на "***". Тест: после санитизации токена в файле нет, а воспроизведение (задача 2)
    по-прежнему работает. Почему работает? Запиши в «Ответах».

Задача 4. Обновление HAR по флагу.
    Фикстура orders_har: если UPDATE_HAR=1 — пишет HAR заново (update=True), иначе воспроизводит.
    В «Ответах»: как встроить обновление в процесс (когда и кто перезаписывает).

Задача 5. install не останавливает время.
    page.clock.install() до входа; после тоста «Аккаунт создан» page.wait_for_timeout(3000) —
    тост виден? Запиши результат. Затем то же с pause_at — виден ли тост через реальные 3 с?

Задача 6. Длительность тоста — детерминированно.
    С остановленными часами: после пополнения тост виден; run_for(2000) — всё ещё виден;
    run_for(600) — скрыт. Ни одного wait_for_timeout в итоговом тесте.

Задача 7. run_for против fast_forward.
    Остановленные часы, кабинет открыт. Считай запросы GET /orders (page.on("request")).
    run_for(10_000) — сколько опросов? fast_forward(10_000) — сколько? Объясни разницу.
    Подсказка: после действий с часами дай странице выполнить запросы — дождись нужного числа
    через expect.poll-заменитель (wait_until из U4.4) или page.wait_for_request.

Задача 8. Время в странице.
    set_fixed_time("2030-12-31T23:59:59Z") → new Date().toISOString() в странице равно этому значению;
    set_system_time на сутки вперёд → дата изменилась, а таймеры (тост) продолжают работать.

Задача 9. Граница clock (письменно + тест).
    Кабинет открыт с часами, fast_forward("16:00") — пользователя разлогинило? Почему нет?
    Как тогда тестировать «токен истёк» (вспомни U5.1)? Напиши тест правильным способом.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое HAR и как используешь его в тестах?
    2. Как воспроизвести баг, который проявляется только на данных с прода?
    3. Как тестировать функциональность, зависящую от времени?
    4. Чем run_for отличается от fast_forward?
    5. Мок, HAR или реальный бэкенд — как выбираешь?
```

<a id="u6-3"></a>

## U6.3 Окружение браузера и собес по модулю U6

*Теория: `practice/u6_03_browser_env_interview.md`*

Задания: `tests/ui/test_u6_03_browser_env.py`. Страница: **лаборатория** `http://localhost:8080/app/lab.html`
(блок «Окружение»; стенд пересобери: `docker compose up -d --build`).

План: какие настройки окружения есть у context; локаль и часовой пояс; геолокация и разрешения;
устройства и мобильная эмуляция; тема, сеть, прочее; как задать на весь прогон, на тест, на шаг;
шпаргалка и вопросы собеса по модулю U6.

---

#### 1. Окружение — это настройки context

Почти всё, что «окружение браузера», задаётся при создании **context** (U1.4) и действует на все его страницы:

```python
context = browser.new_context(
    locale="de-DE",
    timezone_id="Asia/Tokyo",
    geolocation={"latitude": 55.7558, "longitude": 37.6173},
    permissions=["geolocation", "clipboard-read", "clipboard-write"],
    color_scheme="dark",
    viewport={"width": 390, "height": 844},
)
```

Проверено на лаборатории — страница увидела:

| Настройка | Что показала страница |
|---|---|
| `locale="de-DE"` | `navigator.language` = `de-DE`; число `1234567.891` → `1.234.567,891` |
| `timezone_id="Asia/Tokyo"` | часовой пояс `Asia/Tokyo`; `2030-01-15 12:00 UTC` → `15.01.2030, 21:00` |
| `viewport` 390×844 | медиазапрос `max-width: 600px` → «мобильный» |
| `color_scheme="dark"` | `prefers-color-scheme: dark` → «тёмная» |
| `geolocation` + `permissions=["geolocation"]` | «Широта 55.7558, долгота 37.6173» |
| `permissions=["clipboard-write", "clipboard-read"]` | копирование работает, `navigator.clipboard.readText()` читается |

---

#### 2. Локаль и часовой пояс

- `locale` влияет на `navigator.language`, `Intl.*` (числа, даты, валюты), заголовок `Accept-Language`;
- `timezone_id` — на `Date`, `Intl.DateTimeFormat` в странице. Идентификаторы IANA: `Europe/Moscow`, `UTC`, `America/New_York`.

Зачем: форматы денег и дат («1 234,56» vs «1,234.56»), границы суток («сделки за сегодня» в Токио и
Москве — разные), переводы интерфейса. Типичный баг — фронт форматирует дату в поясе браузера,
а должен в поясе биржи.

Часовой пояс context — это пояс **браузера**, а не сервера и не теста. Время сервера им не поменять
(как и `page.clock`, U6.2).

---

#### 3. Геолокация и разрешения

```python
context = browser.new_context(geolocation={"latitude": 55.75, "longitude": 37.61}, permissions=["geolocation"])
context.set_geolocation({"latitude": 59.93, "longitude": 30.31})   # сменить «на ходу» (поездка)
context.grant_permissions(["notifications"], origin="http://localhost:8080")
context.clear_permissions()                                        # отозвать все
```

Без разрешения — как пользователь, который нажал «Запретить»? Не совсем. Проверено на лаборатории:

| Разрешение | Без выдачи в context |
|---|---|
| геолокация | ошибка «доступ запрещён» (`err.code === 1`) — сразу |
| уведомления | `Notification.permission` = `default`, запрос **повисает**: окно разрешения в автотесте никто не нажмёт |
| clipboard | ошибка `NotAllowedError` |

Вывод: состояния «разрешено» и «запрещено» тестируются явно — выдачей или отзывом разрешения.
Для «пользователь ещё не решил» (`default`) — проверяй интерфейс до клика, а сам запрос не жди.

Список разрешений: `geolocation`, `notifications`, `camera`, `microphone`, `clipboard-read`, `clipboard-write`,
`midi`, `background-sync` и др. — зависят от браузера.

---

#### 4. Устройства и мобильная эмуляция

```python
iphone = playwright.devices["iPhone 13"]
# {'user_agent': '...', 'viewport': {'width': 390, 'height': 664}, 'device_scale_factor': 3,
#  'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'}

context = browser.new_context(**iphone)
```

```bash
uv run pytest tests/ui --device "iPhone 13"     # pytest-playwright: устройство на весь прогон
```

Что эмулируется: размер экрана, плотность пикселей, user agent, `is_mobile` (мета viewport, поведение
скролла), `has_touch` (тач-события: `locator.tap()`). Что **не** эмулируется: реальный мобильный браузер,
его движок (Safari на iPhone — это WebKit, а эмуляция в Chromium — всё равно Chromium), производительность
устройства, клавиатура. Эмуляция — для **адаптивной вёрстки**; поведение настоящего Safari — только на WebKit
или реальном устройстве (облака устройств).

`is_mobile` не поддерживается в Firefox.

---

#### 5. Прочее

| Настройка | Что | Пример |
|---|---|---|
| `context.set_offline(True)` | нет сети | проверено: лаборатория показала «офлайн» |
| `page.emulate_media(color_scheme="dark", reduced_motion="reduce", media="print")` | медиа на ходу | печатная версия, анимации выключены |
| `user_agent` | строка UA | ветвление «мобильный/десктоп» по UA |
| `extra_http_headers` | заголовки всех запросов | `X-Test-Run: 123` для логов стенда |
| `http_credentials` | HTTP Basic | закрытый stage |
| `java_script_enabled=False` | без JS | SSR-страницы, SEO |
| `ignore_https_errors=True` | самоподписанный сертификат | stage |
| `base_url` | U1.4 | |

---

#### 6. Где задавать

| Область | Как |
|---|---|
| весь прогон | `browser_context_args` в conftest (U1.4), `--device` в командной строке |
| окружение (stage/local) | значения из Settings (U4.3) в `browser_context_args` |
| один тест | `@pytest.mark.browser_context_args(locale="en-US", timezone_id="UTC")` |
| несколько вариантов | `new_context(**options)` в тесте или параметризованная фикстура |
| на ходу | `set_geolocation`, `set_offline`, `grant_permissions`, `emulate_media` |

Параметризованная фикстура «локаль × часовой пояс» — один тест форматирования прогоняется на 4 окружениях.

---

#### 7. Шпаргалка по модулю U6

- **route (U6.1)**: `page.route` / `context.route`; `fulfill` / `continue_` / `fallback` / `abort` / `fetch`;
  фильтр по методу; glob не ловит query → регулярка; последний зарегистрированный — первый;
  ошибки 500/502/422 и что видит пользователь; придержать запрос для промежуточных состояний;
  `unroute`, `times=1`; мок — по контракту, из реальных ответов.
- **HAR и clock (U6.2)**: запись `route_from_har(update=True)` — файл при `context.close()`; воспроизведение
  с `not_found`; секреты в HAR; устаревание. `clock.install` время не останавливает → `pause_at`;
  `run_for` выполняет все таймеры, `fast_forward` — по разу; часы только в браузере.
- **Окружение (U6.3)**: locale, timezone_id, geolocation + permissions, devices, color_scheme, offline;
  без разрешения геолокация — отказ, уведомления — висят; эмуляция ≠ реальный мобильный браузер.

---

#### Собес: вопросы и ответы

Плюс вопросы из U6.1 (6) и U6.2 (5).

**1. Как проверить, что фронт отправил правильный запрос?**
> `expect_request` с предикатом по URL и методу вокруг действия — проверяю метод, тело (`post_data_json`),
> заголовки. Или `route` с `continue_` и запоминанием запроса. Если важно, что сервер **сохранил**, — ещё
> проверка через API. (U2.1, U5.1, U6.1.)

**2. Как тестировать мобильную версию сайта?**
> Эмуляция устройства — `playwright.devices[...]` или `--device`: viewport, плотность пикселей, user agent,
> тач. Это для адаптивной вёрстки и мобильных сценариев интерфейса. Поведение настоящего мобильного Safari —
> на WebKit или на реальных устройствах в облаке, эмуляция в Chromium его не заменит.

**3. Как тестировать геолокацию и другие разрешения?**
> Выдаю разрешение в context (`permissions`) и задаю координаты (`geolocation`), меняю на ходу
> `set_geolocation`. Отказ — тест без разрешения или `clear_permissions`. Учитываю, что «ещё не решил»
> в автотесте не нажать: такие запросы висят.

**4. Как проверить форматирование дат и денег для разных стран?**
> Параметризованные context с `locale` и `timezone_id`, одна проверка на несколько окружений. Отдельно —
> границы суток в разных поясах. Помню, что пояс context — это пояс браузера, а не сервера.

**5. Чем отличаются page.route, HAR и реальный бэкенд — когда что?**
> Реальный бэкенд — основные сценарии E2E. Точечный route — ошибки, трудные состояния, «во время запроса».
> HAR — много реальных ответов сразу, сторонние сервисы, воспроизведение данных с прода. Моки и HAR держу
> актуальными.

### Задания — `tests/ui/test_u6_03_browser_env.py`

```text
U6. Урок 3 — окружение браузера и собес по модулю U6.

Теория: practice/u6_03_browser_env_interview.md
Страница: /app/lab.html, блок «Окружение» (стенд пересобрать: docker compose up -d --build).
Запуск:
    uv run pytest tests/ui/test_u6_03_browser_env.py -v

Задача 1. LabPage (ui_framework/pages/lab_page.py — создай) с компонентом EnvPanel:
    timezone, locale, number, date, layout, online, scheme (Locator), кнопки geo/notify/copy и их результаты.
    Он понадобится и в U3.

Задача 2. Локаль × часовой пояс.
    Параметризованная фикстура env_page: (ru-RU, Europe/Moscow), (en-US, America/New_York),
    (de-DE, Asia/Tokyo), (ja-JP, UTC). Проверь число 1234567.891 и дату 2030-01-15 12:00 UTC
    для каждой пары. Ожидаемые строки сначала посчитай сам (подумай, как это сделать в Python
    без хардкода — или честно захардкодь и объясни выбор в «Ответах»).

Задача 3. Геолокация.
    а) Разрешение + координаты Москвы → текст с широтой и долготой (4 знака).
    б) set_geolocation на Санкт-Петербург без пересоздания context → новые координаты.
    в) Без разрешения → «доступ запрещён».

Задача 4. Уведомления и буфер обмена.
    а) Разрешение notifications → «Уведомления включены».
    б) Без разрешения: какое значение Notification.permission? Что будет, если нажать кнопку и ждать
       результата? Запиши в «Ответах», тест напиши так, чтобы он не висел.
    в) clipboard: адрес кошелька скопирован — проверь содержимое через navigator.clipboard.readText().

Задача 5. Устройства.
    parametrize по устройствам: "iPhone 13", "Pixel 7", "iPad Pro 11", "Desktop Chrome".
    Проверь env-layout (мобильный/десктоп) — где граница и почему iPad даёт то, что даёт?
    Отдельно: запуск всего файла с --device "iPhone 13" — что меняется?

Задача 6. Офлайн и тема.
    set_offline(True) → «офлайн», set_offline(False) → «онлайн».
    emulate_media(color_scheme="dark") на открытой странице → «тёмная» (после resize или reload? проверь,
    когда страница перечитывает тему, и объясни).

Задача 7. Окружение из конфига.
    В Settings (U4.3) добавь locale и timezone; browser_context_args берёт их оттуда.
    Для stage — другой пояс. Проверь на лаборатории для ENV=docker.

Задача 8. Устный собес по модулю U6.
    10 вопросов из «Собес» U6.1–U6.3 (16 вопросов), вслух, 40–90 с. Номера, где «поплыл», — в «Ответы».

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как проверить, что фронт отправил правильный запрос?
    2. Как тестировать мобильную версию сайта?
    3. Как тестировать геолокацию и другие разрешения?
    4. Как проверить форматирование дат и денег для разных стран?
    5. Чем отличаются page.route, HAR и реальный бэкенд — когда что?
```


---

# U7. Отладка и отчёты

<a id="u7-1"></a>

## U7.1 Trace Viewer, скриншоты, видео и отчёт

*Теория: `practice/u7_01_trace_artifacts.md`*

Задания: `tests/ui/test_u7_01_trace_artifacts.py`.

План: какие артефакты даёт pytest-playwright и как их включить; где они лежат (проверено);
ловушка — context вне фикстур без артефактов; Trace Viewer — что в нём есть и как разбирать падение
по шагам; ручная трассировка; видео (и почему у нас локально его нет); артефакты в Allure; что включать
локально, а что в CI.

Модуль U7: U7.1 артефакты и Trace Viewer → U7.2 отладка и «в CI падает, локально проходит» + собес.

---

#### 1. Артефакты pytest-playwright

```bash
uv run pytest tests/ui --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure
```

| Опция | Значения | Что |
|---|---|---|
| `--tracing` | `on`, `off`, `retain-on-failure` | trace.zip — полная запись теста |
| `--screenshot` | `on`, `off`, `only-on-failure` | скриншот в конце теста |
| `--full-page-screenshot` | флаг | скриншот всей страницы, а не экрана |
| `--video` | `on`, `off`, `retain-on-failure` | видео каждой страницы (webm) |
| `--output` | путь, по умолч. `test-results` | куда складывать |

Проверено на стенде (`--tracing retain-on-failure --screenshot only-on-failure`):

```
test-results/
  test-fixture-page-fails-chromium/
    test-failed-1.png
    trace.zip
  test-new-context-fails-chromium/
    test-failed-1.png
    trace.zip
```

- у **прошедшего** теста — ничего (на то и `retain-on-failure`);
- папка — имя теста + браузер (+ параметры parametrize);
- `test-results/` в `.gitignore` (U2.3).

##### Ловушка: context вне фикстур

Артефакты пишутся для context, созданных **фикстурами плагина** — `context`, `page`, `new_context`.
Проверено: тест, который сам вызвал `browser.new_context()`, упал — и **ни trace, ни скриншота** нет.
Поэтому в фреймворке context создаём через `new_context` (U1.4, U5.1), а не через `browser.new_context`.

---

#### 2. Trace Viewer

```bash
uv run playwright show-trace test-results/<папка>/trace.zip
```

Или открыть trace.zip на **trace.playwright.dev** — файл обрабатывается в браузере, на сервер не отправляется.
Удобно, когда trace скачан из CI на машину без Python.

Что внутри (`unzip -l trace.zip`): `trace.trace` (действия), `trace.network` (сеть), `screencast/*.jpeg` (кадры),
`resources/` (HTML, CSS, картинки для снимков DOM).

##### Панели

| Панель | Что смотреть |
|---|---|
| **Actions** | список шагов теста: `goto`, `click`, `fill`, `expect` — с длительностью; упавший — красный |
| **Timeline** | кадры экрана по времени — видно, что было на экране в момент шага |
| **Снимки DOM: Before / Action / After** | **живой** DOM до действия, в момент (с точкой клика), после — можно инспектировать как в DevTools |
| **Call** / **Log** | параметры действия и лог actionability (U2.3): что ждали, почему не кликнулось |
| **Errors** | текст ошибки и место в коде |
| **Console** | консоль браузера: ошибки JS, `console.log` |
| **Network** | запросы со статусами, заголовками, телами — тот самый 503 на `app.js` (U2.4) |
| **Source** | строка теста для выбранного шага |
| **Metadata** | браузер, viewport, время |

Снимок DOM — не картинка, а **разметка**: можно найти элемент, посмотреть атрибуты, проверить локатор
(кнопка «Pick locator» прямо в Trace Viewer).

##### Как разбирать упавший тест

1. **Errors** — что именно упало: таймаут действия, проверка, strict mode.
2. **Actions** → упавший шаг → **Before**: что было на экране и в DOM. Элемент есть? Другой текст? Модалка сверху?
3. **Log** шага — чего ждал Playwright: `element is not visible`, `intercepts pointer events`.
4. **Network** вокруг шага — ответы сервера: 4xx/5xx, медленный ответ, ответа нет.
5. **Console** — JS-ошибки фронта.
6. Шаги **до** упавшего — часто причина раньше: пополнение не прошло → ордер не создался → упала проверка таблицы.

---

#### 3. Ручная трассировка

Когда нужен trace без опции командной строки, или для context вне фикстур:

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
...
context.tracing.stop(path=tmp_path / "trace.zip")
```

Куски одной долгой сессии (session-scope context из U5.3):

```python
context.tracing.start(screenshots=True, snapshots=True)
for name in ("step1", "step2"):
    context.tracing.start_chunk(title=name)
    ...
    context.tracing.stop_chunk(path=f"{name}.zip")
context.tracing.stop()
```

Группы шагов в trace (как шаги Allure):

```python
context.tracing.group("Пополнить счёт")
...
context.tracing.group_end()
```

API-запросы через `context.request` тоже попадают в trace — подготовка через API (U5) видна рядом с UI-шагами.

---

#### 4. Скриншоты

```python
page.screenshot(path=tmp_path / "page.png", full_page=True)
locator.screenshot(path="widget.png")                         # только элемент
page.screenshot(mask=[page.get_by_test_id("lab-clock")])       # закрасить динамику
```

`--screenshot only-on-failure` — последний кадр упавшего теста. Скриншоты для **сравнения** (визуальная
регрессия) — U8.

---

#### 5. Видео

```bash
uv run pytest --video retain-on-failure
```

Видео пишется на context и **дописывается при его закрытии**. Вручную: `browser.new_context(record_video_dir=..., record_video_size=...)`,
путь — `page.video.path()` после `context.close()`.

**У нас локально видео нет.** Проверено: Playwright требует свой ffmpeg, а `playwright install ffmpeg` на macOS 12
отвечает `Playwright does not support ffmpeg on mac12`. Тест с `--video` падает на создании страницы.
Видео включают в CI (Linux/Docker, U9). Trace почти всегда полезнее видео: там тот же экран **плюс** DOM, сеть, консоль.

---

#### 6. Артефакты в Allure

Хук из U4.4 прикладывал скриншот и URL. Добавить trace:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "teardown":                               # артефакты плагин пишет на teardown
        output = item.funcargs.get("output_path")               # фикстура плагина: папка артефактов теста
        if output and Path(output).is_dir():
            for file in Path(output).glob("*"):
                allure.attach.file(str(file), name=file.name)
```

`output_path` — фикстура pytest-playwright: путь к папке этого теста в `test-results`. Trace плагин записывает
**после** теста (в teardown context), поэтому прикладывать — на фазе teardown, а не call.

Allure сам не открывает trace — в отчёте он будет файлом для скачивания и просмотра на trace.playwright.dev.

---

#### 7. Что включать где

| | Локально | CI |
|---|---|---|
| trace | `retain-on-failure` или вручную | `retain-on-failure` — **всегда** |
| скриншот | по желанию | `only-on-failure` |
| видео | нет (macOS 12) / по желанию | `retain-on-failure`, если хватает места |
| Allure | при необходимости | да, с вложениями |

`--tracing on` для всех тестов — тяжело (сотни МБ) и медленнее; включают точечно для расследования.

---

#### Собес: вопросы и ответы

**1. Что такое Trace Viewer и как разбираешь по нему упавший тест?**
> Trace — запись теста: шаги с длительностью, снимки DOM до и после каждого действия, кадры экрана, сеть, консоль,
> лог ожиданий, исходник. Открываю `playwright show-trace` или на trace.playwright.dev. Сначала ошибка, потом
> упавший шаг и снимок Before — что было на экране и в DOM, лог действия — чего ждал Playwright, сеть и консоль
> вокруг шага, и шаги до — причина часто раньше.

**2. Какие артефакты собираешь при падении?**
> Trace с retain-on-failure — главный, плюс скриншот на падении, в CI — видео, если позволяет место. Всё
> прикладываю в Allure. Плюс логи стенда по request id (U2.4).

**3. Почему у теста нет trace, хотя опция включена?**
> Плагин пишет артефакты для context, созданных его фикстурами — `page`, `context`, `new_context`. Если тест
> создал context через `browser.new_context()`, артефактов нет. Решение — `new_context` или ручной
> `context.tracing.start/stop`.

**4. Trace или видео?**
> Trace почти всегда полезнее: там тот же экран плюс DOM, сеть, консоль и лог. Видео удобно показать не
> технарям — как воспроизводится баг. Видео тяжелее и требует ffmpeg.

### Задания — `tests/ui/test_u7_01_trace_artifacts.py`

```text
U7. Урок 1 — Trace Viewer, скриншоты, видео и отчёт.

Теория: practice/u7_01_trace_artifacts.md
Запуск (в этом уроке часть тестов падают специально — смотри артефакты):
    uv run pytest tests/ui/test_u7_01_trace_artifacts.py -v --tracing retain-on-failure --screenshot only-on-failure

Задача 1. Падение по сети.
    Тест: мок 500 на POST /orders (U6.1), но проверка ожидает, что ордер появился (тест «не знает» про мок).
    Запусти, открой trace (uv run playwright show-trace ...): найди в Network ответ 500, в Console — ошибки,
    в снимке Before упавшего шага — что было в форме. Опиши в «Ответах» путь разбора по шагам из теории.
    После — пометь тест xfail(strict=True), чтобы он не мешал прогону.

Задача 2. Падение по локатору.
    Тест кликает page.get_by_role("button", name="Отменить") при двух ордерах (strict mode, U2.2).
    Найди в trace: Errors (что сказал strict mode), Log шага, снимок DOM — проверь в нём локатор через Pick locator.
    xfail(strict=True).

Задача 3. Причина раньше падения.
    Сценарий: пополнение на "-5" (тихо не проходит, если хелпер не проверяет ответ), потом ордер на 100,
    падает проверка «заблокировано 100». По trace найди шаг, где на самом деле всё пошло не так.
    Как сделать, чтобы тест падал сразу на нём? (Вспомни U4.1: PO проверяет своё действие.)

Задача 4. Нет trace.
    Тест с browser.new_context() вместо new_context — упади в нём. Есть ли папка в test-results?
    Почини двумя способами: new_context и ручной tracing.start/stop с сохранением в tmp_path.

Задача 5. Ручная трассировка с группами.
    Тест покупки (U5.2, builder): tracing.group("Подготовка через API") / group("Покупка") / group("Проверки").
    tracing.stop(path=...) — открой и убедись, что группы видны, а API-запросы подготовки — тоже в trace.

Задача 6. Скриншоты.
    а) page.screenshot(full_page=True) лаборатории в tmp_path;
    б) locator.screenshot только таблицы котировок;
    в) скриншот с mask на часы в шапке — открой и посмотри, как выглядит маска.

Задача 7. Артефакты в Allure.
    Хук в ui_framework/fixtures/reporting.py (U4.4): на фазе teardown приложить всё из output_path.
    Запусти задачу 1 с --alluredir: в отчёте у теста есть trace.zip и png.
    Объясни в «Ответах», почему фаза teardown, а не call.

Задача 8. Видео (письменно).
    Попробуй --video retain-on-failure. Что случилось и почему? Где видео будет работать (U9)?

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое Trace Viewer и как разбираешь по нему упавший тест?
    2. Какие артефакты собираешь при падении?
    3. Почему у теста нет trace, хотя опция включена?
    4. Trace или видео?
```

<a id="u7-2"></a>

## U7.2 Отладка и «в CI падает, локально проходит»; собес по модулю U7

*Теория: `practice/u7_02_debug_ci_interview.md`*

Задания: `tests/ui/test_u7_02_debug_ci.py`.

План: инструменты отладки одним списком (что когда); `--headed --slowmo` и почему slowmo прячет гонки;
`breakpoint()` и `--pdb`; чем CI отличается от твоей машины — таблица; как воспроизвести CI локально
(headless, медленная сеть, медленный CPU, параллель, Docker); алгоритм ответа на главный вопрос модуля;
собес.

---

#### 1. Инструменты отладки

| Инструмент | Как | Когда |
|---|---|---|
| `--headed` | видеть браузер | понять, что происходит на экране |
| `--slowmo 500` | пауза 500 мс **перед каждым действием** | глазами успеть за шагами |
| `PWDEBUG=1` | Inspector, пошагово, без таймаутов (U2.3) | разобрать шаги, подобрать локатор |
| `page.pause()` | остановиться в точке, Inspector, Record (U2.3) | дописать кусок теста |
| `DEBUG=pw:api` | лог каждого действия в консоль (U2.3) | чего ждёт зависшее действие |
| `breakpoint()` / `--pdb` | отладчик Python в тесте / при падении | значения переменных, данные API |
| Trace Viewer | после прогона (U7.1) | **главный** инструмент для CI |
| логи стенда по `X-Request-ID` (U2.4) | `docker compose logs exchange \| grep <id>` | что ответил бэкенд и почему |
| `page.on("console")`, `page.on("pageerror")` (U6.1) | ошибки JS в тесте | фронт упал молча |

##### slowmo прячет гонки

`--slowmo` замедляет **действия теста**, а не приложение. Между кликом и проверкой UI получает лишние 500 мс —
и успевает обновиться. Проверено на стенде: наивный тест «три пополнения по тосту» (U2.1) со `slow_network(400)` и медленным CPU
**падает** без slowmo и **проходит** с `--slowmo 1000`.
Для поиска гонок — наоборот, замедлять **приложение**: сеть (`slow_network`, U2.1), CPU (раздел 3).

##### breakpoint и pdb

```python
def test_trade(...):
    order = seller.api.place_order(...)
    breakpoint()                    # pytest остановится: можно смотреть order, вызывать page.screenshot()
```

```bash
uv run pytest tests/ui/test_x.py -k trade --pdb      # отладчик в момент падения
uv run pytest ... -s                                  # нужен, чтобы ввод/вывод отладчика работал
```

Во время паузы в pdb браузер **стоит** — можно смотреть его в `--headed`. Не оставлять `breakpoint()` в коде (как `pause()`).

---

#### 2. Чем CI отличается от твоей машины

| Различие | У тебя | В CI | Чем ломает |
|---|---|---|---|
| режим | headed / headless | headless | редко: размеры, фокус окна, шрифты |
| ОС и шрифты | macOS | Linux (Docker) | вёрстка, переносы текста, скриншоты (U8) |
| браузер | `--browser-channel chrome` (системный) | Chromium Playwright | версия браузера, поведение |
| ресурсы | быстрый ноутбук | 2 vCPU, соседние джобы | **тайминги**: гонки ожиданий (U2.1) |
| параллель | по одному | `-n auto` | общие данные (U5.3) |
| окружение | docker local | stage / свежий стенд | данные, сбои, задержки (U2.4) |
| состояние | стенд «прогретый», данные от прошлых запусков | чистая база | тесты, зависящие от «уже есть» |
| порядок | один файл | весь набор | зависимость от порядка (U2.4) |
| время и пояс | твой | UTC | даты, границы суток (U6.3) |
| конфиг | `.local.env` | секреты CI | забытая переменная, другой URL (U4.3) |
| сеть | localhost | контейнеры, DNS | медленнее, бывает недоступно |

---

#### 3. Воспроизвести CI локально

1. **Скачать артефакты** CI: trace, скриншоты, Allure, логи — чаще всего причина видна сразу (U7.1).
2. **Тот же запуск**: команда из CI целиком — с теми же маркерами, `-n`, `ENV`, `--base-url`.
3. **Headless и браузер CI**: без `--headed`, тот же браузер (Chromium Playwright, а не системный Chrome).
4. **Замедлить приложение**:
   ```python
   slow_network(page, 400)                                           # U2.1
   cdp = page.context.new_cdp_session(page)
   cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})            # CPU в 4 раза медленнее (Chromium)
   ```
5. **Повторять**: `--count 20 -x` (U2.4), под `-n 4` — с соседними тестами.
6. **Тот же Docker-образ**, что в CI (`mcr.microsoft.com/playwright/python:v<версия>-noble`, U9) — те же ОС, шрифты, браузер.
7. **То же окружение**: stage, если CI бежит на stage; чистая база — свежий `docker compose down -v && up`.

Цель — превратить «иногда в CI» в «всегда у меня». Дальше — обычная починка по категориям U2.4.

---

#### 4. Главный вопрос: «тест упал в CI, локально проходит — твои действия»

Структура ответа (2–3 минуты):

1. **Не перезапускаю вслепую.** Сначала смотрю, что упало: один тест или много, впервые или регулярно
   (история в Allure / CI).
2. **Артефакты**: trace — упавший шаг, DOM, сеть, консоль; скриншот; логи стенда по request id.
3. **Гипотеза по различиям**: тайминги, параллель и общие данные, окружение и данные, конфиг, браузер, время.
4. **Воспроизвожу**: та же команда, headless, Docker-образ CI, замедление сети/CPU, повтор с `--count`.
5. **Чиню причину**, а не симптом: ожидание результата вместо промежуточного сигнала, изоляция данных, конфиг.
   Не `sleep`, не увеличение таймаутов, не ретраи.
6. **Если баг в продукте** — баг-репорт с trace; тест в `xfail` со ссылкой или карантин.
7. **Закрепляю**: прогон `--count` и под параллелью зелёный; если причина типовая — правило в чек-лист ревью.

---

#### 5. Шпаргалка по модулю U7

- Артефакты: `--tracing retain-on-failure`, `--screenshot only-on-failure`, `--video retain-on-failure`, `--output`.
- Только для context из фикстур плагина; иначе — `context.tracing.start/stop`.
- Trace Viewer: Actions, Before/After DOM, Log, Network, Console, Errors, Source; `show-trace` или trace.playwright.dev.
- Вложения в Allure — на фазе teardown, из `output_path`.
- Видео на macOS 12 недоступно (ffmpeg) — только CI.
- Отладка: headed, slowmo (прячет гонки), PWDEBUG, pause, pw:api, breakpoint/--pdb.
- CI ≠ локально: тайминги, параллель, окружение, браузер, ОС, время, конфиг. Воспроизводить — артефакты,
  та же команда, Docker-образ, замедление, повторы.

---

#### Собес: вопросы и ответы

Плюс вопросы U7.1 (4).

**1. Тест упал в CI, а локально проходит. Твои действия?**
> См. раздел 4 — артефакты, гипотеза по различиям, воспроизведение, починка причины, закрепление.

**2. Какими инструментами отлаживаешь UI-тест?**
> Локально — headed, Inspector через PWDEBUG или `page.pause`, лог `DEBUG=pw:api`, `breakpoint`/`--pdb`.
> После прогона и для CI — Trace Viewer, скриншоты, Allure, логи бэкенда по request id, ошибки консоли браузера.

**3. Почему `--slowmo` не помогает найти флейк?**
> Он замедляет действия теста — между действием и проверкой у UI появляется лишнее время, и гонка исчезает.
> Для гонок замедляю приложение: эмуляция медленной сети и CPU, нагрузка, параллель.

**4. Как сделать локальный запуск похожим на CI?**
> Та же команда и окружение, headless, тот же браузер, тот же Docker-образ Playwright, замедление сети и CPU,
> повторы и параллель. Тогда «иногда в CI» превращается в «стабильно у меня».

### Задания — `tests/ui/test_u7_02_debug_ci.py`

```text
U7. Урок 2 — отладка и «в CI падает, локально проходит»; собес по модулю U7.

Теория: practice/u7_02_debug_ci_interview.md
Запуск:
    uv run pytest tests/ui/test_u7_02_debug_ci.py -v

Задача 1. slowmo прячет гонку.
    Возьми naive-тест из U2.1/U2.4 (три пополнения подряд по тосту, ожидание 300) со slow_network(page, 400).
    Запусти обычно — падает; с --slowmo 1000 — что? Объясни в «Ответах».

Задача 2. Медленный CPU.
    Фикстура slow_cpu(page, rate=4) через CDP Emulation.setCPUThrottlingRate.
    Прогони тесты U4.2 (компоненты) с ней и --count 3: что-нибудь стало падать? Если да — разбери по trace
    и почини причину (не таймауты!). Если нет — объясни, почему твои тесты к этому устойчивы.

Задача 3. pdb.
    В тесте сделки (U5.2) поставь breakpoint() после подготовки через API. Запусти с -s --headed:
    в отладчике выведи созданные ордера, сделай page.screenshot(path="/tmp/x.png"), продолжи (c).
    Затем убери breakpoint и запусти с --pdb тест, который падает (U7.1, задача 1): что доступно в отладчике?

Задача 4. Ошибки консоли в отчёте.
    Фикстура console_errors (autouse для UI-тестов? — реши и объясни): собирает pageerror и console.error;
    в teardown прикладывает их в Allure, если есть. Проверь на тесте с abort /balances (U6.1, задача 6).

Задача 5. Режим «как в CI».
    Флаг окружения CI_LIKE=1: в conftest включает headless (игнорирует --headed), slow_network 200 мс и
    slow_cpu 4 для всех страниц, --tracing retain-on-failure по умолчанию. Прогони весь свой набор U4–U5
    с CI_LIKE=1 -n 4. Запиши, что упало и почему.

Задача 6. Разбор кейса (письменно в «Ответах»).
    «Тест "отмена ордера" зелёный локально, в CI падает 1 раз из 10: AssertionError, ожидали статус CANCELED,
    actual NEW. В trace: клик по "Отменить" прошёл, ответ DELETE 200, через 300 мс проверка упала.»
    Гипотеза, как подтвердить, как починить. (Подсказка: U2.1 — что делает UI после ответа и когда перерисовывает таблицу.)

Задача 7. Устный ответ на главный вопрос модуля.
    «Тест упал в CI, локально проходит — твои действия». Запиши ответ по структуре из теории, расскажи вслух
    за 2–3 минуты, сократи лишнее.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Тест упал в CI, а локально проходит. Твои действия?
    2. Какими инструментами отлаживаешь UI-тест?
    3. Почему --slowmo не помогает найти флейк?
    4. Как сделать локальный запуск похожим на CI?
```


---

# U8. Качество: визуал, доступность, производительность

<a id="u8-1"></a>

## U8.1 Визуальная регрессия

*Теория: `practice/u8_01_visual_regression.md`*

Задания: `tests/ui/test_u8_01_visual.py`, код — `ui_framework/utils/visual.py`.

План: что ловит визуальный тест и чего не ловит функциональный; **в Python нет `to_have_screenshot`** — строим
своё сравнение (Pillow + pixelmatch, проверено на стенде); эталоны — где хранить, как обновлять; маски и другие
способы убрать динамику; пороги; почему визуальные тесты флейкают и когда они оправданы.

Модуль U8: U8.1 визуальная регрессия → U8.2 доступность и производительность + собес.

---

#### 1. Что такое визуальный тест

Функциональный тест проверяет **поведение**: «после клика статус CANCELED». Он не заметит, что кнопка уехала
за край экрана, текст белый на белом, таблица налезла на форму, шрифт сломался. Визуальный тест сравнивает
**скриншот с эталоном** и падает, если отличается больше порога.

Ловит: вёрстку, CSS-регрессии, сломанные шрифты и иконки, перекрытия, тему, адаптив.
Не ловит: логику (картинка правильная, данные неверные — если неверные данные выглядят «нормально»).

---

#### 2. В Python нет `to_have_screenshot`

В JS-версии Playwright (`@playwright/test`) есть `expect(page).toHaveScreenshot()` с эталонами, порогами и масками.
**В Python-версии этой проверки нет** — в `LocatorAssertions` / `PageAssertions` её нет (проверено на 1.63).
Варианты:
- готовые плагины (`pytest-playwright-visual` и похожие) — проверь, поддерживается ли твоя версия;
- **своё сравнение** — 30 строк на Pillow и pixelmatch. Так делают часто, и это хороший ответ на собесе.

```python
import io
from pathlib import Path

from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

SNAPSHOTS = Path(__file__).parent / "__snapshots__"


def assert_screenshot(png: bytes, name: str, *, max_diff_pixels: int = 0, threshold: float = 0.1,
                      update: bool = False, artifacts: Path | None = None) -> None:
    expected_path = SNAPSHOTS / f"{name}.png"
    actual = Image.open(io.BytesIO(png)).convert("RGBA")
    if update or not expected_path.exists():               # первый запуск или режим обновления
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        actual.save(expected_path)
        return
    expected = Image.open(expected_path).convert("RGBA")
    assert actual.size == expected.size, f"размер {actual.size} != эталон {expected.size}"
    diff = Image.new("RGBA", actual.size)
    changed = pixelmatch(actual, expected, diff, threshold=threshold)
    if changed > max_diff_pixels:
        if artifacts:                                      # сохранить actual и diff для разбора
            actual.save(artifacts / f"{name}-actual.png")
            diff.save(artifacts / f"{name}-diff.png")
        raise AssertionError(f"{name}: отличается {changed} px (допуск {max_diff_pixels})")
```

- `threshold` (0–1) — насколько должен отличаться **цвет** пикселя, чтобы считаться изменённым (сглаживание шрифтов);
- `max_diff_pixels` / доля от площади — сколько изменённых пикселей допустимо;
- `diff`-картинка — красным изменённые пиксели; прикладывай в Allure (U4.4) вместе с actual и expected.

Проверено на лаборатории (1280×720):

| Сравнение | Изменённых пикселей |
|---|---|
| два скриншота подряд, без маски | **33** — тикают часы в шапке |
| то же с маской на часах | **0** |
| после фильтра котировок «bt» | **166 315** — реальное изменение |

---

#### 3. Эталоны

- лежат **в репозитории** рядом с тестами (`__snapshots__/`), меняются через PR — ревьюер видит картинку;
- **на платформу**: эталон с macOS не совпадёт с Linux в CI (шрифты, сглаживание) — имя с платформой и браузером
  (`lab-chromium-linux.png`) или эталоны генерируют **только** в Docker-образе CI (U9);
- обновление — осознанное: флаг `UPDATE_SNAPSHOTS=1` / опция pytest, только когда изменение ожидаемое;
- первый запуск без эталона: сохранить и **не** считать тест пройденным молча — лучше падать с «эталон создан, проверь».

---

#### 4. Убрать динамику

Динамика — главный источник ложных падений: время, даты, анимации, курсор, случайные данные, реклама, аватары.

| Способ | Как |
|---|---|
| **маска** | `page.screenshot(mask=[clock, avatar])` — закрасить элементы (`mask_color="#FF00FF"`) |
| **скриншот элемента** | `locator.screenshot()` — только стабильный блок, а не вся страница |
| **стабильные данные** | мок API (U6.1) или HAR (U6.2) — одинаковые ордера в каждом прогоне |
| **время** | `page.clock.install(time=...)` + `pause_at` (U6.2) — часы не тикают |
| **анимации** | `screenshot(animations="disabled")` — CSS-анимации к концу, transitions выключены |
| **курсор** | `screenshot(caret="hide")` (по умолчанию) |
| **CSS для тестов** | `screenshot(style="...")` или `add_style_tag` — спрятать баннеры, скроллбары |
| **размер** | фиксированный viewport и `device_scale_factor` в context |
| **шрифты** | дождаться `document.fonts.ready` перед скриншотом |

---

#### 5. Почему визуальные тесты флейкают

- разная **платформа**: ОС, шрифты, GPU, версия браузера;
- **динамика**, которую забыли замаскировать;
- **не дождались**: картинки, шрифты, ленивые блоки ещё грузятся;
- **анимации** и transitions в момент снимка;
- **антиалиасинг** — пиксели по краям текста отличаются от прогона к прогону (лечится `threshold`);
- слишком **большие** скриншоты: изменение где угодно на странице роняет тест.

---

#### 6. Когда оправданы

| Оправдано | Не нужно |
|---|---|
| дизайн-система, библиотека компонентов | быстро меняющийся UI в активной разработке |
| ключевые экраны: главная, оплата, отчёты | всё подряд «на всякий случай» |
| кросс-браузерная / адаптивная вёрстка | данные, которые проверяются текстом |
| регрессии CSS после рефакторинга стилей | когда нет стабильного окружения для эталонов |

Стоимость: поддержка эталонов, ревью картинок, флейки. Начинают с нескольких **компонентов** и экранов, не со всего сайта.
Облачные сервисы (Percy, Applitools, Chromatic) — хранение эталонов, ревью diff в браузере, «умное» сравнение.

---

#### Собес: вопросы и ответы

**1. Как делаешь визуальное тестирование в Playwright на Python?**
> В Python нет встроенного `to_have_screenshot`, поэтому сравниваю сам: скриншот страницы или элемента, эталон
> в репозитории, pixelmatch с порогом по цвету и допуском по числу пикселей, при падении сохраняю actual и diff
> в отчёт. Либо плагин или облачный сервис. Эталоны генерирую в том же Docker-образе, что CI.

**2. Почему визуальные тесты флейкают и что с этим делать?**
> Разная платформа и шрифты, динамика — время, данные, анимации, — не догрузились картинки и шрифты, антиалиасинг.
> Лечу: эталоны в одном окружении с CI, маски динамики, стабильные данные через моки, фиксированное время через
> clock, отключённые анимации, скриншот элемента вместо страницы, разумный порог.

**3. Когда визуальные тесты оправданы?**
> Для дизайн-системы и компонентов, ключевых экранов, адаптивной и кросс-браузерной вёрстки, после рефакторинга CSS.
> Не для быстро меняющегося UI и не вместо функциональных проверок. Начинаю с небольшого набора — поддержка эталонов
> стоит времени.

**4. Как обновляешь эталоны?**
> Только осознанно: флаг обновления, новые эталоны — через PR, где ревьюер видит картинки. Генерирую их в Docker-образе
> CI, чтобы не было расхождений платформы.

### Задания — `tests/ui/test_u8_01_visual.py`

```text
U8. Урок 1 — визуальная регрессия.

Теория: practice/u8_01_visual_regression.md
Код: ui_framework/utils/visual.py (создай: assert_screenshot по теории).
Подготовка: uv sync (pillow, pixelmatch уже в группе tests).
Запуск:
    uv run pytest tests/ui/test_u8_01_visual.py -v
    UPDATE_SNAPSHOTS=1 uv run pytest tests/ui/test_u8_01_visual.py     # пересоздать эталоны

Эталоны — tests/ui/__snapshots__/ (в git). Помни: эталоны с macOS не совпадут с Linux в CI (U9).

Задача 1. assert_screenshot(png, name, max_diff_pixels=0, threshold=0.1).
    Флаг UPDATE_SNAPSHOTS из окружения (или из Settings). Нет эталона — создать и упасть с понятным
    сообщением «эталон создан, проверь картинку» (не проходить молча). При падении — actual и diff
    в output_path теста (U7.1) и в Allure.
    Тесты без браузера: одинаковые картинки → ок; картинка с 10 изменёнными пикселями → падение,
    с max_diff_pixels=10 → ок; разный размер → понятная ошибка.

Задача 2. Динамика.
    Скриншот лаборатории дважды с интервалом > 1 с без маски — сколько пикселей отличается и почему?
    С маской на часах — 0. Тест «страница лаборатории стабильна» с маской.

Задача 3. Скриншот компонента.
    Эталон таблицы котировок (locator.screenshot). Сортировка по цене ↓ — тест падает; diff-картинка
    показывает, что изменилось. Сделай эталон для отсортированного состояния тоже.

Задача 4. Стабильные данные.
    Кабинет (/app/) с моком GET /orders и GET /balances (U6.1) — фиксированные ордера и балансы.
    Эталон блока «Мои ордера». Почему без мока этот тест невозможен?

Задача 5. Время и анимации.
    Лаборатория с page.clock.install(time="2030-01-15T10:00:00Z") + pause_at — часы стоят, маска не нужна.
    Скриншот с animations="disabled". Сравни подход «маска» и «clock» — что надёжнее и почему?

Задача 6. Адаптив.
    Эталоны лаборатории для viewport 1440×900 и 390×844 (U6.3). Проверь, что на мобильном карточки в одну колонку
    (это видно и функционально — как? Подумай, нужна ли тут картинка).

Задача 7. Ловим настоящую регрессию.
    page.add_style_tag(content=".dnd li { padding: 30px }") перед скриншотом избранного — тест упал? Сколько пикселей?
    Подбери порог, при котором тест ловит такое изменение, но не падает от антиалиасинга (запусти 5 раз --count).

Задача 8. Письменно в «Ответах».
    Предложи визуальное покрытие для биржи: какие 5 экранов/компонентов, что маскировать, где генерировать эталоны,
    кто и как их обновляет.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как делаешь визуальное тестирование в Playwright на Python?
    2. Почему визуальные тесты флейкают и что с этим делать?
    3. Когда визуальные тесты оправданы?
    4. Как обновляешь эталоны?
```

<a id="u8-2"></a>

## U8.2 Доступность и производительность фронта; собес по модулю U8

*Теория: `practice/u8_02_a11y_perf_interview.md`*

Задания: `tests/ui/test_u8_02_a11y_perf.py`.

План: доступность (a11y) — что это и кому нужно; axe-core через `axe-playwright-python` (проверено:
находит проблемы на лаборатории и 0 в кабинете); что автоматическая проверка не найдёт — и как дотестировать
Playwright'ом (роли, имена, фокус, клавиатура); производительность фронта — Navigation Timing, Web Vitals
(LCP, CLS, INP), метрики CDP, число и размер запросов; бюджеты без флейков; собес по U8.

---

#### 1. Доступность

**Accessibility (a11y)** — сайтом могут пользоваться люди с особенностями: незрячие (скринридер), слабовидящие
(контраст, масштаб), без мыши (клавиатура), с моторными нарушениями. Стандарт — **WCAG 2.1/2.2**, уровни A / AA / AAA;
в требованиях обычно **AA**. Для многих компаний это закон (EAA в ЕС с 2025, ADA в США).

Для тестировщика это не отдельный мир: **локаторы по ролям** (U1.2) уже проверяют доступность — если
`get_by_role("button", name="Пополнить")` не находит кнопку, её не найдёт и скринридер.

---

#### 2. axe-core в Playwright

axe-core — движок автоматических проверок доступности (Deque). Для Python — пакет `axe-playwright-python`
(в группе `tests`):

```python
from axe_playwright_python.sync_playwright import Axe

axe = Axe()
results = axe.run(page)                                  # проверка текущей страницы
results.violations_count                                 # число правил с нарушениями
for v in results.response["violations"]:
    print(v["id"], v["impact"], v["help"], len(v["nodes"]))
    for node in v["nodes"]:
        print("   ", node["target"], node["failureSummary"])
print(results.generate_report())                         # читаемый отчёт — приложить в Allure
```

Проверено: на лаборатории axe находит **3 правила** с нарушениями (разной серьёзности), в кабинете `/app/` — **0**.
Какие именно на лаборатории — найдёшь в задании 1.

| Поле | Что |
|---|---|
| `id` | правило: `image-alt`, `color-contrast`, `button-name`, `label`, `region`, `landmark-*` … |
| `impact` | `critical`, `serious`, `moderate`, `minor` |
| `nodes[].target` | CSS-путь к элементу |
| `help`, `helpUrl` | что не так и ссылка на объяснение |

Настройки: проверить часть страницы (`axe.run(page, context="#dashboard")`), только нужные стандарты
(`options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}}`), отключить правило.

##### Как встроить

- тест на ключевые страницы: «нет нарушений `critical` и `serious`» — порог, а не «ноль всего»;
- известные нарушения — **список исключений** с ссылками на задачи (как карантин, U2.4), иначе тест вечно красный
  и его выключат;
- проверять **разные состояния**: открытое меню, ошибка формы, модалка — axe видит только текущий DOM.

---

#### 3. Чего axe не найдёт

Автоматика находит примерно **треть** проблем доступности. Остальное — поведение:

| Проблема | Как проверить Playwright'ом |
|---|---|
| кнопка-иконка с «именем» `⟳` — формально имя есть, по смыслу нет | `expect(button).to_have_accessible_name("Обновить")` |
| порядок фокуса | `page.keyboard.press("Tab")` + `expect(el).to_be_focused()` по цепочке |
| форма проходится без мыши | Tab, ввод, Enter — сценарий только клавиатурой |
| фокус после закрытия модалки возвращается на кнопку | `to_be_focused()` после закрытия |
| ошибка поля связана с полем | `to_have_accessible_description` / `to_have_accessible_error_message` |
| структура и имена | `to_match_aria_snapshot` (U1.2) |
| динамические сообщения читаются скринридером | у тоста `role="status"` (U4.2): `to_have_role("status")` |

---

#### 4. Производительность фронта

Это **не** нагрузочное тестирование (Locust — в части API): здесь один пользователь, вопрос — насколько быстро
страница отрисовывается и откликается.

##### Navigation Timing

```python
nav = page.evaluate("performance.getEntriesByType('navigation')[0].toJSON()")
ttfb = nav["responseStart"] - nav["requestStart"]       # время до первого байта
dcl = nav["domContentLoadedEventEnd"]                    # HTML разобран
load = nav["loadEventEnd"]                               # всё загружено
```

##### Web Vitals

| Метрика | Что | Хорошо |
|---|---|---|
| **LCP** (Largest Contentful Paint) | отрисован самый большой элемент | < 2,5 с |
| **CLS** (Cumulative Layout Shift) | насколько «прыгает» вёрстка | < 0,1 |
| **INP** (Interaction to Next Paint) | отклик на действие пользователя | < 200 мс |
| FCP (First Contentful Paint) | первый контент на экране | < 1,8 с |

Собрать — подписаться на события до загрузки:

```python
page.add_init_script("""
  window.__vitals = {lcp: 0, cls: 0};
  new PerformanceObserver(list => {
    for (const e of list.getEntries()) window.__vitals.lcp = e.startTime;
  }).observe({type: 'largest-contentful-paint', buffered: true});
  new PerformanceObserver(list => {
    for (const e of list.getEntries()) if (!e.hadRecentInput) window.__vitals.cls += e.value;
  }).observe({type: 'layout-shift', buffered: true});
""")
page.goto("/app/lab.html")
vitals = page.evaluate("window.__vitals")
fcp = page.evaluate("performance.getEntriesByName('first-contentful-paint')[0]?.startTime")
```

Проверено на лаборатории (локально): TTFB ≈ 3 мс, DCL ≈ 130 мс, load ≈ 135 мс, LCP = FCP ≈ 176 мс, CLS = 0.
INP требует реального взаимодействия — его меряют действием (клик) и событием `event` в PerformanceObserver
или библиотекой `web-vitals`.

##### CDP и сеть

```python
cdp = page.context.new_cdp_session(page)
cdp.send("Performance.enable")
metrics = {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}
metrics["JSHeapUsedSize"], metrics["Nodes"], metrics["LayoutCount"]
```

Число и вес запросов — `page.on("response", ...)`: страница грузит 150 запросов или картинку 5 МБ — это видно и без
Lighthouse. Lighthouse (полный аудит) запускают отдельно (CLI) на тех же страницах.

##### Бюджеты без флейков

- метрики **шумят**: CI медленнее (U7.2), соседние джобы. Порог — с запасом (LCP < 2,5 с, а не < 200 мс);
- несколько замеров и **медиана**, а не один;
- одинаковые условия: throttling сети и CPU (U2.1, U7.2) — сравнимо от прогона к прогону;
- отдельный маркер (`perf`) и отдельный прогон — не мешать функциональным тестам;
- тренд важнее одного числа: писать метрики в отчёт и смотреть, как меняются от релиза к релизу.

---

#### 5. Шпаргалка по модулю U8

- Визуал (U8.1): в Python нет `to_have_screenshot` — своё сравнение Pillow + pixelmatch (`threshold`, допуск пикселей,
  actual/diff в отчёт); эталоны в git и в окружении CI; маски, скриншот элемента, моки, clock, `animations="disabled"`.
- Доступность (U8.2): axe через `axe-playwright-python`, порог по `impact`, исключения с задачами, разные состояния;
  axe находит треть — остальное ролями, именами, фокусом, клавиатурой.
- Производительность (U8.2): Navigation Timing, LCP/CLS/INP/FCP через PerformanceObserver, CDP-метрики, запросы;
  бюджеты с запасом, медиана, одинаковые условия, тренд.

---

#### Собес: вопросы и ответы

Плюс вопросы U8.1 (4).

**1. Как проверяешь доступность в автотестах?**
> axe-core через Playwright на ключевых страницах и состояниях — меню, ошибки, модалки; падаю на critical и serious,
> известные проблемы — в исключениях с задачами. Плюс то, что axe не видит: имена кнопок по смыслу, порядок фокуса,
> прохождение сценария только клавиатурой, возврат фокуса, связь ошибок с полями. Локаторы по ролям — уже
> проверка доступности.

**2. Что такое Web Vitals и как их измерить в Playwright?**
> LCP — когда отрисован главный контент, CLS — насколько прыгает вёрстка, INP — отклик на действие; плюс FCP, TTFB.
> Подписываюсь через PerformanceObserver в init script до загрузки и читаю значения из страницы; Navigation Timing —
> через `performance.getEntriesByType`. Бюджеты — с запасом, медиана нескольких замеров, одинаковый throttling.

**3. Чем проверка производительности фронта отличается от нагрузочного тестирования?**
> Здесь один пользователь и вопрос «насколько быстро отрисовывается и откликается страница» — метрики браузера.
> Нагрузка — много одновременных пользователей и поведение сервера: RPS, перцентили, ошибки — это Locust или k6.

**4. Почему тесты производительности в CI флейкают?**
> Шумит окружение: другая машина, соседние джобы, сеть. Поэтому пороги с запасом, медиана, фиксированный throttling,
> отдельный прогон и внимание к тренду, а не к одному числу.

### Задания — `tests/ui/test_u8_02_a11y_perf.py`

```text
U8. Урок 2 — доступность и производительность фронта; собес по модулю U8.

Теория: practice/u8_02_a11y_perf_interview.md
Подготовка: uv sync (axe-playwright-python уже в группе tests).
Запуск:
    uv run pytest tests/ui/test_u8_02_a11y_perf.py -v -s

Задача 1. axe на лаборатории.
    Запусти Axe().run(page) на /app/lab.html. Какие правила нарушены, какой impact, на каких элементах?
    Для каждого нарушения — в «Ответах»: что не так, кому мешает, как исправить в разметке.
    (Стенд пишу я — исправлять не надо, нужен анализ. Хочешь — опиши как issue.)

Задача 2. Хелпер assert_no_a11y_violations(page, impacts=("critical", "serious"), ignore=(), context=None).
    Падает с читаемым списком (правило, impact, target), прикладывает generate_report() в Allure.
    ignore — список id правил с комментарием-ссылкой на задачу.
    Тесты: кабинет /app/ (форма входа) и кабинет после входа — 0 нарушений; лаборатория — падает,
    с ignore известных — проходит.

Задача 3. Состояния.
    axe на кабинете в состояниях: ошибка входа видна; ошибка формы ордера видна; таблица ордеров с 3 строками.
    Меню «Ещё» в лаборатории открыто. Что-то поменялось по сравнению со «спокойным» состоянием?

Задача 4. Чего axe не видит.
    а) Кнопка «⟳» в блоке «Окружение»: axe молчит? Проверь её доступное имя (to_have_accessible_name) —
       что там и почему это проблема для скринридера.
    б) Форма входа только с клавиатуры: Tab → Email (to_be_focused), ввод, Tab → Пароль, ввод, Tab → «Войти»,
       Enter → кабинет. Регистрация так же.
    в) Тост — role="status" (to_have_role).

Задача 5. Navigation Timing и Web Vitals.
    Фикстура web_vitals: init script из теории, после goto — dict с ttfb, dcl, load, fcp, lcp, cls.
    Выведи для /app/ и /app/lab.html (-s). Прикладывай в Allure как JSON.

Задача 6. Бюджет без флейков.
    Тест perf (маркер perf, зарегистрируй): 5 загрузок лаборатории, медиана LCP < 2500 мс, CLS < 0.1.
    То же со slow_network(400) и slow_cpu(4) (U7.2) — что стало с медианой? Влезает в бюджет?

Задача 7. Запросы страницы.
    page.on("response") — сколько запросов и сколько байт (по content-length или body()) при загрузке кабинета
    после входа? Какие запросы повторяются каждые 2 секунды?

Задача 8. Устный собес по модулю U8.
    8 вопросов из «Собес» U8.1–U8.2, вслух. Номера, где «поплыл», — в «Ответы».

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как проверяешь доступность в автотестах?
    2. Что такое Web Vitals и как их измерить в Playwright?
    3. Чем проверка производительности фронта отличается от нагрузочного тестирования?
    4. Почему тесты производительности в CI флейкают?
```


---

# U9. Масштаб и CI

<a id="u9-1"></a>

## U9.1 Параллель, шардирование и кросс-браузерность

*Теория: `practice/u9_01_parallel_sharding_browsers.md`*

Задания: `tests/ui/test_u9_01_parallel_browsers.py`.

План: масштаб прогона — процессы (xdist) и машины (шарды); как шардировать без плагинов (проверено:
без пересечений и потерь) и с pytest-split по длительности; где предел ускорения; кросс-браузерность —
зачем, как запускать, маркеры; **у нас локально только Chrome** (проверено) — остальные браузеры в Docker.

Модуль U9: U9.1 параллель, шарды, браузеры → U9.2 Docker, CI, артефакты, стабильность + собес.

---

#### 1. Два уровня масштаба

| Уровень | Чем | Что делит |
|---|---|---|
| **процессы** на одной машине | pytest-xdist: `-n 4` (U5.3) | тесты между воркерами |
| **машины** в CI | шарды: `SHARD_INDEX` из `SHARD_TOTAL` | набор на части по машинам |

Комбинируют: 4 машины × `-n 4` = 16 параллельных потоков.

Всё из U5.3 остаётся в силе: изоляция данных, seed на контроллере, общие ресурсы, `base_url` под xdist.
На шардах добавляется: каждая машина — **отдельный прогон** (свой `testrun_uid`), поэтому общий `RUN_ID`
для данных и уборки задают снаружи — номером сборки CI (U5.2).

---

#### 2. Шардирование

##### Без плагинов — хешем nodeid

```python
# tests/conftest.py
import os
import zlib


def pytest_collection_modifyitems(config, items):
    total = int(os.getenv("SHARD_TOTAL", "1"))
    index = int(os.getenv("SHARD_INDEX", "0"))
    if total <= 1:
        return
    selected, deselected = [], []
    for item in items:
        bucket = zlib.crc32(item.nodeid.encode()) % total
        (selected if bucket == index else deselected).append(item)
    config.hook.pytest_deselected(items=deselected)       # чтобы pytest показал «N deselected»
    items[:] = selected
```

Проверено: 40 тестов на 3 шарда → 16 + 14 + 10, объединение — ровно 40 уникальных, пересечений нет.

- `zlib.crc32`, а **не** встроенный `hash()`: у `hash()` для строк случайная соль в каждом процессе
  (`PYTHONHASHSEED`) — на разных машинах тест попал бы в разные шарды или ни в один;
- хеш по `nodeid` — тест всегда в одном и том же шарде, новые тесты не перетасовывают старые;
- минус — шарды **неравные** по времени (16 тестов против 10, и тесты разной длины).

##### По длительности — pytest-split

```bash
uv run pytest --store-durations                          # один раз: записать .test_durations
uv run pytest --splits 4 --group 1                       # машина 1 из 4, группы равны по времени
```

Файл `.test_durations` коммитят и обновляют время от времени.

##### Где предел ускорения

Время прогона ≈ самый долгий шард + запуск окружения. Ускорение не линейное (U5.3, задача 8):
- **стенд** один на всех — 16 потоков нагружают его, растут ответы и флейки;
- **подготовка окружения** на каждой машине (образ, браузер, стенд) — фиксированная цена;
- **длинные тесты** — один тест на 3 минуты ограничивает шард снизу;
- session-фикстуры выполняются на каждом воркере и шарде.

---

#### 3. Кросс-браузерность

Playwright умеет три движка: **Chromium** (Chrome, Edge), **Firefox**, **WebKit** (движок Safari).

```bash
uv run pytest --browser chromium --browser firefox --browser webkit    # каждый тест × 3
uv run pytest --browser-channel chrome                                 # системный Chrome (как у нас)
uv run pytest --browser-channel msedge
```

В имени теста — браузер: `test_deposit[chromium]`, `test_deposit[firefox]`.

```python
@pytest.mark.skip_browser("webkit")                  # не запускать в WebKit (с причиной в комментарии)
@pytest.mark.only_browser("chromium")                # только в Chromium (CDP: slow_network, slow_cpu)
def test_x(page, browser_name, is_webkit): ...
```

Наши хелперы `slow_network` и CPU throttling работают **только в Chromium** (CDP) — такие тесты помечай
`only_browser("chromium")`.

##### Когда нужно

| Нужно | Не нужно |
|---|---|
| заметная доля пользователей на Safari / Firefox (аналитика) | внутренняя админка «только Chrome» |
| вёрстка и CSS, формы, даты (`input type=date` разный), файлы, буфер обмена | бизнес-логика — она одинакова, это бэкенд |
| smoke-набор на всех браузерах | весь регресс × 3 на каждый PR |

Типичная схема: полный набор — в Chromium на каждый PR; smoke в Firefox и WebKit — ночью или перед релизом.
WebKit Playwright ≠ настоящий Safari на macOS/iOS, но ловит большинство WebKit-специфичных багов.

##### У нас локально — только Chrome

Проверено: на macOS 12 Playwright **не поддерживает** свои Chromium, Firefox, WebKit и ffmpeg
(`Playwright does not support firefox on mac12`). Поэтому в `addopts` стоит `--browser-channel chrome` —
системный Chrome. Firefox, WebKit и видео — **в Docker-образе Playwright** (U9.2) или в CI на Linux.

---

#### Собес: вопросы и ответы

**1. Как ускорить большой UI-набор?**
> Подготовка через API и storage_state, без sleep — это первое. Потом параллель: xdist на машине и шарды
> между машинами CI, шарды лучше делить по длительности. Данные изолированы, seed — вне воркеров.
> Ускорение упирается в стенд, подготовку окружения и самые длинные тесты — их дроблю.

**2. Как шардировать тесты между машинами CI?**
> pytest-split по записанным длительностям — шарды равны по времени. Без плагина — детерминированный хеш
> nodeid по модулю числа шардов в хуке сбора; именно стабильный хеш, а не встроенный `hash`, у которого
> случайная соль. Общий id прогона для данных — из номера сборки.

**3. Нужна ли кросс-браузерность и как её организуешь?**
> Зависит от аудитории: смотрю аналитику. Если нужна — полный набор в Chromium на PR, smoke в Firefox и WebKit
> ночью. Запуск — `--browser` несколько раз; тесты на CDP-возможности помечаю `only_browser("chromium")`.
> Помню, что WebKit Playwright — не настоящий Safari, критичное проверяю на реальных устройствах.

**4. Почему ускорение от параллели не линейное?**
> Общий стенд нагружается, у каждой машины и воркера фиксированная стоимость старта, session-фикстуры
> выполняются на каждом воркере, а время прогона ограничено самым длинным шардом.

### Задания — `tests/ui/test_u9_01_parallel_browsers.py`

```text
U9. Урок 1 — параллель, шардирование и кросс-браузерность.

Теория: practice/u9_01_parallel_sharding_browsers.md
Запуск:
    uv run pytest tests/ui/test_u9_01_parallel_browsers.py -v

Задача 1. Шарды.
    Хук шардирования в tests/conftest.py (по теории). Проверь на всём tests/ui:
        SHARD_TOTAL=3 SHARD_INDEX=0..2 uv run pytest tests/ui --collect-only -q
    Скриптом (или руками) убедись: объединение трёх шардов == полный набор, пересечений нет.
    Замени crc32 на hash() и запусти дважды для одного шарда — состав меняется? Почему? (PYTHONHASHSEED.)

Задача 2. Шарды по длительности.
    uv add --group tests pytest-split; --store-durations на tests/ui/test_u4_0*.py tests/ui/test_u5_0*.py;
    --splits 3 --group N — сравни суммарное время групп с хешевыми шардами. Запиши в «Ответы».

Задача 3. Шарды × xdist.
    SHARD_TOTAL=2 SHARD_INDEX=0 uv run pytest ... -n 2 и SHARD_INDEX=1 — одновременно в двух терминалах.
    Что нужно, чтобы данные двух «машин» не пересекались (RUN_ID, U5.2)? Сделай: RUN_ID из TEST_RUN_ID.

Задача 4. Маркеры браузеров.
    Пометь only_browser("chromium") все свои тесты, где есть slow_network / slow_cpu / CDP.
    Найди их по коду (grep new_cdp_session) — сколько? Есть ли такие, где CDP можно заменить на route (U6.1)?

Задача 5. browser_name.
    Тест, который печатает browser_name, is_chromium, browser.version и page.evaluate("navigator.userAgent").
    Запусти с --browser chromium --browser-channel chrome и без channel. Что получилось и почему (раздел 3 теории)?

Задача 6. Кросс-браузерный smoke (в Docker — после U9.2).
    Маркер smoke у 5 ключевых тестов (вход, пополнение, ордер, отмена, лаборатория: popup + iframe).
    Команда для запуска на трёх браузерах — запиши; запустишь её в Docker-образе в U9.2, задача 3.

Задача 7. Письменно в «Ответах».
    Набор из 600 UI-тестов, полный прогон 90 минут на одной машине. Цель — 15 минут на PR.
    Распиши план: что в PR, что ночью, сколько шардов и воркеров, какие браузеры, что упрётся первым.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как ускорить большой UI-набор?
    2. Как шардировать тесты между машинами CI?
    3. Нужна ли кросс-браузерность и как её организуешь?
    4. Почему ускорение от параллели не линейное?
```

<a id="u9-2"></a>

## U9.2 Docker-образ Playwright, CI, артефакты и стабильность; собес по модулю U9

*Теория: `practice/u9_02_docker_ci_stability.md`*

Задания: `tests/ui/test_u9_02_docker_ci.py`.

План: зачем тесты в Docker; официальный образ Playwright и запуск наших тестов в нём против стенда
(проверено на U1.4: WebKit — 9/9, Firefox — 8/9, один тест упал на проверке видимости, его разбор — задание 3); подводные камни (venv, `addopts`, сеть,
`--ipc=host`); CI на GitHub Actions — пайплайн целиком; артефакты; ретраи и карантин в CI; метрики стабильности; собес.

---

#### 1. Зачем Docker

- **одинаковое окружение**: та же ОС, шрифты, браузеры, что в CI — нет «у меня работает» (U7.2) и расхождения
  эталонов скриншотов (U8.1);
- **все браузеры и ffmpeg**: на нашей macOS 12 Playwright даёт только системный Chrome (U9.1), в образе — Chromium,
  Firefox, WebKit и видео;
- CI-раннеры и так запускают джобы в контейнерах — локальный запуск в образе = воспроизведение CI.

---

#### 2. Официальный образ

`mcr.microsoft.com/playwright/python:v1.63.0-noble` — Ubuntu 24.04 + Python + браузеры **той же версии**, что пакет
`playwright` (тег = версия пакета; несовпадение версий — «Executable doesn't exist»). `-jammy` — Ubuntu 22.04.

Внутри: браузеры Playwright и системные зависимости. **Нет**: наших зависимостей (uv, pytest-плагины) и системного
Google Chrome — `--browser-channel chrome` в образе не сработает.

##### Запуск наших тестов в образе

```bash
docker run --rm --ipc=host \
  -v "$PWD":/work -w /work \
  -e UV_PROJECT_ENVIRONMENT=/tmp/venv \
  --add-host=host.docker.internal:host-gateway \
  mcr.microsoft.com/playwright/python:v1.63.0-noble \
  bash -c "pip install -q uv && uv sync --frozen -q && \
           uv run pytest tests/ui/test_u1_04_context_pytest.py -o addopts='-ra --strict-markers' \
             --base-url http://host.docker.internal:8080 --browser firefox --browser webkit"
```

Разбор флагов — каждый из них важен:

| Флаг | Зачем |
|---|---|
| `--ipc=host` | Chromium использует общую память; без этого падает на больших страницах |
| `-v "$PWD":/work` | код из репозитория |
| `-e UV_PROJECT_ENVIRONMENT=/tmp/venv` | **не трогать** `.venv` хоста: там бинарники macOS, uv в Linux его бы пересоздал |
| `--add-host=host.docker.internal:host-gateway` | доступ к стенду на хосте (`:8080`) из контейнера |
| `-o addopts='...'` | убрать `--browser-channel chrome` из `pyproject` — Chrome в образе нет |
| `--base-url` | адрес стенда из контейнера — не `localhost` (это сам контейнер) |

Лучше вместо `-o addopts` сделать канал **настраиваемым**: в `addopts` его не держать, а передавать из Settings / CI
(задача 2) — тогда одна команда работает везде.

Альтернатива `host.docker.internal` — запустить тесты **в той же сети docker compose**, что стенд:
`--network api_learning_default` и `--base-url http://exchange:8000`.

---

#### 3. CI на GitHub Actions

Пайплайн UI-тестов (файл `.github/workflows/ui-tests.yml` — создаёшь в задании 4):

```yaml
name: ui-tests
on:
  pull_request:
  schedule: [{cron: "0 2 * * *"}]          # ночной полный прогон

concurrency:                               # новый пуш в PR отменяет старый прогон
  group: ui-${{ github.ref }}
  cancel-in-progress: true

jobs:
  ui:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        shard: [0, 1, 2]
    env:
      SHARD_TOTAL: 3
      SHARD_INDEX: ${{ matrix.shard }}
      TEST_RUN_ID: ${{ github.run_id }}     # общий RUN_ID для данных всех шардов (U5.2, U9.1)
      ENV: docker
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with: {enable-cache: true}
      - name: Стенд
        run: docker compose up -d --build --wait
      - name: Зависимости и браузер
        run: |
          uv sync --frozen
          uv run playwright install --with-deps chromium
      - name: Тесты
        run: >
          uv run pytest tests/ui -m "smoke or regression" -n 2
          --browser chromium --tracing retain-on-failure --screenshot only-on-failure
          --alluredir allure-results --junitxml report-${{ matrix.shard }}.xml
      - name: Артефакты
        if: always()                        # и при падении — именно тогда они нужны
        uses: actions/upload-artifact@v4
        with:
          name: ui-${{ matrix.shard }}
          path: |
            test-results/
            allure-results/
            report-*.xml
          retention-days: 14
      - name: Логи стенда
        if: failure()
        run: docker compose logs exchange > exchange.log
```

Ключевые решения:
- `--with-deps` ставит системные библиотеки браузера на Ubuntu;
- `--browser chromium` без channel — Chromium Playwright, а не системный Chrome;
- `fail-fast: false` — падение одного шарда не отменяет остальные, видно всю картину;
- `if: always()` у артефактов; логи стенда при падении (U2.4: поиск по X-Request-ID);
- `--wait` у compose — дождаться healthcheck стенда;
- секреты — `${{ secrets.UI_USER_PASSWORD }}` в `env`, не в файле (U4.3).

Allure-отчёт из нескольких шардов собирают отдельной джобой: скачать все `allure-results`, `allure generate`,
опубликовать (GitHub Pages / артефакт). История и тренды — сохранять папку `history` между прогонами.

Jenkins и GitLab CI устроены так же: стадии, матрица/параллель, артефакты, `always`-шаги. Подробно — модуль 9 части API.

---

#### 4. Ретраи и карантин в CI

Повтор U2.4 с точки зрения CI:

```bash
uv run pytest ... --reruns 2 --reruns-delay 1 --only-rerun "TimeoutError|503"
```

- `--only-rerun` — перезапускать только по похожим на инфраструктуру ошибкам, а не любые `AssertionError`;
- тест, прошедший с перезапуска, — **флейк**: в отчёте `RERUN`, по нему заводится задача;
- карантин — маркер `quarantine`, отдельная джоба «карантин» с `continue-on-error: true`: тесты бегут, но не блокируют PR;
- выход из карантина — серия зелёных прогонов (`--count 50` ночью).

#### 5. Метрики стабильности

| Метрика | Как считать | Зачем |
|---|---|---|
| **pass rate** | доля зелёных прогонов набора | общее здоровье |
| **flaky rate** | тестов, прошедших с rerun / всех тестов | сколько «шума» |
| **топ флейков** | тесты по числу rerun за 2 недели | что чинить первым |
| размер карантина | тестов в карантине и как давно | не превращается ли в кладбище |
| длительность | p50/p95 прогона и шардов | деградация, перекос шардов |
| время до починки | от появления флейка до исправления | процесс работает? |

Источник данных — JUnit XML (`--junitxml`), Allure history, API CI. Без метрик флейки накапливаются молча.

---

#### 6. Шпаргалка по модулю U9

- Масштаб: xdist (процессы) × шарды (машины); шард — стабильный хеш nodeid или pytest-split по длительности;
  общий `RUN_ID` из CI; ускорение упирается в стенд и самые длинные тесты.
- Браузеры: `--browser` × N, `only_browser`/`skip_browser`; CDP-хелперы — только Chromium; у нас локально только Chrome.
- Docker: образ `playwright/python:v<версия>-noble`, `--ipc=host`, отдельный venv, сеть до стенда, без channel chrome.
- CI: стенд → зависимости → `playwright install --with-deps` → тесты с шардами → артефакты `if: always()` → Allure.
- Стабильность: rerun только по инфраструктурным ошибкам, флейк = задача, карантин не блокирует, метрики.

---

#### Собес: вопросы и ответы

Плюс вопросы U9.1 (4).

**1. Как запускаете UI-тесты в CI?** (вопрос из программы)
> На каждый PR — smoke и регресс в Chromium, шардами по машинам и xdist внутри. Стенд поднимается в docker compose
> с ожиданием healthcheck, зависимости через uv с кэшем, браузеры — `playwright install --with-deps` или готовый
> образ Playwright. Артефакты — trace, скриншоты, Allure, логи стенда — выгружаются всегда. Ночью — полный набор и
> кросс-браузерный smoke. Секреты из CI.

**2. Как параллелите?** (из программы)
> xdist внутри машины, матрица шардов между машинами; шарды по длительности. Данные изолированы: уникальные значения
> с id сборки, seed вне воркеров, общие ресурсы — без пересечений.

**3. Что делаете с флейками?** (из программы)
> Ретрай только на инфраструктурные ошибки и как сигнал, а не лечение: прошедший с rerun тест — задача. Не чинится
> сразу — карантин с владельцем в неблокирующей джобе. Смотрим метрики — flaky rate и топ флейков, — чиним причины
> по категориям (U2.4).

**4. Зачем запускать тесты в Docker?**
> Одинаковое окружение с CI — ОС, шрифты, браузеры той же версии, — значит воспроизводимые падения и эталоны
> скриншотов. Плюс все браузеры и видео там, где локальная ОС их не поддерживает, как у нас на macOS 12.

**5. Какие подводные камни у запуска в контейнере?**
> Версия образа должна совпадать с пакетом playwright. `--ipc=host` для Chromium. Не затирать venv хоста.
> `localhost` в контейнере — это контейнер, стенд — через host.docker.internal или общую сеть compose.
> Системного Chrome в образе нет.

### Задания — `tests/ui/test_u9_02_docker_ci.py`

```text
U9. Урок 2 — Docker-образ Playwright, CI, артефакты и стабильность; собес по модулю U9.

Теория: practice/u9_02_docker_ci_stability.md
Подготовка: docker pull mcr.microsoft.com/playwright/python:v1.63.0-noble (≈1,5 ГБ).
Большая часть задач — команды и конфиги, а не тесты в этом файле.

Задача 1. Тесты в Docker.
    Запусти U1.4 в образе командой из теории (раздел 2) — сначала в Chromium.
    Разбери в «Ответах» каждый флаг: что сломается без него? Проверь на практике -o addopts и --ipc=host.
    UV_PROJECT_ENVIRONMENT НЕ убирай: uv в контейнере пересоздаст .venv хоста под Linux, и на Mac
    придётся делать uv sync заново — просто объясни, почему так.

Задача 2. Канал браузера из конфига.
    Убери --browser-channel chrome из addopts в pyproject. Сделай так, чтобы на хосте канал chrome
    подставлялся сам (Settings.browser_channel + фикстура browser_type_launch_args или pytest_configure),
    а в Docker/CI — нет (переменная окружения). Одна и та же команда pytest работает в обоих местах.

Задача 3. Кросс-браузерный smoke в Docker.
    Smoke из U9.1 (задача 6) на --browser chromium --browser firefox --browser webkit в образе.
    Что упало только в одном браузере? Это баг стенда, теста или ограничение (CDP-хелперы)?
    Добавь видео: --video retain-on-failure — где лежит webm, открывается?

Задача 4. Workflow.
    .github/workflows/ui-tests.yml по теории (раздел 3): шарды, стенд, артефакты, логи стенда.
    Проверь синтаксис (actionlint, если поставишь, или внимательно глазами). Запуск на GitHub —
    когда дойдём до CI в модуле 0/9 (пока не пушь workflow, если не готов к красным прогонам).
    В «Ответах»: что поменяешь для ночного прогона (браузеры, маркеры, -n, таймаут).

Задача 5. JUnit и метрики.
    Прогони набор U4–U5 с --junitxml=report.xml --reruns 1 -n 4 (лучше на stage, U2.4).
    Скрипт (python, xml.etree): сколько тестов, сколько упало, сколько прошло с перезапуска (rerun),
    топ-5 самых долгих. Это заготовка метрик стабильности из теории.

Задача 6. only-rerun.
    --reruns 2 --only-rerun "TimeoutError|503": на тесте с AssertionError — перезапустился? на тесте с 503
    (мок, U6.1) — перезапустился? Объясни, зачем фильтр.

Задача 7. Карантин в CI (письменно + конфиг).
    Маркер quarantine (U2.4). В workflow — отдельная джоба для карантина с continue-on-error: true,
    основная — -m "not quarantine". Правило выхода из карантина — запиши.

Задача 8. Устный собес по модулю U9.
    9 вопросов из «Собес» U9.1–U9.2, вслух. Главные три из программы — «как запускаете в CI, как параллелите,
    что делаете с флейками» — одним связным ответом на 3 минуты.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как запускаете UI-тесты в CI?
    2. Как параллелите?
    3. Что делаете с флейками?
    4. Зачем запускать тесты в Docker?
    5. Какие подводные камни у запуска в контейнере?
```


---

# U10. Senior и собеседования

<a id="u10-1"></a>

## U10.1 Стратегия UI-автоматизации и гибридные тесты

*Теория: `practice/u10_01_strategy_hybrid.md`*

Задания: `tests/ui/test_u10_01_strategy_hybrid.py`.

План: пирамида и «трофей» тестов; сколько стоит UI-тест; что автоматизировать в UI, а что в API и ниже;
как выбрать сценарии для UI на нашей бирже; гибридные тесты API → UI → БД; как говорить о стратегии на собесе.

Модуль U10: U10.1 стратегия и гибридные тесты → U10.2 ревью UI-тестов и Selenium для собеса →
U10.3 итоговый собес и лайвкодинг.

---

#### 1. Пирамида и трофей

**Пирамида** (Майк Кон): внизу много быстрых unit-тестов, в середине — интеграционные / API, наверху — немного UI (E2E).
Чем выше, тем дороже, медленнее и хрупче тест.

**Трофей** (Кент Доддс, для фронтенда): основа — статический анализ (типы, линтеры), самый толстый слой — **интеграционные**
тесты, E2E — немного сверху. Суть та же: **большая часть проверок — ниже UI**.

```
        /\         E2E / UI       — десятки-сотни: ключевые пути пользователя
       /  \
      /----\       API / интеграция — сотни-тысячи: логика, контракты, ошибки
     /      \
    /--------\     unit           — тысячи: функции, расчёты
```

Антипаттерн — **«мороженое»**: много ручных и UI-тестов, мало API и unit. Медленно, флейки, дорого поддерживать.

#### 2. Сколько стоит UI-тест

| Статья | UI-тест | API-тест |
|---|---|---|
| время прогона | секунды–минуты | миллисекунды |
| стабильность | ожидания, вёрстка, браузер (U2) | почти детерминирован |
| поддержка | меняется UI → правим PO (U4) | меняется контракт |
| локализация падения | «что-то сломалось по пути» | точное место |
| что проверяет | **то, что видит пользователь**, связку целиком | логику и контракт |

UI-тест оправдан, когда проверяет **то, что нельзя проверить ниже**: что пользователь может пройти путь, что фронт
правильно показывает данные и ошибки, что связка фронт–бэк работает.

#### 3. Что в UI, а что в API — на нашей бирже

| Проверка | Уровень | Почему |
|---|---|---|
| регистрация, вход, выход | UI (несколько тестов) + API (все негативы) | путь пользователя; валидации email и пароля — API |
| пополнение: суммы 0, -5, abc, 19 знаков | **API** (parametrize) | логика валидации бэкенда; в UI — один-два кейса «ошибка показана» |
| форма ордера: ошибки по полям видны | UI | отображение ошибок — фронт |
| матчинг: цена сделки, частичное исполнение | **API** | бизнес-логика, много комбинаций |
| «ордер исполнился» — статус в таблице обновился сам | UI (1–2 теста) | опрос и перерисовка — фронт |
| двойная трата, гонки | **API** (конкурентные запросы) | через UI не воспроизвести надёжно |
| отмена ордера кнопкой в строке | UI | действие пользователя |
| сортировка, фильтры таблицы | UI | клиентская логика |
| что UI при 500 / обрыве сети | UI + моки (U6.1) | реакция фронта |
| вёрстка ключевых экранов | визуальные (U8.1) | |
| доступность | axe + клавиатура (U8.2) | |

Принцип: **комбинаторика — вниз**, **путь пользователя и отображение — в UI**.

#### 4. Как выбрать сценарии для UI

- **критичные пути** (деньги, вход, основная ценность): «пополнить → выставить → исполниться → увидеть баланс»;
- **риск × частота**: где ломалось, что чаще используют;
- то, что **нельзя проверить ниже** (отображение, клиентская логика, интеграция фронта);
- **не дублировать** API-тесты: если валидация суммы покрыта на API, в UI — один тест «ошибка отображается»;
- каждый UI-тест — **одна цель**, подготовка — через API (U5).

Для ответа на собесе: «Сначала определяю критичные пользовательские пути и риски, покрываю их небольшим числом
стабильных E2E; всю комбинаторику и негативы — на API; UI-тесты быстрые за счёт подготовки через API».

#### 5. Гибридные тесты: API → UI → БД

Гибридный тест проверяет **одну операцию на трёх уровнях**: подготовка через API, действие через UI, проверка того,
что видит пользователь, и того, что **сохранилось** (API или напрямую БД).

```python
def test_cancel_order_hybrid(trader_factory, login_in_browser, db):
    trader = trader_factory(balance={"USDT": "1000"}, orders=[OrderData(price="100", quantity="2")])  # 1. API
    order_id = trader.orders[0]["id"]

    dashboard = login_in_browser(trader)                                                          # 2. UI
    dashboard.orders.row(order_id).cancel()
    expect(dashboard.orders.row(order_id).status).to_have_text("CANCELED")
    expect(dashboard.balances.locked("USDT")).to_have_text("0")

    assert trader.api.orders()[0]["status"] == "CANCELED"                                         # 3. API

    row = db.execute("SELECT status FROM orders WHERE id = %s", (order_id,)).fetchone()          # 4. БД
    assert row[0] == "CANCELED"
    bal = db.execute(
        "SELECT available, locked FROM balances b JOIN users u ON u.id = b.user_id "
        "WHERE u.email = %s AND b.asset = 'USDT'", (trader.email,)
    ).fetchone()
    assert bal == (Decimal("1000"), Decimal("0"))
```

Колонки у стенда: `orders(id, user_id, symbol, side, type, price, quantity, filled_quantity, status, created_at, updated_at)`,
`balances(user_id, asset, available, locked)` — `numeric(36,18)`, psycopg вернёт `Decimal` (модуль F3).

Когда БД-проверка уместна:
- **побочные эффекты**, которых нет в API: записи аудита, флаги, счётчики;
- **инварианты**: сумма `available + locked` не изменилась; нет «висящих» блокировок;
- **расследование**: API и UI говорят разное — кто врёт.

Когда нет: если API отдаёт то же самое — проверка через API надёжнее (тест не завязан на схему БД, которую могут
поменять). Доступ к БД — только на тестовых окружениях (U5.2), только чтение в проверках.

Фикстура `db` — session-соединение psycopg с `autocommit=True`, DSN из Settings (U4.3, U5.2).

---

#### Собес: вопросы и ответы

**1. Как решаешь, что автоматизировать в UI, а что в API?**
> Комбинаторику, негативы и бизнес-логику — на API: быстрее, стабильнее, точнее локализация. В UI — критичные
> пользовательские пути, отображение данных и ошибок, клиентская логика и интеграция фронта с бэком. Не дублирую:
> если валидация покрыта на API, в UI один тест, что ошибка показана. Подготовка UI-тестов — через API.

**2. Что такое пирамида тестов? Есть ли альтернативы?**
> Много дешёвых unit-тестов внизу, меньше интеграционных и API, немного UI сверху — чем выше, тем дороже и хрупче.
> Трофей для фронтенда смещает вес в интеграционные тесты и добавляет статический анализ снизу. Антипаттерн —
> «мороженое»: много UI и ручных тестов. Суть одна — большинство проверок ниже UI.

**3. Сколько должно быть UI-тестов?**
> Столько, сколько критичных пользовательских путей и рисков, которые нельзя проверить ниже, — обычно десятки–сотни,
> а не тысячи. Ориентир — время прогона на PR в пределах 10–15 минут и стабильность; если UI-набор растёт быстрее API,
> это сигнал пересмотреть уровни.

**4. Что такое гибридный тест и зачем проверять БД?**
> Подготовка через API, действие и проверка отображения через UI, проверка сохранённого через API или БД. БД — для
> побочных эффектов, которых нет в API, инвариантов вроде «деньги не исчезли» и расследований, когда уровни расходятся.
> Если то же отдаёт API — проверяю через API, чтобы не завязываться на схему.

### Задания — `tests/ui/test_u10_01_strategy_hybrid.py`

```text
U10. Урок 1 — стратегия UI-автоматизации и гибридные тесты.

Теория: practice/u10_01_strategy_hybrid.md
Запуск:
    uv run pytest tests/ui/test_u10_01_strategy_hybrid.py -v

Задача 1. Ревизия своего набора (письменно в «Ответах»).
    Пройди свои тесты U1–U9: какие из них на самом деле проверяют бэкенд-логику и должны жить на API?
    Минимум 5 примеров: тест → куда перенести → что оставить в UI.

Задача 2. Карта покрытия биржи.
    Таблица: функция × уровень (unit / API / UI / визуал / a11y) × приоритет (риск × частота).
    Минимум 12 строк. Отметь 8 UI-сценариев, которые ты бы оставил в smoke на каждый PR.

Задача 3. Фикстура db.
    ui_framework/fixtures/db.py: session-соединение psycopg (autocommit), DSN из Settings, только для окружений,
    где разрешено (флаг из U5.2). На stage — pytest.skip с понятной причиной.

Задача 4. Гибридный тест отмены.
    По образцу из теории: API → UI (отмена) → API → БД. Проверь в БД: статус, available + locked == 1000,
    updated_at > created_at.

Задача 5. Гибридный тест сделки.
    Продавец и покупатель через фабрики (U5.2), сделка через UI покупателя (BUY в форме), статусы в UI обоих,
    в БД — у обоих ордеров filled_quantity == quantity, балансы обоих (Decimal). Инвариант: суммарный USDT
    продавца и покупателя до и после сделки одинаковый, ETH — тоже.

Задача 6. Расхождение уровней.
    Мок GET /orders (U6.1): UI показывает FILLED, а в API и БД ордер NEW. Тест должен это поймать:
    сравни статус в UI со статусом в API. Зачем такой тест в реальности? (Кэш, CDN, баг фронта.)

Задача 7. Устно, 3 минуты.
    «Вы пришли в проект, где 800 UI-тестов, 50 API-тестов, прогон 2 часа, 15% флейков. Что будете делать
    первые 3 месяца?» Запиши тезисы в «Ответы» и расскажи вслух.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как решаешь, что автоматизировать в UI, а что в API?
    2. Что такое пирамида тестов? Есть ли альтернативы?
    3. Сколько должно быть UI-тестов?
    4. Что такое гибридный тест и зачем проверять БД?
```

<a id="u10-2"></a>

## U10.2 Ревью UI-тестов и Selenium на уровне собеседования

*Теория: `practice/u10_02_review_selenium.md`*

Задания: `tests/ui/test_u10_02_review_selenium.py`, ревью — `practice/u10_02_review_me.py`.

План: как проводить ревью UI-тестов — порядок, чек-лист, как писать замечания; сводный каталог антипаттернов
курса; Selenium — WebDriver, ожидания, PageFactory, stale element, Grid; сравнение с Playwright так, как спрашивают
на собесе.

---

#### 1. Ревью UI-тестов: порядок

1. **Что проверяет тест** — по имени и проверкам понятно, какое поведение? Одна цель?
2. **Уровень** — это точно UI, а не API (U10.1)?
3. **Данные и изоляция** — своё, уникальное, через API, уборка (U5).
4. **Ожидания** — всё через `expect`, нет sleep и «в моменте» (U2.1).
5. **Локаторы** — по ролям, без XPath, без позиций, однозначные (U1.2, U2.2).
6. **Структура** — PO и компоненты, нет DOM в тесте, нет проверок в PO (U4).
7. **Стабильность** — прогнан `--count`, в параллели, под замедлением (U2.4, U5.3).
8. **Читаемость** — Allure-шаги, понятные сообщения, нет мёртвого кода и `pause()`.

##### Как писать замечания

- `файл:строка` + **что не так** + **чем грозит** + **как исправить** (CLAUDE.md, ревью в чате);
- разделяй: **блокер** (флейк, неверная проверка, утечка секрета) / **важно** (структура, читаемость) / **мелочь** (стиль);
- ссылайся на правило, а не на вкус: «U2.1: `text_content()` читает в моменте — флейк в CI»;
- хвали удачные решения — ревью учит, а не только находит ошибки.

#### 2. Каталог антипаттернов курса

| Антипаттерн | Чем грозит | Где разбирали |
|---|---|---|
| `time.sleep`, `wait_for_timeout`, `networkidle` | медленно и флейк | U2.1 |
| `assert loc.is_visible()` / `count()` / `text_content()` | проверка в моменте — флейк | U2.1 |
| проверка отсутствия до загрузки | ложно-зелёный тест | U2.1 |
| проверка по тосту вместо результата | гонка, потерянный ввод | U2.1, U2.2 |
| XPath, длинные CSS, `.nth()` / `.first` без причины | хрупкость, скрытые дубли | U1.2, U2.2 |
| `has_text` для точного значения | подстрока: 10 ↔ 100 | U2.2 |
| `all()` с действиями на меняющемся списке | индексы съезжают | U2.2 |
| `force=True` | скрывает реальное перекрытие | U1.4 |
| запись codegen без переписывания | зашитые данные, нет проверок | U2.3 |
| `page.pause()` / `breakpoint()` в коде | CI висит | U2.3, U7.2 |
| ретраи как лечение, повтор неидемпотентных действий | маскировка, задвоение данных | U2.4 |
| God object PO, проверки в PO, строки вместо Locator | хрупкость, нельзя переиспользовать | U4.1 |
| `self.page` внутри компонента | чужие элементы, strict | U4.2 |
| адреса и секреты в коде | нельзя сменить окружение, утечка | U4.3 |
| `utils` знает про page, зависимости «не в ту сторону» | циклы, свалка | U4.4 |
| подготовка через UI | медленно, хрупко | U5.1 |
| Faker для уникальных полей, фиксированные данные | коллизии | U5.2 |
| общий пользователь в меняющих тестах, seed без блокировки | гонки в параллели | U5.3 |
| мок не по контракту, glob без query | тест несуществующего бэкенда | U6.1 |
| `browser.new_context()` мимо фикстур | нет trace | U7.1 |
| визуальный тест без масок и в «чужом» окружении | флейк | U8.1 |
| зависимые тесты | порядок ломает набор | U2.4 |

#### 3. Selenium: что спрашивают

Даже если в проекте Playwright, на собесе спросят Selenium — это до сих пор самый распространённый инструмент.

##### WebDriver

Selenium управляет браузером через **W3C WebDriver** — HTTP-протокол: каждая команда (найти элемент, кликнуть) —
отдельный HTTP-запрос к драйверу (chromedriver, geckodriver), драйвер управляет браузером. Playwright — одно постоянное
соединение (WebSocket/pipe) и события, которые приходят сами (U1.3).

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()                 # Selenium Manager сам найдёт/скачает chromedriver
driver.get("http://localhost:8080/app/")
driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]').send_keys("u@test.com")
driver.find_element(By.CSS_SELECTOR, '[data-testid="register-button"]').click()
driver.quit()
```

Локаторы: `By.ID`, `By.CSS_SELECTOR`, `By.XPATH`, `By.NAME`, `By.LINK_TEXT`, `By.CLASS_NAME`, `By.TAG_NAME`.
Ролевых локаторов (`get_by_role`) **нет** — поэтому в Selenium-проектах много XPath.

##### Ожидания

| | Неявное (implicit) | Явное (explicit) |
|---|---|---|
| Как | `driver.implicitly_wait(10)` | `WebDriverWait(driver, 10).until(EC....)` |
| Что ждёт | **только появления** элемента в `find_element` | любое условие: видим, кликабелен, текст, URL |
| Область | глобально на драйвер | конкретное место |
| Проблема | не ждёт видимости/кликабельности; смешивание с явными даёт непредсказуемые таймауты | нужно писать везде |

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="dashboard"]')))
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="deposit-button"]'))).click()
wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '[data-testid="toast"]'), "пополнен"))
```

Правило собеса: **не смешивать** implicit и explicit; использовать explicit. В Playwright этого выбора нет —
автоожидание в каждом действии и web-first assertions (U1.4, U2.1).

`FluentWait` — explicit с частотой опроса и игнорируемыми исключениями (`WebDriverWait(..., poll_frequency=0.5,
ignored_exceptions=[...])` в Python).

##### StaleElementReferenceException

`find_element` возвращает **ссылку на DOM-узел**. Наш фронтенд раз в 2 с перерисовывает таблицы (U2.2) — старая
ссылка протухает: `StaleElementReferenceException`. Лечат повторным поиском, ожиданием, обёртками. В Playwright —
Locator ищет заново при каждом действии, этой проблемы нет (U2.2, раздел 5).

##### PageFactory

Java-Selenium: `@FindBy(id = "email") WebElement email;` + `PageFactory.initElements(driver, this)` — ленивые прокси
элементов в PO. В Python своего PageFactory нет; локаторы хранят кортежами `(By.CSS_SELECTOR, "...")` и ищут
в методах. В Playwright Locator уже ленивый — PageFactory не нужен (U4.1).

##### Selenium Grid

Сервер, который распределяет сессии по **нодам** с разными браузерами и ОС — параллель и кросс-браузерность
на нескольких машинах.

```python
driver = webdriver.Remote(command_executor="http://localhost:4444", options=webdriver.ChromeOptions())
```

Локально — Docker-образы `selenium/standalone-chrome` (одна нода) или hub + nodes в docker compose.
Облака: BrowserStack, Sauce Labs, LambdaTest. В Playwright аналог — шарды и xdist (U9), плюс облака с поддержкой
Playwright; отдельный Grid обычно не нужен.

На нашей macOS 12 локальный chromedriver с системным Chrome **зависал** (ReadTimeout при подготовке урока), поэтому
практику Selenium делаем через `selenium/standalone-chrome` в Docker (задание 6).

#### 4. Playwright vs Selenium — таблица для собеса

| | Selenium | Playwright |
|---|---|---|
| Протокол | W3C WebDriver (HTTP на каждую команду) | своё постоянное соединение + CDP/патченные движки |
| Ожидания | implicit / explicit вручную | автоожидание действий, web-first `expect` |
| Stale element | да | нет (Locator) |
| Локаторы | By.*, XPath частый | роли, текст, label, test-id, цепочки, фильтры |
| Изоляция | новый драйвер = новый браузер (секунды) | BrowserContext (миллисекунды) |
| Вкладки, iframe | `switch_to.window/frame` | объект Page, `frame_locator` |
| Сеть | нет (только через прокси / BiDi) | `route`, моки, HAR |
| Трассировка | скриншоты, логи | Trace Viewer |
| Браузеры | любые с драйвером, включая настоящий Safari | Chromium, Firefox, WebKit (свои сборки) |
| Языки | Java, Python, C#, JS, Ruby, Kotlin… | JS/TS, Python, Java, C# |
| Экосистема | огромная, Grid, облака, Appium для мобильных | моложе, растёт |
| Когда Selenium | легаси-проект, настоящий Safari, Appium, требования Grid | — |

---

#### Собес: вопросы и ответы

**1. Как проводишь ревью UI-тестов?**
> По порядку: что проверяет и на правильном ли уровне; данные и изоляция; ожидания; локаторы; структура PO;
> стабильность — прогнан ли многократно и в параллели; читаемость. Замечание — место, что не так, чем грозит, как
> исправить, с разделением на блокеры и мелочи.

**2. Чем implicit wait отличается от explicit?**
> Implicit — глобальное ожидание появления элемента при поиске, не ждёт видимости и кликабельности. Explicit —
> WebDriverWait с конкретным условием в конкретном месте. Их не смешивают — таймауты становятся непредсказуемыми;
> используют explicit. В Playwright ожидание встроено в каждое действие и проверку.

**3. Что такое StaleElementReferenceException и почему её нет в Playwright?**
> Selenium хранит ссылку на DOM-узел; если страница его перерисовала, ссылка протухает. Playwright-локатор —
> описание поиска, элемент ищется заново при каждом действии.

**4. Что такое Selenium Grid?**
> Сервер, распределяющий сессии по нодам с разными браузерами и ОС — для параллели и кросс-браузерности.
> Подключение через Remote WebDriver. Есть облачные Grid-сервисы.

**5. Почему Playwright, а не Selenium? Когда всё-таки Selenium?**
> Playwright быстрее за счёт постоянного соединения и дешёвых контекстов, стабильнее за счёт автоожиданий и
> web-first проверок, даёт перехват сети и Trace Viewer. Selenium — для легаси-проектов, настоящего Safari, мобильных
> через Appium и там, где уже есть Grid и экспертиза.

### Задания — `tests/ui/test_u10_02_review_selenium.py`

```text
U10. Урок 2 — ревью UI-тестов и Selenium на уровне собеседования.

Теория: practice/u10_02_review_selenium.md
Ревью: practice/u10_02_review_me.py
Запуск:
    uv run pytest tests/ui/test_u10_02_review_selenium.py -v

Задача 1. Финальное ревью — 30 минут.
    practice/u10_02_review_me.py: минимум 20 проблем, с уровнем (блокер / важно / мелочь) и ссылкой
    на урок, где это разбирали (каталог антипаттернов — раздел 2 теории).

Задача 2. Переписать.
    Тесты из review_me — здесь, на своём фреймворке (PO, компоненты, API-подготовка, фабрики, expect).
    Те же сценарии, но независимые, со своими данными, стабильные при -n 4 --count 3.

Задача 3. Ревью своего кода.
    Выбери 3 своих файла из U4–U9 и пройди по чек-листу из теории (раздел 1). Запиши замечания так, как
    оставил бы их в PR (файл:строка, что, чем грозит, как исправить). Исправь блокеры.

Задача 4. Гайдлайн команды (письменно, ui_framework/GUIDELINES.md).
    1–2 страницы: локаторы, ожидания, данные, PO, что нельзя, как писать тест, чек-лист PR.
    Это то, что ты принесёшь в новую команду (часть «Senior-навыков»).

Задача 5. Selenium на бумаге.
    Перепиши на Selenium (в «Ответах», без запуска) три теста: вход, пополнение с проверкой баланса,
    отмена ордера в строке таблицы. С WebDriverWait и expected_conditions, без implicit wait.
    Отметь места, где в Selenium пришлось бы бороться со StaleElementReferenceException (таблица перерисовывается
    раз в 2 с) и как.

Задача 6. Selenium в Docker (по желанию).
    docker run -d -p 4444:4444 --shm-size=2g --add-host=host.docker.internal:host-gateway selenium/standalone-chrome
    Тест через webdriver.Remote("http://localhost:4444"), base URL http://host.docker.internal:8080:
    регистрация и проверка email в шапке. Посмотри сессию на http://localhost:4444 (Grid UI).
    Локальный chromedriver на macOS 12 зависал при подготовке урока — поэтому через Docker.

Задача 7. Устно, по 2 минуты.
    «Чем Playwright лучше Selenium?» и «Когда вы бы выбрали Selenium?» — без подглядывания в таблицу.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как проводишь ревью UI-тестов?
    2. Чем implicit wait отличается от explicit?
    3. Что такое StaleElementReferenceException и почему её нет в Playwright?
    4. Что такое Selenium Grid?
    5. Почему Playwright, а не Selenium? Когда всё-таки Selenium?
```

### Файл для ревью — `practice/u10_02_review_me.py`

```python
"""U10.2, задача 1 — финальное ревью: тесты «коллеги» на Playwright.

Найди минимум 20 проблем по всему курсу. Для каждой: строка, что не так, чем грозит, как исправить,
уровень (блокер / важно / мелочь). Ответы — внизу файла.
Это только чтение: файл в practice/ и не собирается pytest'ом.
"""

import random
import time

import pytest
from playwright.sync_api import Page, expect

URL = "http://localhost:8080/app/"
EMAIL = "qa@test.com"
PASSWORD = "Secret123!"


class Dashboard:
    def __init__(self, page):
        self.page = page
        self.last_order = None

    def login(self):
        self.page.goto(URL)
        self.page.locator("//input[@type='email']").fill(EMAIL)
        self.page.locator("//input[@type='password']").fill(PASSWORD)
        self.page.locator("text=Войти").click()
        self.page.wait_for_load_state("networkidle")

    def deposit(self, amount):
        self.page.locator("#deposit-form input").nth(0).fill(str(amount))
        self.page.locator("#deposit-form button").click(force=True)
        expect(self.page.get_by_test_id("toast")).to_contain_text("пополнен")

    def buy(self, price, qty):
        self.page.fill('[data-testid="order-price"]', str(price))
        self.page.fill('[data-testid="order-quantity"]', str(qty))
        self.page.click('[data-testid="place-order-button"]')
        self.last_order = price
        time.sleep(2)

    def balance(self):
        return float(self.page.locator('[data-asset="USDT"] [data-testid="balance-available"]').inner_text())


@pytest.fixture(scope="session")
def dash(browser):
    page = browser.new_page()
    d = Dashboard(page)
    d.login()
    return d


def test_1_deposit(dash):
    dash.deposit(1000)
    assert dash.balance() == 1000


def test_2_buy(dash):
    dash.buy(100.1, 1)
    assert dash.balance() == 899.9


def test_3_cancel(dash):
    dash.page.get_by_text("Отменить").first.click()
    rows = dash.page.get_by_test_id("order-row").all()
    assert "CANCELED" in rows[0].inner_text()
    assert dash.balance() == 1000


@pytest.mark.parametrize("amount", [random.randint(1, 100) for _ in range(3)])
def test_4_deposit_many(dash, amount):
    try:
        dash.deposit(amount)
    except Exception:
        pass
    assert dash.page.get_by_test_id("order-row").count() >= 0


def test_5_matching(dash, browser):
    seller = browser.new_page()
    seller.goto(URL)
    seller.pause()
    dash.buy(100, 1)
    time.sleep(10)
    assert "FILLED" in dash.page.content()


# Ответы
"""
"""
```

<a id="u10-3"></a>

## U10.3 Итоговый собес по UI-части и лайвкодинг

*Теория: `practice/u10_03_final_interview.md`*

Задания: `tests/ui/test_u10_03_final_livecoding.py`.

План: как устроено собеседование на Senior AQA и что проверяют на каждом этапе; карта всех вопросов курса
по модулям; 25 главных вопросов с короткими ответами — то, что должно отскакивать от зубов; рассказ о себе
и о фреймворке; лайвкодинг — как себя вести и задачи на время; вопросы работодателю.

---

#### 1. Этапы собеседования

| Этап | Что проверяют | Как готовиться |
|---|---|---|
| скрининг (HR / тимлид) | опыт, стек, мотивация, английский | рассказ о себе на 2 минуты (раздел 4) |
| технический | теория: Playwright, pytest, локаторы, ожидания, архитектура, CI | банк вопросов (разделы 2–3), вслух |
| лайвкодинг | написать тест / PO за 20–40 минут, говорить вслух | раздел 5, тренажёр `livecoding/` |
| ревью кода | найти проблемы в чужом тесте | U1.5, U4.1, U5.4, U10.2 |
| дизайн | «спроектируй фреймворк / стратегию для продукта» | U4.5, U5.4, U10.1 |
| поведенческий | конфликты, провалы, влияние | истории по STAR (модуль 10 части API) |

#### 2. Карта вопросов курса

Ответы — в разделах «Собес» уроков:

| Модуль | Уроки | Тема |
|---|---|---|
| U1 | U1.1–U1.5 | основы, локаторы, архитектура Playwright, context, pytest |
| U2 | U2.1–U2.4 | ожидания, strict mode, codegen, флейки |
| U3 | U3.1–U3.4 | вкладки, iframe, диалоги, файлы, мышь, Shadow DOM, таблицы, хранилища |
| U4 | U4.1–U4.5 | Page Object, компоненты, фикстуры, конфиг, утилиты, Allure, Screenplay |
| U5 | U5.1–U5.4 | API в Playwright, данные, storage_state, параллель |
| U6 | U6.1–U6.3 | моки сети, HAR, clock, окружение браузера |
| U7 | U7.1–U7.2 | trace, артефакты, отладка, CI vs локально |
| U8 | U8.1–U8.2 | визуал, доступность, производительность |
| U9 | U9.1–U9.2 | шарды, браузеры, Docker, CI, стабильность |
| U10 | U10.1–U10.3 | стратегия, гибридные тесты, ревью, Selenium |

#### 3. 25 главных вопросов

Короткий ответ — 3–4 предложения. Развёрнутый — в указанном уроке.

1. **Чем Playwright отличается от Selenium?** Постоянное соединение вместо HTTP на команду, автоожидания и web-first
   проверки, дешёвые контексты, перехват сети, trace; Selenium — шире экосистема и настоящий Safari. (U1.3, U10.2)
2. **Как Playwright ждёт перед кликом?** Attached, visible, stable, receives events, enabled — до таймаута действия. (U1.4)
3. **Почему `expect`, а не `assert`?** Повторяет проверку до таймаута, локатор ищется заново; `assert` — в моменте. (U2.1)
4. **Какие локаторы выбираешь?** Роль с именем → label/placeholder/текст → test-id → CSS; без XPath и позиций. (U1.2)
5. **Что такое strict mode?** Одна операция — один элемент, иначе ошибка; разрешаю уточнением, областью, фильтром. (U2.2)
6. **Что такое BrowserContext?** Изолированный профиль; новый на тест — изоляция за миллисекунды. (U1.4)
7. **Как в тесте два пользователя?** Два context. (U1.4, U5.3)
8. **Почему тест флейкает и как найти причину?** Не ждёт результата, общие данные, порядок, окружение; воспроизвожу,
   смотрю trace, чиню причину. (U2.4)
9. **Почему sleep — антипаттерн?** Одновременно слишком длинный и слишком короткий, не проверяет условие. (U2.1)
10. **Как устроен твой Page Object?** Класс на экран из компонентов; «как» в PO, «что» в тесте; Locator для проверок;
    переходы возвращают PO. (U4.1–U4.2)
11. **Можно ли проверки в PO?** Бизнес-проверки — нет; синхронизация и проверка своего действия — да. (U4.1)
12. **Какие scope у фикстур и как cleanup?** function/class/module/session; после `yield`, в обратном порядке. (U4.3)
13. **Как запускать на разных окружениях?** pydantic-settings, `ENV`, env-файлы, `base_url` из конфига, секреты из окружения. (U4.3)
14. **Как устроен твой фреймворк целиком?** Слои снизу вверх, стабильность, окружения, отчётность. (U4.5)
15. **Как не логиниться в каждом тесте?** API-логин и storage_state; дорогой логин — один раз с блокировкой; срок токена. (U5.1, U5.3)
16. **Как готовите и чистите данные?** Каждый тест создаёт своё через API, уникальность из uuid с префиксом,
    уборка в teardown и по префиксу. (U5.2)
17. **Что делать на общем стенде с чужими данными?** Не полагаться на пустоту, свои сущности по id, непересекающиеся
    данные, изоляция окружения. (U5.2)
18. **Как замокать бэкенд и зачем?** `page.route` — ошибки, трудные состояния, «во время запроса»; мок по контракту. (U6.1)
19. **Как проверить, что фронт отправил правильный запрос?** `expect_request` вокруг действия; сохранённое — через API. (U2.1, U6.3)
20. **Как тестировать iframe, вкладку, загрузку, скачивание?** frame_locator; expect_page/expect_popup; set_input_files;
    expect_download + save_as. (U3)
21. **Тест упал в CI, локально проходит — твои действия?** Артефакты, различия, воспроизведение (Docker, замедление,
    повторы), починка причины. (U7.2)
22. **Как запускаете в CI и параллелите?** Стенд в compose, шарды × xdist, артефакты всегда, ночью полный и
    кросс-браузерный. (U9)
23. **Что делаете с флейками?** Ретрай только как сигнал, задача на каждый, карантин, метрики. (U2.4, U9.2)
24. **Что автоматизировать в UI, а что в API?** Комбинаторику вниз, пути пользователя и отображение — в UI. (U10.1)
25. **Когда визуальные тесты оправданы и почему флейкают?** Дизайн-система и ключевые экраны; платформа, динамика,
    анимации — маски, моки, одно окружение. (U8.1)

#### 4. Рассказ о себе и о фреймворке

**О себе (2 минуты)**: кто ты сейчас → опыт и домены → что умеешь в автоматизации (UI на Playwright, API, CI, данные) →
чем гордишься (одна история с цифрой: «сократил прогон с 50 до 12 минут», «нашёл гонку двойной траты») → чего ищешь.

**О фреймворке (2–3 минуты)** — план из U4.5, вопрос 3: стек → слои → стабильность → окружения → отчёт → одно решение,
которым гордишься, и одно, которое переделал бы. Твой фреймворк — `ui_framework/` этого курса: стенд-биржа, PO
и компоненты, API-подготовка, фабрики, storage_state, моки, визуал, a11y, CI.

#### 5. Лайвкодинг

##### Как себя вести

1. **Уточни требования** (1–2 минуты): что проверяем, какие данные, что считается готовым.
2. **Проговори план** вслух: шаги, локаторы, проверки.
3. Начни с **позитивного** сценария, потом негативы.
4. Пиши **сразу правильно**: роли, `expect`, без sleep — интервьюер смотрит на привычки.
5. Запусти. Упало — **читай ошибку вслух**, не паникуй: «strict mode — уточню локатор».
6. Не успеваешь — скажи, что сделал бы дальше: вынес бы в PO, добавил бы parametrize, подготовку через API.
7. В конце — что улучшить: данные, изоляция, параллель.

##### Типовые задачи (из программы)

- **логин**: позитив, parametrize негативов, ошибка видна, кабинет скрыт;
- **форма с валидацией**: parametrize по полям, ошибка у нужного поля, ничего не создано;
- **таблица**: создать, найти строку по содержимому, действие в строке, фильтр, сортировка;
- **модалка**: открыть, проверить состояние кнопок, подтвердить/отменить, фокус, Escape.

Все четыре — в задании на время (на кабинете и лаборатории).

#### 6. Вопросы работодателю

- Как устроена автоматизация сейчас: сколько UI и API тестов, сколько идёт прогон, сколько флейков?
- Кто пишет тесты — только QA или и разработчики? Есть ли ревью тестов?
- Какие окружения: эфемерные на PR или общий stage?
- Что считается успехом через 3 и 6 месяцев на этой позиции?
- Как принимается решение «релизим / не релизим» и какую роль играют тесты?

### Задания — `tests/ui/test_u10_03_final_livecoding.py`

```text
U10. Урок 3 — итоговый собес по UI-части и лайвкодинг на время.

Теория: practice/u10_03_final_interview.md
Страницы: кабинет /app/ и лаборатория /app/lab.html (стенд: docker compose up -d --build).
Запуск:
    uv run pytest tests/ui/test_u10_03_final_livecoding.py -v

Правила как на собесе: засекай время; говори вслух; фреймворк использовать можно (это «ваш проект»);
не подглядывай в свои решения прошлых уроков, пока не закончишь задачу.

Задача 1. Логин — 10 минут.
    Позитив: зарегистрированный (через API) пользователь входит через UI → кабинет, email в шапке.
    parametrize негативов: неверный пароль, несуществующий email, пустые поля, email без @ —
    ошибка видна (текст — посмотри сначала, что отдаёт стенд), кабинет скрыт.

Задача 2. Форма с валидацией — 15 минут.
    Форма ордера, parametrize ≥ 6 кейсов: пустая цена, отрицательная, "abc", ноль в количестве,
    19 знаков после запятой, недостаточно средств. Для каждого: ошибка содержит имя поля (или текст про средства),
    ордер не создан (дождись загрузки таблицы!), баланс не заблокирован. Данные кейсов — в JSON (U5.2).

Задача 3. Таблица — 15 минут.
    Через API: 4 ордера с разными ценами. В UI: отмени второй по цене (найди строку по цене через колонку,
    не через nth). Фильтр NEW — 3 строки, колонка «Цена» в правильном порядке (новые сверху);
    фильтр CANCELED — 1 строка. Котировки в лаборатории: сортировка по изменению ↓ — проверь весь столбец.

Задача 4. Модалка — 15 минут.
    Лаборатория, «Вывод средств»:
        пустая сумма → «Введите сумму больше 0», модалки нет;
        сумма 150 → модалка «Подтвердите вывод» (role=dialog), текст с суммой, фокус на чекбоксе,
        «Подтвердить» disabled до чекбокса; кнопка «Вывести» под модалкой не кликается (почему? — U1.4);
        чекбокс → «Подтвердить» → модалка закрыта, «Заявка на вывод 150 USDT создана», фокус вернулся на «Вывести»;
        отмена тремя способами (кнопка, Escape, клик по фону) — parametrize, результат «Вывод отменён».
    Сначала сделай компонент ConfirmModal (U4.2, раздел 7 — теперь модалка есть на стенде).

Задача 5. Ревью на время — 10 минут.
    Открой practice/u5_04_review_me.py или practice/u10_02_review_me.py (тот, что делал раньше), закрой свои ответы
    и найди за 10 минут как можно больше проблем. Сравни с прошлым результатом.

Задача 6. Дизайн — 10 минут, устно.
    «Спроектируйте UI-автоматизацию для криптобиржи с нуля: стек, структура, данные, окружения, CI, что в UI,
    что в API, метрики». Тезисы — в «Ответы», рассказ — вслух.

Задача 7. Устный собес — 30 минут.
    25 главных вопросов из теории (раздел 3) — вслух, без подглядывания, 40–90 с на каждый.
    Плюс «расскажи о себе» и «расскажи о фреймворке». Номера, где «поплыл», — в «Ответы»; их повторить по урокам.

Задача 8. Итог.
    Отметь в трекере курса (ссылка в CLAUDE.md) пройденные модули UI. Обнови ui_framework/README.md:
    что умеет фреймворк, как запустить, ограничения, что бы сделал дальше.
```

