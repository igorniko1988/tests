# Собес GlobalLogic / AdTech: BDD (behave), e2e для API, микросервисы

**Смысл темы.** На проекте много микросервисов, внешние зависимости заменены моками, тесты — API e2e на
Python + behave. Нужно уметь объяснить: что такое BDD и Gherkin, как устроен behave (feature → steps →
context → environment.py), что такое e2e для API и зачем моки, как это запускается в CI на AWS и как
выглядит отчёт. Пример на нашем стенде пишешь сам по шагам в папке `bdd/` (разбор в чате).

**План на 2 часа:** разделы 1–4 (BDD и behave) → прогнать `bdd/` и прочитать шаги → раздел 6 (e2e и
моки) → раздел 10 (ответы, проговорить вслух по-английски).

---

### 1. BDD простыми словами

**BDD (Behavior-Driven Development)** — договориться о поведении системы на понятном всем языке, *до*
кода, и сделать эти договорённости автотестами.

```gherkin
Feature: Orders
  Scenario: Placing a BUY order locks its cost
    Given a registered user
    And the user has deposited 100 USDT
    When the user places a BUY order for 2 ETH at 10 USDT
    Then the response status is 201
    And the USDT balance is 80 available and 20 locked
```

- **Три амиго:** продакт (что нужно бизнесу), разработчик (как сделать), QA (как проверить) вместе пишут
  сценарии на встрече — так находят непонятные места требований до разработки.
- **Сценарий = живая документация.** Его читает продакт, а запускает CI. Если поведение поменялось —
  тест упадёт, документация не устареет.
- **Given / When / Then:** Given — исходное состояние (предусловия), When — одно действие пользователя или
  системы, Then — ожидаемый результат. And / But — продолжение предыдущего ключевого слова.
- **BDD ≠ инструмент.** behave, pytest-bdd, Cucumber — только способ запускать Gherkin. Главное в BDD —
  разговор и общие примеры.

---

### 2. Gherkin: все конструкции

```gherkin
@api @orders                                  # теги: фильтр запуска, хуки, отчёты
Feature: Orders                               # одна фича = один файл .feature
  As a trader                                 # свободное описание (user story)
  I want to place and cancel limit orders
  So that my money is locked only while the order is open

  Background:                                 # шаги перед КАЖДЫМ сценарием этого файла
    Given a registered user
    And the user has deposited 100 USDT

  @smoke
  Scenario: Cancelling an order returns the money
    Given the user has placed a BUY order for 1 ETH at 30 USDT
    When the user cancels the order
    Then the response status is 200

  Scenario Outline: Invalid orders are rejected        # шаблон: запускается на каждую строку Examples
    When the user places an order with <field> set to "<value>"
    Then the response status is <status>

    Examples:
      | field    | value   | status |
      | symbol   | XXX-YYY | 422    |
      | quantity | 0       | 422    |

  Scenario: Create a campaign
    When I create a campaign with:            # таблица данных → context.table
      | name     | budget |
      | Summer   | 1000   |
    And I send the body:                      # многострочный текст → context.text
      """
      {"name": "Summer", "budget": 1000}
      """
```

- **Background** — общие Given для всех сценариев файла (не путать с хуками: Background видно в отчёте).
- **Scenario Outline + Examples** — аналог `pytest.mark.parametrize`: каждая строка — отдельный сценарий.
- **Data table** (`| ... |` под шагом) — в шаге доступна как `context.table` (строки по заголовкам).
- **Doc string** (`"""`) — многострочный текст, например JSON тела запроса, в шаге — `context.text`.
- **Теги** — `@smoke`, `@regression`, `@wip`, `@skip`, `@jira-123`; запуск `--tags=smoke`,
  `--tags="smoke and not slow"`.

---

### 3. behave: как устроен проект

```text
bdd/
  behave.ini                     настройки: paths, default_tags, формат отчёта
  features/
    orders.feature               сценарии на Gherkin
    auth.feature
    environment.py               хуки: before_all, before_scenario, after_scenario …
    steps/
      common_steps.py            реализация шагов на Python
      order_steps.py
      auth_steps.py
```

```python
# features/steps/order_steps.py
from behave import given, then, when

@when("the user places a {side} order for {quantity} ETH at {price} USDT")
def step_place_order(context, side, quantity, price):
    context.response = context.api.orders.create(CreateOrder(side=side, quantity=quantity, price=price))

@then("the response status is {status:d}")
def step_status(context, status):
    assert context.response.status_code == status, context.response.text
```

- **Шаг** — функция с декоратором `@given / @when / @then` и шаблоном текста. behave ищет шаблон, который
  совпадает со строкой из `.feature`, и вызывает функцию.
- **Параметры в шаблоне** (парсер `parse` по умолчанию): `{side}` — строка, `{status:d}` — int,
  `{price:f}` — float. Можно `use_step_matcher("re")` для регулярных выражений.
- **Ключевое слово не важно для поиска:** шаг `@given("...")` найдётся и для строки `And ...` после Given.
  Шаг можно пометить двумя декораторами, если он нужен и как Given, и как When.
- **`context`** — общий «рюкзак» сценария: шаг When кладёт `context.response`, шаг Then берёт его. Атрибуты,
  добавленные в сценарии, удаляются после него; добавленные в `before_all` — живут весь прогон.
- **Шаги не должны знать про HTTP напрямую** — они вызывают фреймворк (клиент, сервисы, модели). В `bdd/`
  шаги вызывают наш `framework/api` — тот же, что у pytest-тестов.

---

### 4. environment.py — хуки (аналог фикстур)

```python
def before_all(context):            # один раз: настройки, клиенты, логирование
    context.settings = get_settings()

def before_feature(context, feature): ...
def before_scenario(context, scenario):   # перед каждым сценарием: свежий клиент
    context.api = Api(ApiClient(context.settings.base_url, context.settings.timeout))

def before_tag(context, tag):       # например @mock_ads → включить нужный мок
    ...

def after_scenario(context, scenario):    # уборка, выполнится и после упавшего сценария
    cancel_open_orders(context.api)
    context.api.client.close()

def after_step(context, step):      # при падении — приложить ответ / скриншот в отчёт
    if step.status == "failed": ...
```

- **Порядок:** before_all → before_feature → before_scenario → before_step/after_step → after_scenario →
  after_feature → after_all. Есть before_tag/after_tag.
- **Фикстуры behave** (`@fixture` + `use_fixture(fx, context)`) — генераторы с `yield` как в pytest; часто
  включаются по тегу `@fixture.browser.chrome`.
- **userdata:** `behave -D env=stage` → `context.config.userdata["env"]` — выбор окружения.

---

### 5. behave и pytest-bdd, плюсы и минусы BDD

- **behave** — отдельный раннер (не pytest): свои хуки, свой `context`, нет фикстур с областями видимости
  как в pytest, нет встроенного параллельного запуска (используют **behavex** или разбивку по тегам в CI).
- **pytest-bdd** — Gherkin поверх pytest: сценарии становятся pytest-тестами, работают фикстуры,
  `-n auto`, плагины pytest.
- **Когда BDD полезен:** бизнес-правила с примерами (биллинг, таргетинг рекламы, лимиты), когда сценарии
  читают не только инженеры.
- **Когда мешает:** технические проверки (схема JSON, коды ошибок пачкой), если сценарии никто, кроме QA,
  не читает — получается лишний слой.
- **Хорошие сценарии — декларативные:** «Given an active campaign with budget 1000» вместо «Given I send
  POST /campaigns with body ...». Детали — в шагах, бизнес-смысл — в Gherkin.
- **Анти-паттерны:** один гигантский сценарий на всё; шаги с логикой и ветвлениями; зависимость сценариев
  друг от друга; дубли шагов с разным текстом; `time.sleep` в шагах.

---

### 6. Что такое e2e для API и зачем моки

**e2e (end-to-end) для API** — проверка целого бизнес-процесса через публичные API, когда запрос проходит
через несколько сервисов, как у реального клиента. UI нет, но путь «от входа до результата» — весь.

```text
Пример AdTech:  POST /campaigns  →  campaign-service  ──событие──▶  ad-server
                                                                      │  GET /ad?user=…
                POST /impressions ◀──────────────── клиент (плеер) ◀──┘
                                       │ Kafka/SQS
                GET /reports/campaign/{id}  ◀── reporting-service  (impressions = 1)

Пример на нашем стенде:  POST /orders (BUY) + POST /orders (SELL)  →  matching в фоне
                         →  GET /orders/{id} status=FILLED, балансы обоих изменились, событие в Kafka
```

- **Пирамида для микросервисов:** unit (код сервиса) → **component** (один сервис целиком, его соседи
  заменены моками) → **contract** (Pact: договор потребителя и поставщика) → **integration** (несколько
  реальных сервисов) → **e2e** (весь процесс). Чем выше — тем медленнее и дороже, поэтому e2e мало и только
  ключевые потоки.
- **Моки (stubs)** — фейковые версии зависимостей: внешние партнёры (платёжка, DSP, гео-сервис), сервисы
  другой команды, всё, что нестабильно или платно. Инструменты: **WireMock** (HTTP), **LocalStack** (AWS:
  S3, SQS, SNS, Lambda), **moto** (AWS в Python), `responses`/`requests-mock` (в коде).
- **Что даёт мок:** детерминированные данные, негативные сценарии по заказу (500, таймаут, пустой ответ),
  независимость от чужих окружений. **Минус:** мок может разойтись с реальным сервисом → нужны
  контрактные тесты.
- **Пример с нашего стенда:** провайдер цен — WireMock (`localhost:8089`). Тест подменяет ответ через
  `/__admin/mappings`: «цена устарела» → стенд отвечает 503 `price_stale`. Toxiproxy добавляет задержку
  сети — проверка таймаутов.
- **Асинхронность:** между сервисами часто очереди (Kafka, SQS). В e2e нельзя `sleep(5)` — ждём условие
  с таймаутом (polling: `wait_until(lambda: report()["impressions"] == 1, timeout=30)`) или читаем событие
  из топика.
- **Корреляция:** один `X-Request-ID` / trace id проходит через все сервисы — по нему ищут, где сломалось
  (логи, CloudWatch, Jaeger/X-Ray).

---

### 7. AdTech: минимум словаря

- **Advertiser / campaign / line item / creative** — рекламодатель → кампания → строка размещения (бюджет,
  даты, таргетинг) → сам ролик/баннер.
- **Ad server** — решает, какую рекламу показать в этот момент этому зрителю. **Ad decisioning** — этот выбор.
- **Impression** — показ рекламы; **CPM** — цена за 1000 показов; **click / CTR** — клики и их доля.
- **Targeting** — кому показывать (гео, устройство, возраст, интересы); **frequency capping** — не больше N
  показов одному зрителю; **pacing** — равномерно расходовать бюджет по дням.
- **VAST** — XML-формат видеорекламы (плеер получает VAST и показывает ролик); **SSAI** — вставка рекламы в
  поток на сервере (стриминг).
- **DSP / SSP / RTB** — платформы покупателя и продавца, аукцион в реальном времени за показ.
- **Что тестировать:** правила выбора рекламы (таргетинг, капы), расчёт бюджета и отчётов (суммы — Decimal,
  часовые пояса), события показов через очереди, корректность VAST, отказоустойчивость при сбое партнёра.

---

### 8. AWS, CI/CD, отчёты — что сказать

- **AWS для QA:** тесты бегут в CI-агентах или контейнерах (ECS/EKS, CodeBuild); сервисы читают/пишут
  S3, SQS/SNS, DynamoDB, Lambda; логи — **CloudWatch**; трейсы — **X-Ray**. Из тестов — `boto3`: положить
  файл в S3, прочитать сообщение из SQS, найти лог по request id. Локально и в CI без AWS — **LocalStack**.
  Секреты — Secrets Manager / переменные CI, не в репозитории.
- **CI/CD:** на PR — линтер, unit, `behave --tags=smoke`; после merge — регрессия; ночью — полный прогон.
  Окружение — `-D env=stage` или переменные. Артефакты: отчёт, логи. (Наш пример — `.github/workflows/`
  в репозитории: pr, regression, nightly, manual.)
- **Отчёты:** `allure-behave` (`behave -f allure_behave.formatter:AllureFormatter -o allure-results`),
  JUnit (`behave --junit`) для CI, ReportPortal — для истории и анализа падений.
- **TA-метрики:** pass rate, flaky rate (тесты, которые то падают, то нет), время прогона, покрытие
  требований/эндпоинтов автотестами, число багов, найденных автотестами, MTTR красного билда.

---

### 9. Selenium и OOP — коротко

- **Selenium WebDriver:** явные ожидания `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))`,
  не `time.sleep`; локаторы — `By.CSS_SELECTOR`, `data-testid`; Page Object; Selenium Grid для параллели.
  Разница с Playwright: у Playwright авто-ожидания и свой протокол, у Selenium — стандарт W3C WebDriver.
- **В behave + Selenium:** драйвер создаётся в `before_scenario` (или фикстурой по тегу `@ui`), закрывается
  в `after_scenario`, скриншот при падении — в `after_step`.
- **OOP во фреймворке:** инкапсуляция (клиент прячет HTTP), наследование (`BaseClient` → `OrdersClient`,
  `BasePage` → `LoginPage`), полиморфизм (`headers()` у наследника), композиция (страница из компонентов).

---

### 10. Вопросы и ответы (проговорить вслух; по-английски — коротко)

- **What is BDD?** — *A collaboration approach: product, dev and QA agree on behavior using concrete examples
  in Gherkin before coding; the same scenarios become automated tests and living documentation.*
- **Given / When / Then?** — *Given sets up the state, When is the single action, Then checks the outcome.
  And/But continue the previous step type.*
- **Background vs hooks?** — *Background is visible business setup for every scenario in a feature; hooks in
  environment.py are technical setup and cleanup, invisible to business readers.*
- **Scenario Outline?** — *A template run once per row of Examples — data-driven testing, like pytest
  parametrize.*
- **How do steps share data?** — *Through the `context` object: a When step stores the response, a Then step
  reads it. Scenario-level attributes are cleared after each scenario.*
- **How do you structure a behave framework?** — *Feature files by business area, thin step definitions that
  call a framework layer — API clients per service, models, data builders — environment.py for setup and
  cleanup, tags for suites, config per environment, Allure reporting, CI runs smoke on PR and regression
  after merge.*
- **How to avoid step explosion / duplicates?** — *Declarative steps in business language, parameters
  instead of copies, shared common steps, reviewing new steps against the step catalog
  (`behave --steps-catalog`).*
- **Parallel run in behave?** — *Not built in; I'd use behavex or split by tags/features across CI jobs; tests
  must be independent — own test data per scenario and cleanup in after_scenario.*
- **What is e2e for APIs?** — *Testing a full business flow through public APIs across several services, e.g.
  create a campaign, request an ad, send an impression, check the report — no UI, but the whole chain.*
- **Why mocks in microservices?** — *To isolate the service or flow from unstable, paid or third-party
  dependencies, get deterministic data and simulate failures like 500s and timeouts. The risk is drift, so
  I add contract tests (Pact) and a few real integration checks.*
- **How do you test async flows (Kafka/SQS)?** — *Polling with a timeout instead of sleep, or consume the
  event from the topic/queue and assert its payload; correlate by request/trace id.*
- **A test is flaky. What do you do?** — *Reproduce, check logs by request id, look for shared data, timing
  (missing waits on async processing), environment instability; fix the cause, not add retries; quarantine
  with a tag and a ticket if it blocks the pipeline.*
- **How do you design a test strategy for a heavily integrated system?** — *Map services and dependencies,
  find critical business flows and risks, put most checks low in the pyramid (unit, component with mocks,
  contract), keep few e2e for key flows, define environments and test data, run by level in CI, report
  metrics.*
- **Why Python + behave and not pytest?** — *behave if business reads the scenarios; pytest(-bdd) if mostly
  engineers do. I can work with both: same framework layer underneath, only the runner differs.*

---

### 11. Рассказ о себе (шаблон, 1 минута)

*I'm an AQA engineer with [N] years in test automation on Python. I build frameworks for API and web UI: a
requests-based API layer with service clients and pydantic models, UI with Page Object on Playwright [and Selenium — if you used it], pytest fixtures for isolated test data, Allure reporting, and CI pipelines with smoke on pull
requests, regression after merge and nightly cross-browser runs. I've tested services with mocks —
WireMock for external providers, Toxiproxy for network failures — and async flows through Kafka and
webhooks. I've used BDD with behave: Gherkin scenarios over the same API framework, hooks in
environment.py for setup and cleanup, tags for smoke and regression.*

Подставь свои цифры и инструменты — говори только то, что делал. Про behave честно: опыт с behave — учебный проект поверх своего фреймворка (`bdd/`), его можно
показать и объяснить.
