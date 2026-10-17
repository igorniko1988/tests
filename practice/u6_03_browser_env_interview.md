# U6. Урок 3 — окружение браузера и собес по модулю U6

Задания: `practice/tasks/test_u6_03_browser_env.py`, решение — `tests/ui/test_u6_03_browser_env.py` (создаёшь сам). Страница: **лаборатория** `http://localhost:8080/app/lab.html`
(блок «Окружение»; стенд пересобери: `docker compose up -d --build`).

План: какие настройки окружения есть у context; локаль и часовой пояс; геолокация и разрешения;
устройства и мобильная эмуляция; тема, сеть, прочее; как задать на весь прогон, на тест, на шаг;
шпаргалка и вопросы собеса по модулю U6.

---

## 1. Окружение — это настройки context

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

## 2. Локаль и часовой пояс

- `locale` влияет на `navigator.language`, `Intl.*` (числа, даты, валюты), заголовок `Accept-Language`;
- `timezone_id` — на `Date`, `Intl.DateTimeFormat` в странице. Идентификаторы IANA: `Europe/Moscow`, `UTC`, `America/New_York`.

Зачем: форматы денег и дат («1 234,56» vs «1,234.56»), границы суток («сделки за сегодня» в Токио и
Москве — разные), переводы интерфейса. Типичный баг — фронт форматирует дату в поясе браузера,
а должен в поясе биржи.

Часовой пояс context — это пояс **браузера**, а не сервера и не теста. Время сервера им не поменять
(как и `page.clock`, U6.2).

---

## 3. Геолокация и разрешения

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

## 4. Устройства и мобильная эмуляция

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

## 5. Прочее

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

## 6. Где задавать

| Область | Как |
|---|---|
| весь прогон | `browser_context_args` в conftest (U1.4), `--device` в командной строке |
| окружение (stage/local) | значения из Settings (U4.3) в `browser_context_args` |
| один тест | `@pytest.mark.browser_context_args(locale="en-US", timezone_id="UTC")` |
| несколько вариантов | `new_context(**options)` в тесте или параметризованная фикстура |
| на ходу | `set_geolocation`, `set_offline`, `grant_permissions`, `emulate_media` |

Параметризованная фикстура «локаль × часовой пояс» — один тест форматирования прогоняется на 4 окружениях.

---

## 7. Шпаргалка по модулю U6

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

## Собес: вопросы и ответы

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
