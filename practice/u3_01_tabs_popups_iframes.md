# U3. Урок 1 — вкладки, всплывающие окна и iframe

Задания: `tests/ui/test_u3_01_tabs_popups_iframes.py`. Страница: **лаборатория** `/app/lab.html`
(блоки «Вкладки и окна», «Виджет курса»; стенд пересобери: `docker compose up -d --build`).

Модуль U3: U3.1 вкладки, окна, iframe → U3.2 диалоги и файлы → U3.3 мышь, клавиатура, скролл →
U3.4 Shadow DOM, таблицы, cookies и localStorage + собес и лайвкодинг.

---

## 1. Новая вкладка (`target="_blank"`)

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

## 2. Всплывающее окно (`window.open`)

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

### OAuth и платёжные окна

Типичный сценарий: «Войти через Google» открывает popup, после логина он закрывается, основная страница
залогинена. В тестах сторонний провайдер **не используют** (капчи, лимиты, 2FA): мокают (U6.1) или
логинят через API и storage_state (U5). Popup-механику проверяют на своём тестовом провайдере.

---

## 3. iframe

iframe — **отдельный документ** внутри страницы. Локаторы страницы внутрь iframe не видят:

```python
page.get_by_test_id("widget-price")               # 0 элементов — он внутри iframe
```

### frame_locator — основной способ

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

### Frame — объект документа

```python
page.frames                                       # главный + все iframe: ['lab.html', 'widget.html']
frame = page.frame(url=re.compile(r"widget\.html"))
frame.evaluate("document.title")
```

`Frame` нужен для `evaluate` внутри iframe, ожиданий навигации iframe. Для действий и проверок —
`frame_locator`.

### Вложенные и общение со страницей

```python
page.frame_locator("#outer").frame_locator("#inner").get_by_role("button")
```

Кнопка «Подписаться» в виджете отправляет `postMessage` родителю — основная страница показывает
«Подписка на ETH-USDT». Тест проверяет **результат** на стороне страницы:
`expect(page.get_by_test_id("widget-message")).to_have_text("Подписка на ETH-USDT")`.

### Другой домен

Cross-origin iframe (платёжная форма на домене провайдера) Playwright обрабатывает так же — `frame_locator`
работает, в отличие от JS в странице, которому браузер запретил бы доступ. Но **логику провайдера**
не тестируют — только интеграцию: форма встроена, результат вернулся.

---

## 4. Частые ошибки

| Ошибка | Как правильно |
|---|---|
| клик, потом `context.pages[-1]` | `expect_page` / `expect_popup` **вокруг** клика — иначе гонка |
| ищут элемент iframe локатором страницы | `frame_locator` / `content_frame` |
| `page.frames[1]` по индексу | по `url` или `name`, а лучше `frame_locator` по атрибуту iframe |
| «переключение» на вкладку, как в Selenium | у каждой вкладки свой `Page` |
| тестируют сторонний OAuth / платёжку вживую | мок или логин через API |
| забыли, что вкладка в том же context | новая вкладка видит тот же логин — это не изоляция |

---

## Собес: вопросы и ответы

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
