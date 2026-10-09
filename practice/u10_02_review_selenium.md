# U10. Урок 2 — ревью UI-тестов и Selenium на уровне собеседования

Задания: `tests/ui/test_u10_02_review_selenium.py`, ревью — `practice/u10_02_review_me.py`.

План: как проводить ревью UI-тестов — порядок, чек-лист, как писать замечания; сводный каталог антипаттернов
курса; Selenium — WebDriver, ожидания, PageFactory, stale element, Grid; сравнение с Playwright так, как спрашивают
на собесе.

---

## 1. Ревью UI-тестов: порядок

1. **Что проверяет тест** — по имени и проверкам понятно, какое поведение? Одна цель?
2. **Уровень** — это точно UI, а не API (U10.1)?
3. **Данные и изоляция** — своё, уникальное, через API, уборка (U5).
4. **Ожидания** — всё через `expect`, нет sleep и «в моменте» (U2.1).
5. **Локаторы** — по ролям, без XPath, без позиций, однозначные (U1.2, U2.2).
6. **Структура** — PO и компоненты, нет DOM в тесте, нет проверок в PO (U4).
7. **Стабильность** — прогнан `--count`, в параллели, под замедлением (U2.4, U5.3).
8. **Читаемость** — Allure-шаги, понятные сообщения, нет мёртвого кода и `pause()`.

### Как писать замечания

- `файл:строка` + **что не так** + **чем грозит** + **как исправить** (CLAUDE.md, ревью в чате);
- разделяй: **блокер** (флейк, неверная проверка, утечка секрета) / **важно** (структура, читаемость) / **мелочь** (стиль);
- ссылайся на правило, а не на вкус: «U2.1: `text_content()` читает в моменте — флейк в CI»;
- хвали удачные решения — ревью учит, а не только находит ошибки.

## 2. Каталог антипаттернов курса

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

## 3. Selenium: что спрашивают

Даже если в проекте Playwright, на собесе спросят Selenium — это до сих пор самый распространённый инструмент.

### WebDriver

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

### Ожидания

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

### StaleElementReferenceException

`find_element` возвращает **ссылку на DOM-узел**. Наш фронтенд раз в 2 с перерисовывает таблицы (U2.2) — старая
ссылка протухает: `StaleElementReferenceException`. Лечат повторным поиском, ожиданием, обёртками. В Playwright —
Locator ищет заново при каждом действии, этой проблемы нет (U2.2, раздел 5).

### PageFactory

Java-Selenium: `@FindBy(id = "email") WebElement email;` + `PageFactory.initElements(driver, this)` — ленивые прокси
элементов в PO. В Python своего PageFactory нет; локаторы хранят кортежами `(By.CSS_SELECTOR, "...")` и ищут
в методах. В Playwright Locator уже ленивый — PageFactory не нужен (U4.1).

### Selenium Grid

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

## 4. Playwright vs Selenium — таблица для собеса

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

## Собес: вопросы и ответы

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
