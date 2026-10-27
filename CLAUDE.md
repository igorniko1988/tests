# CLAUDE.md

Учебный проект: программа «API-тестирование на Python, уровень Senior» (см. `PROGRAM.md`).
Трекер прогресса: https://claude.ai/artifact/NcRHhuunzHDMmrPmncDvrL

## Роли — главное правило

- **Claude пишет только стенд** — сервис «мини-биржа» в `exchange/` и его инфраструктуру
  (`Dockerfile`, `docker-compose.yml`, будущие сервисы вроде провайдера котировок).
- **Фреймворк (`framework/`) и тесты (`tests/`, `load/`) пишет пользователь сам.**
  Claude не генерирует в них код, даже «для примера», без прямой просьбы.
- Роль Claude в тестовой части — ментор: даёт задания с критериями готовности,
  объясняет теорию, делает ревью кода пользователя, даёт подсказки, если он застрял.
- В стенд специально закладываются баги. Claude не раскрывает, где они, пока
  пользователь не поймает их тестом или сам не попросит подсказку.

## Как проходят занятия

Договорённости накопились по ходу курса; при расхождении с разделом «Роли» действуют эти.

- **Порядок курса:** фундамент F1–F4 → UI (Playwright, U1–U10, 34 урока) → API-часть программы.
  Уроки идут по порядку; на «на чём остановились» продолжаем с текущего урока.
- **Материалы урока:** теория — `practice/uN_MM_*.md` (всё вместе — `practice/UI_COURSE.md`,
  пересборка: `uv run python practice/build_ui_course.py`), условия заданий — `practice/tasks/`,
  файлы ревью — `practice/*_review_me.py` (ответы пользователь пишет внизу файла).
- **Теория — полная:** простой язык, но объём не урезаем: примеры на стенде, таблицы методов,
  частые ошибки, раздел «Собес» с готовыми ответами. На каждый вопрос из заданий есть ответ в теории.
- **Кто пишет код (UI с U4):** пользователь, в `ui_framework/` и `tests/ui/`. Claude даёт теорию
  и задания, ревьюит по «проверь», подсказывает. Решение Claude пишет только для урока, который
  пользователь прямо назвал («сделай за меня этот урок»); «дальше» = теория и задания следующего урока.
- **Режим «делаем вместе» (с U4.3):** Claude показывает код в чате маленькими шагами и объясняет
  каждую строку, даёт команду проверки; пользователь перепечатывает, пишет «готово» или вопрос.
  В файлы Claude сам не пишет. Темп: сначала то, что спрашивают на собесе, второстепенное — кратко.
- **Стиль Page Object пользователя:** страницы через фасад `Application` (`app.auth_page`,
  `app.dashboard_page`), фикстуры только готовят состояние (`app`, `logged_user` …). Методы PO
  не возвращают другие страницы; один метод на позитив и негатив — ждёт ответ сервера и возвращает
  `Response`, статус проверяет тест. В ревью это не считать ошибкой.
- **Тестовые данные:** уникальный пользователь на тест и teardown открытых ордеров — стакан общий,
  чужие ордера ломают тест сделки.
- **framework2** (requests, ветка `feat/framework2`) и **лайвкодинг** (ветка `livecoding`,
  тренажёр `trainer/` на :8090 из ветки `stand/trainer`, без багов) — код пишет пользователь, Claude ставит задачи и разбирает решения.

## Git-процесс

- Репозиторий: https://github.com/igorniko1988/tests
- GitHub Flow: `main` всегда рабочий, каждое задание — своя ветка и Pull Request.
- Git-команды для своей работы пользователь выполняет сам (это часть курса, модуль 0).
  Claude подсказывает команды и объясняет, но не коммитит и не пушит за него.
- Пока пользователь проходит весь цикл руками: PR, ревью, merge — через сайт GitHub.
  `gh` и автоматизацию добавляем позже, когда ручной цикл освоен. Не предлагать `gh` раньше.
- Ревью задания без `gh`: `git fetch`, затем `git diff main...origin/<ветка>`;
  замечания Claude пишет в чат со ссылками `файл:строка`, пользователь переносит их в PR сам.
- Изменения стенда Claude делает в своей ветке `stand/...` и открывает PR,
  который пользователь мержит сам.
- Коммиты по Conventional Commits: `feat:`, `fix:`, `test:`, `chore:`, `docs:`.

## Язык

Общение на русском. Код, идентификаторы и технические термины — в оригинале.

## Стенд

- Запуск: `docker compose up -d --build` → http://localhost:8080 (веб-интерфейс на `/app/`,
  Swagger на `/docs`). Фронтенд — ванильный JS в `exchange/web/`, у элементов есть `data-testid`.
- Лаборатория `/app/lab.html` — статическая страница для уроков UI (вкладки, iframe, диалоги, файлы,
  drag & drop, Shadow DOM, модалка, окружение браузера); бэкенд не нужен. Статика вшита в образ —
  после правок `exchange/web/` нужен `--build`.
- macOS 12: Playwright не ставит свои Chromium/Firefox/WebKit и ffmpeg — локально только системный Chrome
  (`--browser-channel chrome`), остальные браузеры и видео — в образе `mcr.microsoft.com/playwright/python:v1.63.0-noble`.
- Локально без Docker-сервиса: `docker compose up -d db`, затем
  `uv run uvicorn exchange.main:app --reload --port 8000`.
- Стек: FastAPI, SQLAlchemy 2 (async) + Postgres, JWT (PyJWT). Суммы — Decimal, в API строкой.
- Схема БД создаётся на старте (`create_all`), миграций пока нет.
- Режим сбоев: `EXCHANGE_CHAOS_RATE=0.3 docker compose up -d` — 30% запросов отвечают 503
  с `Retry-After: 1`; половина сбоев случается уже после обработки запроса.
  `/health` и `/docs` не затрагиваются. По умолчанию выключен.
- Сопоставление ордеров идёт в фоне раз в `EXCHANGE_MATCHING_INTERVAL` секунд (по умолчанию 1):
  исполнение видно не сразу. Цена сделки — цена более раннего ордера.
- Логи: одна JSON-строка на запрос (`level`, `request_id`, `method`, `path`, `status`, `duration_ms`);
  `X-Request-ID` из запроса (или сгенерированный) возвращается в ответе.
  Поиск: `docker compose logs exchange | grep <request_id>`.
- Kubernetes (Docker Desktop): `kubectl apply -f k8s/exchange.yaml`, затем
  `kubectl -n exchange port-forward svc/exchange 8082:8000`. Образ — локальный `api_learning-exchange:latest`.
- WebSocket `/ws/orderbook/{symbol}`: сначала `snapshot`, затем `update` на каждое изменение стакана;
  `sequence` растёт на 1. Неизвестный символ — закрытие с кодом 4004.
- Вебхуки: `POST /webhooks {url}` → `secret`; на `order.filled` и `order.canceled` стенд шлёт POST
  с `X-Event-Id`, `X-Event-Type`, `X-Delivery-Attempt` и `X-Signature: sha256=<HMAC тела секретом>`.
  Не 2xx — повтор через 1, 2, 4 с (всего 4 попытки, `EXCHANGE_WEBHOOK_MAX_ATTEMPTS`). Из Docker
  приёмник на хосте доступен как `host.docker.internal`.
- Kafka (Redpanda, `localhost:19092`): стенд пишет в `orders.events` (3 партиции, ключ — id ордера)
  события `order.created`, `order.partially_filled`, `order.filled`, `order.canceled`.
  Смотреть: `docker compose exec redpanda rpk topic consume orders.events -n 5`.
- RabbitMQ (`localhost:5672`, консоль `:15672`, `exchange`/`exchange`): очередь `deposits`,
  тело `{"user_id", "asset", "amount"}` + обязательный `message_id`; повтор с тем же id не зачисляется,
  битые сообщения уходят в `deposits.dlq`. Без `EXCHANGE_KAFKA_BOOTSTRAP` / `EXCHANGE_RABBITMQ_URL` выключены.
- Провайдер цен (WireMock `price-feed`, `localhost:8089`, админка `/__admin`): `type: MARKET` без `price`
  берёт цену из `GET /prices/{symbol}` → `{"symbol", "price", "timestamp"}`. Ошибка, таймаут
  (`EXCHANGE_PRICE_FEED_TIMEOUT`, 2 с) или цена старше `EXCHANGE_PRICE_MAX_AGE` (10 с) — 503
  `price_unavailable` / `price_stale`, деньги не блокируются. Цены по умолчанию — `wiremock/mappings/`,
  `POST /__admin/reset` возвращает к ним.
- Toxiproxy (`localhost:8474`): стенд ходит к провайдеру цен через прокси `price_feed`
  (`toxiproxy:8666` → `price-feed:8080`). Сбои сети — `POST /proxies/price_feed/toxics`,
  `POST /reset` убирает все toxics и включает прокси.
- Stage-экземпляр: `docker compose --profile stage up -d` → http://localhost:8081.
  Своя база и JWT-секрет, 5% сбоев (`EXCHANGE_STAGE_CHAOS_RATE`). Обычный `up` его не трогает.

## Окружение

- Python 3.13 через `uv` (3.14 не используем: у gevent/grpcio/pact может не быть колёс).
- Зависимости: группы `service` (только стенд, идут в Docker-образ), `tests`, `dev`.
  `uv sync` ставит всё.
- Тесты: `uv run pytest`. Условия заданий UI — `practice/tasks/`, решения пользователь пишет
  в `tests/ui/` и `ui_framework/` с нуля (рабочие папки очищены 2026-10-10).
