# API-фреймворк: дорожная карта и прогресс

Фреймворк пишет пользователь, Claude ставит задачи и ревьюит (см. `CLAUDE.md`).
Тесты — `api_tests/`, запуск `uv run pytest`, отчёт `uv run pytest --alluredir=allure-results` → `allure serve allure-results`.

## Где остановились (2026-10-26)

**Этап 3, шаг 3.1 выдан** — `funded_api` (депозит USDT и ETH), фабрика-фикстура `create_order(**fields)` → `Order`,
тесты на ордера переведены на неё, проверка `uv run pytest -n 4`.
2.4 почти готово: в `test_contract.py` нужно `CreateOrder()` со скобками.

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
- 2.2 модели запросов с умолчаниями (`CreateOrder` на строках, `exclude` для пропуска поля) — ✅
- 2.3 негативные тесты контракта: 422 на каждое неверное поле через `parametrize` — 2 случая, хвост: больше полей и границы
- 2.4 сверка с OpenAPI: `framework/contract.py`, `assert_matches_schema(data, 'OrderOut')`; эталон можно хранить в `framework/openapi.json`

## Этап 3. Данные и изоляция — идёт

- 3.1 `funded_api` + фабрика `create_order`, параллельный прогон `-n 4` — **выдан**

## Дальше

3 данные и изоляция · 4 бизнес-логика · 5 безопасность · 6 CI · 7 не-REST · 8 моки и отказы, Pact ·
9 производительность, Locust · 10 senior
