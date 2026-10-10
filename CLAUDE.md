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
- Stage-экземпляр: `docker compose --profile stage up -d` → http://localhost:8081.
  Своя база и JWT-секрет, 5% сбоев (`EXCHANGE_STAGE_CHAOS_RATE`). Обычный `up` его не трогает.

## Окружение

- Python 3.13 через `uv` (3.14 не используем: у gevent/grpcio/pact может не быть колёс).
- Зависимости: группы `service` (только стенд, идут в Docker-образ), `tests`, `dev`.
  `uv sync` ставит всё.
- Тесты: `uv run pytest`. Условия заданий UI — `practice/tasks/`, решения пользователь пишет
  в `tests/ui/` и `ui_framework/` с нуля (рабочие папки очищены 2026-10-10).
