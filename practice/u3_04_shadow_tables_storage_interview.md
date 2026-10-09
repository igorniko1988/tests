# U3. Урок 4 — Shadow DOM, таблицы, cookies и localStorage; собес по модулю U3

Задания: `tests/ui/test_u3_04_shadow_tables_storage.py`. Страница: лаборатория `/app/lab.html`
(«Тикер (веб-компонент)», «Котировки», баннер cookies).

План: Shadow DOM — что это и как Playwright с ним работает (проверено); динамические таблицы —
сортировка и фильтр, как проверить правильно; cookies и localStorage — читать, подкладывать, чистить;
история про атрибут `hidden`; шпаргалка и вопросы собеса по модулю U3; лайвкодинг таблицы.

---

## 1. Shadow DOM

Веб-компонент `<price-ticker>` прячет свою разметку в **shadow root** — отдельное поддерево, изолированное
от стилей и селекторов страницы. Так устроены дизайн-системы (Lit, Stencil), Salesforce, многие виджеты.

### Playwright пробивает открытый shadow DOM сам

```python
page.get_by_test_id("ticker-price")                   # внутри shadow root — находится
page.get_by_role("button", name="Следить")            # тоже
page.locator("price-ticker button")                   # CSS — тоже
page.locator("xpath=//price-ticker//button")          # XPath — НЕТ
```

Проверено: роль, текст, test-id и CSS находят элементы внутри shadow root; XPath — 0 элементов.
XPath по стандарту не ходит в shadow DOM — ещё одна причина не использовать его (U1.2).

Selenium (до 4.x) требовал `shadow_root` руками — это частый вопрос «как работать с Shadow DOM».

### Закрытый shadow root

`attachShadow({mode: "closed"})` — снаружи недоступен ни JS страницы, ни Playwright. Тестируют через то,
что компонент отдаёт наружу (атрибуты, события, видимый результат) или просят разработчиков `mode: "open"`
в тестовой сборке. На практике закрытые встречаются редко.

### Разметка компонента: part и атрибуты

Компонент может отдавать части наружу (`part="price"`) и принимать данные атрибутами (`price="65000"`).
Проверка атрибута хоста: `expect(page.get_by_test_id("ticker")).to_have_attribute("symbol", "BTC-USDT")`.

---

## 2. Динамические таблицы: сортировка и фильтр

Таблица котировок: 20 строк, сортировка по клику на заголовок (повторный клик — обратный порядок),
поиск с debounce (U3.3), счётчик «Показано: N из 20», атрибут `aria-sort` на `th`.

### Как проверить сортировку

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

### Ожидание после клика

Сортировка на клиенте мгновенная, но **не всегда**: серверная сортировка — запрос и перерисовка. Чтение сразу после
клика — гонка (U2.1). Безопасно: дождаться признака (атрибут `aria-sort`, `expect_response`) или проверить первую
строку через `expect`, потом читать весь столбец.

### Фильтр

```python
search.fill("bt")
expect(rows).to_have_count(1)
expect(table.column("Тикер")).to_have_text(["BTC"])
expect(count).to_have_text("Показано: 1 из 20")
```

Фильтр + сортировка вместе: отсортировать, отфильтровать — порядок сохранился? Сбросить фильтр — сортировка осталась?

### Strict mode в таблицах лаборатории

`page.get_by_role("columnheader", name="Цена")` находит **два** заголовка: в котировках и в таблице импорта.
Сужай до таблицы: `quotes.get_by_role("columnheader", name="Цена")` (U2.2, U4.2).

---

## 3. Cookies и localStorage

### Cookies

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

### localStorage / sessionStorage

API у context нет — через страницу или storage_state:

```python
page.evaluate("localStorage.getItem('token')")
page.evaluate("([k, v]) => localStorage.setItem(k, v)", ["k", "v"])
page.evaluate("localStorage.clear()")
context.storage_state()["origins"]                       # [{'origin': 'http://localhost:8080', 'localStorage': [...]}]
```

Подложить **до** загрузки — `storage_state` в `new_context` (U5.1). sessionStorage в storage_state не сохраняется.

### Зачем в тестах

- пропустить баннеры и онбординг (cookie / флаг в localStorage);
- проверить, что приложение **сохраняет** настройки (тема, выбранная пара) — записалось и применилось после reload;
- проверить выход: токен удалён из хранилища (U1.4);
- фиче-флаги и A/B-группа, если их выбирает cookie.

---

## 4. История: `hidden` и CSS

При подготовке урока баннер cookies на лаборатории был виден **всегда**, хотя у него стоял атрибут `hidden`.
Причина: в CSS у `.banner` было `display: flex`, а правило автора страницы сильнее встроенного правила браузера
`[hidden] { display: none }`. Исправлено: `.banner[hidden] { display: none; }`.

Что из этого для тестировщика:
- `to_be_hidden()` / `to_be_visible()` проверяют **реальную видимость** (размер, `display`, `visibility`), а не атрибут —
  поэтому тест и поймал баг: «expected hidden, actual visible», хотя в логе видно `<div hidden="" ...>`;
- проверка атрибута (`to_have_attribute("hidden", "")`) этот баг **пропустила** бы — проверяй то, что видит пользователь.

---

## 5. Шпаргалка по модулю U3

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

## Собес: вопросы и ответы

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
