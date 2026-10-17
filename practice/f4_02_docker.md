# F4. Урок 2 — Docker: образы, контейнеры, compose, логи, сети

Задания: `practice/f4_02_docker_answers.md`.

## Зачем QA

Наш стенд уже живёт в Docker. В реальных проектах QA поднимает сервисы локально через compose,
гоняет тесты в контейнере в CI, смотрит логи упавшего сервиса. На собесе: «чем образ отличается
от контейнера», «как посмотреть логи», «как тесты попадут в сеть сервиса».

## 1. Образ и контейнер

- **Образ** (image) — шаблон: ОС + Python + зависимости + код. Неизменяемый. Как класс.
- **Контейнер** — запущенный экземпляр образа. Как объект класса. Из одного образа — много контейнеров.
- **Dockerfile** — рецепт сборки образа.

Наш `Dockerfile`:

```dockerfile
FROM python:3.13-slim                 # базовый образ
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv
WORKDIR /app                          # рабочая папка внутри
COPY pyproject.toml uv.lock ./        # сначала зависимости...
RUN uv sync --frozen --no-default-groups --group service
COPY exchange ./exchange              # ...потом код
EXPOSE 8000
CMD ["uvicorn", "exchange.main:app", "--host", "0.0.0.0", "--port", "8000"]   # что запускать
```

**Слои и кэш**: каждая инструкция — слой. Если файлы не менялись, слой берётся из кэша.
Зависимости копируются **до** кода — поэтому правка кода не переустанавливает пакеты.

## 2. Основные команды

```bash
docker images                         # образы
docker ps                             # запущенные контейнеры;  -a — все, включая остановленные
docker run -d -p 5433:5432 -e POSTGRES_PASSWORD=x --name pg postgres:16-alpine
#            │  │ хост:контейнер │ переменная            │ имя    │ образ
docker logs -f pg                     # логи
docker exec -it pg sh                 # зайти внутрь контейнера (shell)
docker exec pg pg_isready             # выполнить одну команду
docker stop pg && docker rm pg        # остановить и удалить
docker inspect pg                     # всё о контейнере (JSON): env, сети, IP, mounts
docker stats                          # CPU / память контейнеров
```

## 3. docker compose — несколько сервисов

```bash
docker compose up -d --build          # собрать и запустить всё в фоне
docker compose ps                     # статус сервисов
docker compose logs -f exchange       # логи одного сервиса
docker compose exec db psql -U exchange   # команда в сервисе
docker compose restart exchange
docker compose down                   # остановить и удалить контейнеры (данные в volume остаются)
docker compose down -v                # + удалить volumes (база с нуля)
```

Важное в `docker-compose.yml`:
- `ports: "8080:8000"` — порт хоста 8080 → порт 8000 в контейнере;
- `environment` — переменные (адрес БД, секрет, chaos rate);
- `depends_on` + `condition: service_healthy` — ждать, пока БД реально готова (healthcheck);
- `profiles: ["stage"]` — сервис запускается только с `--profile stage`.

## 4. Сети

Compose создаёт общую сеть. Внутри неё сервисы видят друг друга **по имени сервиса**:
exchange подключается к `db:5432`, а не к `localhost`.

```text
твой Mac ── localhost:8080 ──▶ [exchange :8000] ── db:5432 ──▶ [db :5432]
         └─ localhost:5432 ─────────────────────────────────────▶ [db]
```

Ловушка: **`localhost` внутри контейнера — это сам контейнер**, а не твой Mac.
Если тесты запущены в контейнере, адрес стенда — `http://exchange:8000`, а не `localhost:8080`.
Из контейнера к хосту на Mac — `host.docker.internal`.

## 5. Volumes — данные

Контейнер одноразовый: удалил — данные пропали. **Volume** хранит данные отдельно
(например, базу). `-v ./reports:/app/reports` — пробросить папку хоста внутрь (для отчётов тестов).

## 6. Тесты в Docker (как в CI)

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.63.0-noble   # браузеры уже внутри; версия = версии playwright в проекте
WORKDIR /tests
COPY . .
RUN pip install uv && uv sync --group tests
CMD ["uv", "run", "pytest", "--alluredir=reports"]
```

Зачем: одинаковое окружение у всех и в CI, не нужно ставить браузеры на агент.

## Вопросы собеседования

1. Образ vs контейнер?
2. Что такое слои и почему зависимости копируют до кода?
3. Как посмотреть логи контейнера и зайти внутрь?
4. Почему из контейнера нельзя обратиться к `localhost`, чтобы попасть в другой сервис?
5. Чем `docker compose down` отличается от `down -v`?
6. Зачем запускать тесты в Docker?
