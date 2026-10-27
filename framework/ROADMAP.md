# API-фреймворк: дорожная карта и прогресс

Фреймворк пишет пользователь, Claude ставит задачи и ревьюит (см. `CLAUDE.md`).
Тесты — `api_tests/`, запуск `uv run pytest`, отчёт `uv run pytest --alluredir=allure-results` → `allure serve allure-results`.
Пункты курса — `PROGRAM.md` (модули 1–10 = этапы ниже); перед переходом к следующему этапу сверяться со списком модуля.

## Где остановились (2026-10-27)

**Этап 3: выданы 3.4 (БД) и 3.5 (testcontainers).** Дальше — пропуски модулей 1–2 (раздел ниже), затем модуль 4 (4.1 уже выдан).

Хвосты:
- 2.1: `Balance` без `strict`, `available`/`locked` — `Decimal`, `asset` — `Literal`; в `test_cancel_orders` сравнивать `Decimal`.
- 1.6: POST повторять только для `/orders` и `/auth/login` (второй `HTTPAdapter` через `mount` по префиксу) —
  в режиме сбоев `allowed_methods=None` дважды зачисляет депозит; уборка в `auth_api` пропускает, если `list()` не 200.
- 3.x: `framework/waiter.py` — `if condition:` без скобок и без умолчаний; `make_user` без списка `users` и уборки;
  нет `test_user_cannot_see_foreign_order` и `test_trade.py`; `test_order_by_id`/`test_cancel_orders` не на фабрике;
  в `funded_user` нет ETH; `print(ENV_FILE)` в settings.py.

## Этап 1. Каркас — ✅

- 1.1 `ApiClient` (сессия, таймаут, `set_token`) · 1.2 Settings и `envs/` · 1.3 сервисы Auth, Balance, Order
- 1.4 `list`/`get`/`cancel`, teardown через `yield` в `auth_api`, тесты в `api_tests/`, корневой `conftest.py`
- 1.5 `transport/reporting.py`: строка лога на запрос + шаги и вложения Allure, тела `/auth/*` не прикладываются
- 1.6 `Retry` на 503 через `HTTPAdapter`, `Idempotency-Key` на `POST /orders`

## Этап 2. Модели и контракты — почти ✅

- 2.1 точные типы в моделях ответов (UUID, Decimal, datetime, Literal), lax + `extra='forbid'` — `Balance` ещё нет
- 2.2 модели запросов с умолчаниями (`CreateOrder` на строках, `exclude` для пропуска поля) — ✅
- 2.3 негативные тесты контракта: 422 на каждое неверное поле через `parametrize` — 2 случая, хвост: больше полей и границы
- 2.4 сверка с OpenAPI: `framework/contract.py`, `assert_matches_schema(data, 'OrderOut')` — ✅; эталон можно хранить в `framework/openapi.json`
- Pact — объяснён, практика на этапе 8

## Этап 3. Данные и изоляция — идёт

- 3.1 `funded_user` + фабрика `create_order`, параллельный прогон `-n 4` — частично
- 3.2 фабрика `make_user` (уборка за всеми), тест чужого ордера: get/cancel → 404, нет в list — частично (токен исправлен)
- 3.3 `wait`/`wait_until` (polling), `api_tests/test_trade.py` сделка BUY/SELL по 500, `xdist_group('order_book')` + `--dist loadgroup` — выдан
- 3.4 БД: `DB_URL` в env, `framework/db.py` (psycopg, autocommit, dict_row), фикстура `db` session;
  `test_db_side_effects.py`: пароль хранится хешем, повтор с тем же Idempotency-Key → один ордер в `orders` — **выдан**
- 3.5 testcontainers: `framework/fixtures/containers.py` session-фикстура `container_stand` (Network + PostgresContainer alias db + образ стенда, HttpWaitStrategy /health), `TESTCONTAINERS_RYUK_DISABLED=true` (Ryuk не стартует на macOS 12), `testcontainers.community.postgres`, `driver=None`; `test_clean_stand.py` count users == 2; маркер `containers`, addopts `-m "not containers"` — **выдан** (проверено Claude: старт ~17 с)
- Уборка без цикла: можно добавить на стенд `DELETE /orders` (cancel-all) — по просьбе пользователя

## Этап 4. Бизнес-логика — выдан 4.1

- 4.1 блокировка денег: `api_tests/test_balance_lock.py` — BUY блокирует price×qty USDT, SELL — qty ETH (parametrize), граница «ровно хватает» 201 / «3.01» 400, после 400 баланс не изменился — выдан

## Пропущенные пункты модулей 1–2 (сверка с PROGRAM.md 2026-10-27)

- М1: маскирование секретов в логах/Allure (сейчас тела `/auth/*` просто не прикладываются; токен в заголовках не маскируется)
- М1: retry только для идемпотентных методов (= хвост 1.6)
- М1 сценарий: тот же набор на local / docker / stage без изменений кода (`ENV=stage`, :8081)
- М2: генерация клиента и моделей из OpenAPI (`datamodel-code-generator`)
- М2: Schemathesis — фаззинг по спецификации
- М2: Pact — по программе в модуле 2 (мы отложили до модуля 6, нужен второй сервис)
- М2 сценарий: ловим breaking change (поле стало nullable, поменялся enum)

## Модуль 4 — теория выдана целиком (инварианты, машина состояний, hypothesis stateful, гонки, идемпотентность, polling, Decimal, пагинация, время); практика — 4.1 выдан

## Модуль 5. Не-REST — идёт

- Теория целиком выдана 2026-10-27 (WebSocket, вебхуки, GraphQL, gRPC, Kafka/RabbitMQ)
- 5.1 WebSocket стакан: `framework/transport/ws_client.py` (websockets sync), фикстура `orderbook_ws`, snapshot → update, sequence+1, close 4004 — **выдан**;
  ручка влита: ветка `stand/ws-orderbook` (PR в main открыть на сайте) + cherry-pick в sandbox; 4004 теперь после accept.
  Пользователь сделал `api_tests/test_ws.py` (snapshot → update), фикстура через `with connect(...)`, WsClient не нужен
- 5.2 вебхуки: стенд `stand/webhooks` (POST /webhooks → secret, order.filled/order.canceled, X-Signature HMAC, повторы 1/2/4 с) —
  задание: `pytest-httpserver`, `WebhookService`, `framework/signature.py`, тесты подписи и повтора после 500, адрес `host.docker.internal` — **выдан**
- 5.3 GraphQL и gRPC — теория-обзор выдана (без практики, по программе обзор)
- 5.4 Kafka: стенд `stand/messaging` (Redpanda localhost:19092, `orders.events`, 3 партиции, ключ = id ордера);
  задание: `framework/kafka.py` subscribe (ждать assignment!) + collect, модель `OrderEvent`, тесты created и порядок created→partially_filled→canceled — **выдан**
- 5.5 RabbitMQ: очередь `deposits` (message_id, дубль не зачисляется, битое → `deposits.dlq`);
  задание: фикстура `rabbit` (pika), тесты зачисления, дубля, DLQ — **выдан**

## Модуль 6. Моки и отказоустойчивость — идёт

- 6.1 тесты фреймворка в `framework_tests/` (в testpaths): `responses` — URL, токен, таймаут, clear_token;
  `pytest-httpserver` — ретрай GET на 503 (3 запроса), POST депозит НЕ ретраится (сейчас падает 4 == 1 → чинить хвост 1.6);
  отчёт без пароля и токена (monkeypatch allure.attach) — **выдан**
- 6.2 WireMock: стенд `stand/price-feed` (MARKET без price → цена из `price-feed:8080/prices/{symbol}`, таймаут 2 с,
  старше 10 с → 503 `price_stale`, иначе `price_unavailable`; WireMock на :8089 с `--global-response-templating`).
  Задание: `framework/wiremock.py` (stub / count / reset), фикстура `price_feed` с reset в teardown, `xdist_group('price_feed')`;
  `test_market_order.py`: цена из фида и блокировка, parametrize отказов (500, задержка 5 с, обрыв, старая цена, битое тело) → 503
  + баланс не изменился + ордера нет, count == 1, 422 для MARKET+price и LIMIT без price, 2 своих «правдоподобных, но неправильных» ответа — **выдан**
- 6.3 Toxiproxy: стенд `stand/toxiproxy` (стенд → toxiproxy:8666 → price-feed:8080, API :8474, прокси `price_feed`).
  Задание: `framework/toxiproxy.py` (add_toxic / disable / reset), фикстура `network`, `test_price_feed_network.py`:
  latency 1500 → 201, latency 5000 → 503 < 3 с, прокси выключен → 503, reset_peer → 503, slicer (струйка) → 503 < 3 с;
  везде баланс не изменился — **выдан** (6.1 и 6.2 на диске ещё не начаты)
- 6.4 Pact (из модуля 2): `uv add --group tests pact-python` (4.x), папка `contract_tests/` в testpaths, файл в `contract_tests/pacts/`;
  consumer — `Pact('aqa-framework','exchange').with_specification('V4')`, взаимодействия «list own orders» (given open order)
  и «create limit order» (given 100 USDT), клиент — свой `Api(ApiClient(str(srv.url)))`; provider — `Verifier('exchange')`
  + `add_custom_header('Authorization', ...)` из `auth_api` + `state_handler({...}, teardown=True)`;
  ломаем контракт полем `fee` → «Actual map is missing the following keys: fee» — **выдан** (проверено Claude, 2 passed ~10 с)

## Модуль 7. Безопасность API — выдан

- Стенд `stand/security`: refresh-токены с ротацией, rate limit входа (5/60 с → 429), роли и `/admin/*`,
  `GET/PATCH /me` (профиль, `test_me_returns_current_user` упадёт — модель `User` не знает `role`/`display_name`),
  подписанный API `/v1/*` (X-API-KEY, HMAC query, timestamp, recvWindow), `/time`
- 7.1 BOLA/IDOR: чужой ордер get/cancel → 404 (сценарий модуля), parametrize по ручкам
- 7.2 BFLA + mass assignment: все `/admin/*` обычным пользователем → 403; `PATCH /me` с role/blocked/email не меняет их
- 7.3 JWT: `framework/tokens.py` (PyJWT, `JWT_SECRET` в dev.env): alg none, чужой секрет, истёкший → token_expired,
  refresh как access, refresh-ротация (старый → 401), rate limit 429 + Retry-After
- 7.4 HMAC: `framework/signed.py` (sign query), happy, неверная подпись, подмена параметра, старый timestamp,
  будущее > 1 с, replay после окна, recvWindow > 60000 отклоняется, сдвиг часов через `/time`
- Всё выдано 2026-10-27; ожидаются найденные баги — оформлять как баг-репорты

## Модуль 8. Производительность в функциональных тестах — выдан

- Замеры Claude (1 пользователь, p50/p95 мс): login 237/449, balances 6/7, orders 6/7, create order 177/425;
  Locust 20 users 20 с: p95 общий 1600 мс (login/register/deposit ~1 с) — SLO 500 мс не проходит, причину ищет пользователь
- 8.1 бюджеты: `framework/budgets.py`, мягкая проверка в `ApiClient._request` (warning + Allure), жёсткая — `test_performance.py`
  (прогрев, 20 запросов, p95 < бюджет, маркер `perf`)
- 8.2 `framework/stats.py` percentile (nearest-rank) + тесты в `framework_tests/`
- 8.3 `load/locustfile.py`: Trader (on_start регистрация+депозит, tasks 3/2/1, name для /orders/{id}),
  SLO в `events.quitting` (fail_ratio ≤ 1%, p95 ≤ 500) → exit code; `--headless -u 20 -r 5 -t 30s --csv --html`

## Модуль 9. CI/CD и надёжность прогонов — выдан

- Стенд `stand/tracing`: OpenTelemetry (FastAPI + asyncpg) → Jaeger :16686, входящий `traceparent`, ответ `X-Trace-ID`,
  `trace_id` в строке лога; фоновые SQL не шумят (sampler только от входящих запросов)
- 9.1 `.github/workflows/api.yml`: PR + push main + nightly + dispatch, concurrency, uv cache, compose up + ожидание /health,
  matrix shard `-n auto` или `pytest-split`, artifacts allure-results/junit, логи стенда при падении, `docker compose down -v`
- 9.2 защита main: required checks, 1 review, `.github/pull_request_template.md`, `CODEOWNERS`
- 9.3 `Jenkinsfile` (declarative: stages, parallel, post always/failure, archiveArtifacts, junit, allure) и чтение `.gitlab-ci.yml`
- 9.4 флейки: `framework/fixtures/tracing` — `traceparent` на каждый тест, при падении ссылка на Jaeger + request_id в Allure;
  `pytest -p no:randomly --count 20` для поиска флейка, маркер `quarantine` (отдельный необязательный job), без rerun в гейте
- 9.5 Allure с историей: gh-pages + `allure generate` с копией `history/`, уведомление в Telegram/Slack — обзор, по желанию

## Модуль 10. Senior-навыки — выдан

- Артефакты в `docs/qa/`: `TEST_STRATEGY.md` (риски биржи, матрица вероятность × ущерб, пирамида, что не автоматизируем),
  `TESTING_GUIDELINES.md` (гайдлайн + чек-лист ревью), `adr/0001-…`, `adr/0002-…` (2 ADR по фреймворку),
  `METRICS.md` (5 метрик для менеджмента), `TEST_PLAN_market_orders.md` (тест-план + оценка), `ONBOARDING.md`
- Ревью: `practice/m10_review_me.py` (PR джуна, >15 проблем, ответы внизу файла)
- LLM-фичи: тест-дизайн для «AI-объяснения сделки» (структура, факты против API, LLM-as-judge, golden set)
- Собес: 5 behavioural-историй по STAR в `docs/qa/INTERVIEW_STORIES.md`

## Дальше — по порядку PROGRAM.md

6 моки и отказы (WireMock/responses, Toxiproxy) ·
7 безопасность (OWASP API Top 10, JWT, HMAC) · 8 производительность в функц. тестах · 9 CI/CD ·
10 senior · 11–12 Locust
