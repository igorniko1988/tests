# U9. Урок 2 — Docker-образ Playwright, CI, артефакты и стабильность; собес по модулю U9

Задания: `tests/ui/test_u9_02_docker_ci.py`.

План: зачем тесты в Docker; официальный образ Playwright и запуск наших тестов в нём против стенда
(проверено: Firefox, WebKit и видео, которых нет на macOS 12); подводные камни (venv, `addopts`, сеть,
`--ipc=host`); CI на GitHub Actions — пайплайн целиком; артефакты; ретраи и карантин в CI; метрики стабильности; собес.

---

## 1. Зачем Docker

- **одинаковое окружение**: та же ОС, шрифты, браузеры, что в CI — нет «у меня работает» (U7.2) и расхождения
  эталонов скриншотов (U8.1);
- **все браузеры и ffmpeg**: на нашей macOS 12 Playwright даёт только системный Chrome (U9.1), в образе — Chromium,
  Firefox, WebKit и видео;
- CI-раннеры и так запускают джобы в контейнерах — локальный запуск в образе = воспроизведение CI.

---

## 2. Официальный образ

`mcr.microsoft.com/playwright/python:v1.63.0-noble` — Ubuntu 24.04 + Python + браузеры **той же версии**, что пакет
`playwright` (тег = версия пакета; несовпадение версий — «Executable doesn't exist»). `-jammy` — Ubuntu 22.04.

Внутри: браузеры Playwright и системные зависимости. **Нет**: наших зависимостей (uv, pytest-плагины) и системного
Google Chrome — `--browser-channel chrome` в образе не сработает.

### Запуск наших тестов в образе

```bash
docker run --rm --ipc=host \
  -v "$PWD":/work -w /work \
  -e UV_PROJECT_ENVIRONMENT=/tmp/venv \
  --add-host=host.docker.internal:host-gateway \
  mcr.microsoft.com/playwright/python:v1.63.0-noble \
  bash -c "pip install -q uv && uv sync --frozen -q && \
           uv run pytest tests/ui/test_u1_04_context_pytest.py -o addopts='-ra --strict-markers' \
             --base-url http://host.docker.internal:8080 --browser firefox --browser webkit"
```

Разбор флагов — каждый из них важен:

| Флаг | Зачем |
|---|---|
| `--ipc=host` | Chromium использует общую память; без этого падает на больших страницах |
| `-v "$PWD":/work` | код из репозитория |
| `-e UV_PROJECT_ENVIRONMENT=/tmp/venv` | **не трогать** `.venv` хоста: там бинарники macOS, uv в Linux его бы пересоздал |
| `--add-host=host.docker.internal:host-gateway` | доступ к стенду на хосте (`:8080`) из контейнера |
| `-o addopts='...'` | убрать `--browser-channel chrome` из `pyproject` — Chrome в образе нет |
| `--base-url` | адрес стенда из контейнера — не `localhost` (это сам контейнер) |

Лучше вместо `-o addopts` сделать канал **настраиваемым**: в `addopts` его не держать, а передавать из Settings / CI
(задача 2) — тогда одна команда работает везде.

Альтернатива `host.docker.internal` — запустить тесты **в той же сети docker compose**, что стенд:
`--network api_learning_default` и `--base-url http://exchange:8000`.

---

## 3. CI на GitHub Actions

Пайплайн UI-тестов (файл `.github/workflows/ui-tests.yml` — создаёшь в задании 4):

```yaml
name: ui-tests
on:
  pull_request:
  schedule: [{cron: "0 2 * * *"}]          # ночной полный прогон

concurrency:                               # новый пуш в PR отменяет старый прогон
  group: ui-${{ github.ref }}
  cancel-in-progress: true

jobs:
  ui:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        shard: [0, 1, 2]
    env:
      SHARD_TOTAL: 3
      SHARD_INDEX: ${{ matrix.shard }}
      TEST_RUN_ID: ${{ github.run_id }}     # общий RUN_ID для данных всех шардов (U5.2, U9.1)
      ENV: docker
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with: {enable-cache: true}
      - name: Стенд
        run: docker compose up -d --build --wait
      - name: Зависимости и браузер
        run: |
          uv sync --frozen
          uv run playwright install --with-deps chromium
      - name: Тесты
        run: >
          uv run pytest tests/ui -m "smoke or regression" -n 2
          --browser chromium --tracing retain-on-failure --screenshot only-on-failure
          --alluredir allure-results --junitxml report-${{ matrix.shard }}.xml
      - name: Артефакты
        if: always()                        # и при падении — именно тогда они нужны
        uses: actions/upload-artifact@v4
        with:
          name: ui-${{ matrix.shard }}
          path: |
            test-results/
            allure-results/
            report-*.xml
          retention-days: 14
      - name: Логи стенда
        if: failure()
        run: docker compose logs exchange > exchange.log
```

Ключевые решения:
- `--with-deps` ставит системные библиотеки браузера на Ubuntu;
- `--browser chromium` без channel — Chromium Playwright, а не системный Chrome;
- `fail-fast: false` — падение одного шарда не отменяет остальные, видно всю картину;
- `if: always()` у артефактов; логи стенда при падении (U2.4: поиск по X-Request-ID);
- `--wait` у compose — дождаться healthcheck стенда;
- секреты — `${{ secrets.UI_USER_PASSWORD }}` в `env`, не в файле (U4.3).

Allure-отчёт из нескольких шардов собирают отдельной джобой: скачать все `allure-results`, `allure generate`,
опубликовать (GitHub Pages / артефакт). История и тренды — сохранять папку `history` между прогонами.

Jenkins и GitLab CI устроены так же: стадии, матрица/параллель, артефакты, `always`-шаги. Подробно — модуль 9 части API.

---

## 4. Ретраи и карантин в CI

Повтор U2.4 с точки зрения CI:

```bash
uv run pytest ... --reruns 2 --reruns-delay 1 --only-rerun "TimeoutError|503"
```

- `--only-rerun` — перезапускать только по похожим на инфраструктуру ошибкам, а не любые `AssertionError`;
- тест, прошедший с перезапуска, — **флейк**: в отчёте `RERUN`, по нему заводится задача;
- карантин — маркер `quarantine`, отдельная джоба «карантин» с `continue-on-error: true`: тесты бегут, но не блокируют PR;
- выход из карантина — серия зелёных прогонов (`--count 50` ночью).

## 5. Метрики стабильности

| Метрика | Как считать | Зачем |
|---|---|---|
| **pass rate** | доля зелёных прогонов набора | общее здоровье |
| **flaky rate** | тестов, прошедших с rerun / всех тестов | сколько «шума» |
| **топ флейков** | тесты по числу rerun за 2 недели | что чинить первым |
| размер карантина | тестов в карантине и как давно | не превращается ли в кладбище |
| длительность | p50/p95 прогона и шардов | деградация, перекос шардов |
| время до починки | от появления флейка до исправления | процесс работает? |

Источник данных — JUnit XML (`--junitxml`), Allure history, API CI. Без метрик флейки накапливаются молча.

---

## 6. Шпаргалка по модулю U9

- Масштаб: xdist (процессы) × шарды (машины); шард — стабильный хеш nodeid или pytest-split по длительности;
  общий `RUN_ID` из CI; ускорение упирается в стенд и самые длинные тесты.
- Браузеры: `--browser` × N, `only_browser`/`skip_browser`; CDP-хелперы — только Chromium; у нас локально только Chrome.
- Docker: образ `playwright/python:v<версия>-noble`, `--ipc=host`, отдельный venv, сеть до стенда, без channel chrome.
- CI: стенд → зависимости → `playwright install --with-deps` → тесты с шардами → артефакты `if: always()` → Allure.
- Стабильность: rerun только по инфраструктурным ошибкам, флейк = задача, карантин не блокирует, метрики.

---

## Собес: вопросы и ответы

Плюс вопросы U9.1 (4).

**1. Как запускаете UI-тесты в CI?** (вопрос из программы)
> На каждый PR — smoke и регресс в Chromium, шардами по машинам и xdist внутри. Стенд поднимается в docker compose
> с ожиданием healthcheck, зависимости через uv с кэшем, браузеры — `playwright install --with-deps` или готовый
> образ Playwright. Артефакты — trace, скриншоты, Allure, логи стенда — выгружаются всегда. Ночью — полный набор и
> кросс-браузерный smoke. Секреты из CI.

**2. Как параллелите?** (из программы)
> xdist внутри машины, матрица шардов между машинами; шарды по длительности. Данные изолированы: уникальные значения
> с id сборки, seed вне воркеров, общие ресурсы — без пересечений.

**3. Что делаете с флейками?** (из программы)
> Ретрай только на инфраструктурные ошибки и как сигнал, а не лечение: прошедший с rerun тест — задача. Не чинится
> сразу — карантин с владельцем в неблокирующей джобе. Смотрим метрики — flaky rate и топ флейков, — чиним причины
> по категориям (U2.4).

**4. Зачем запускать тесты в Docker?**
> Одинаковое окружение с CI — ОС, шрифты, браузеры той же версии, — значит воспроизводимые падения и эталоны
> скриншотов. Плюс все браузеры и видео там, где локальная ОС их не поддерживает, как у нас на macOS 12.

**5. Какие подводные камни у запуска в контейнере?**
> Версия образа должна совпадать с пакетом playwright. `--ipc=host` для Chromium. Не затирать venv хоста.
> `localhost` в контейнере — это контейнер, стенд — через host.docker.internal или общую сеть compose.
> Системного Chrome в образе нет.
