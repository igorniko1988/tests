# API-фреймворк: дорожная карта и прогресс

Фреймворк пишет пользователь, Claude ставит задачи и ревьюит (см. `CLAUDE.md`).
Тесты — `api_tests/`, запуск `uv run pytest`, отчёт `uv run pytest --alluredir=allure-results` → `allure serve allure-results`.

## Где остановились (2026-10-25)

**Этап 2, шаг 2.2 выдан** — модель запроса `CreateOrder` с умолчаниями, `OrderService.create(order: CreateOrder)`
через `model_dump(mode='json')`, в тестах `create(CreateOrder())` / `CreateOrder(price=Decimal('10'))`.

Хвосты:
- 2.1: `Balance` без `strict`, `available`/`locked` — `Decimal`, `asset` — `Literal`; в `test_cancel_orders` сравнивать `Decimal('200')`.
- 1.6: POST повторять только для `/orders` и `/auth/login` (второй `HTTPAdapter` через `mount` по префиксу) —
  в режиме сбоев `allowed_methods=None` дважды зачисляет депозит; уборка в `auth_api` пропускает, если `list()` не 200.

## Этап 1. Каркас — ✅

- 1.1 `ApiClient` (сессия, таймаут, `set_token`) · 1.2 Settings и `envs/` · 1.3 сервисы Auth, Balance, Order
- 1.4 `list`/`get`/`cancel`, teardown через `yield` в `auth_api`, тесты в `api_tests/`, корневой `conftest.py`
- 1.5 `transport/reporting.py`: строка лога на запрос + шаги и вложения Allure, тела `/auth/*` не прикладываются
- 1.6 `Retry` на 503 через `HTTPAdapter`, `Idempotency-Key` на `POST /orders`

## Этап 2. Модели и контракты — идёт

- 2.1 точные типы в моделях ответов (UUID, Decimal, datetime, Literal), lax + `extra='forbid'` — почти готово
- 2.2 модели запросов с умолчаниями — **выдан**
- 2.3 негативные тесты контракта: 422 на каждое неверное поле через `parametrize`
- 2.4 сверка с OpenAPI-схемой стенда (`/openapi.json`)

## Дальше

3 данные и изоляция · 4 бизнес-логика · 5 безопасность · 6 CI · 7 не-REST · 8 моки и отказы, Pact ·
9 производительность, Locust · 10 senior
