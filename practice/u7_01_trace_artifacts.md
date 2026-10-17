# U7. Урок 1 — Trace Viewer, скриншоты, видео и отчёт

Задания: `practice/tasks/test_u7_01_trace_artifacts.py`, решение — `tests/ui/test_u7_01_trace_artifacts.py` (создаёшь сам).

План: какие артефакты даёт pytest-playwright и как их включить; где они лежат (проверено);
ловушка — context вне фикстур без артефактов; Trace Viewer — что в нём есть и как разбирать падение
по шагам; ручная трассировка; видео (и почему у нас локально его нет); артефакты в Allure; что включать
локально, а что в CI.

Модуль U7: U7.1 артефакты и Trace Viewer → U7.2 отладка и «в CI падает, локально проходит» + собес.

---

## 1. Артефакты pytest-playwright

```bash
uv run pytest tests/ui --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure
```

| Опция | Значения | Что |
|---|---|---|
| `--tracing` | `on`, `off`, `retain-on-failure` | trace.zip — полная запись теста |
| `--screenshot` | `on`, `off`, `only-on-failure` | скриншот в конце теста |
| `--full-page-screenshot` | флаг | скриншот всей страницы, а не экрана |
| `--video` | `on`, `off`, `retain-on-failure` | видео каждой страницы (webm) |
| `--output` | путь, по умолч. `test-results` | куда складывать |

Проверено на стенде (`--tracing retain-on-failure --screenshot only-on-failure`):

```
test-results/
  test-fixture-page-fails-chromium/
    test-failed-1.png
    trace.zip
  test-new-context-fails-chromium/
    test-failed-1.png
    trace.zip
```

- у **прошедшего** теста — ничего (на то и `retain-on-failure`);
- папка — имя теста + браузер (+ параметры parametrize);
- `test-results/` в `.gitignore` (U2.3).

### Ловушка: context вне фикстур

Артефакты пишутся для context, созданных **фикстурами плагина** — `context`, `page`, `new_context`.
Проверено: тест, который сам вызвал `browser.new_context()`, упал — и **ни trace, ни скриншота** нет.
Поэтому в фреймворке context создаём через `new_context` (U1.4, U5.1), а не через `browser.new_context`.

---

## 2. Trace Viewer

```bash
uv run playwright show-trace test-results/<папка>/trace.zip
```

Или открыть trace.zip на **trace.playwright.dev** — файл обрабатывается в браузере, на сервер не отправляется.
Удобно, когда trace скачан из CI на машину без Python.

Что внутри (`unzip -l trace.zip`): `trace.trace` (действия), `trace.network` (сеть), `screencast/*.jpeg` (кадры),
`resources/` (HTML, CSS, картинки для снимков DOM).

### Панели

| Панель | Что смотреть |
|---|---|
| **Actions** | список шагов теста: `goto`, `click`, `fill`, `expect` — с длительностью; упавший — красный |
| **Timeline** | кадры экрана по времени — видно, что было на экране в момент шага |
| **Снимки DOM: Before / Action / After** | **живой** DOM до действия, в момент (с точкой клика), после — можно инспектировать как в DevTools |
| **Call** / **Log** | параметры действия и лог actionability (U2.3): что ждали, почему не кликнулось |
| **Errors** | текст ошибки и место в коде |
| **Console** | консоль браузера: ошибки JS, `console.log` |
| **Network** | запросы со статусами, заголовками, телами — тот самый 503 на `app.js` (U2.4) |
| **Source** | строка теста для выбранного шага |
| **Metadata** | браузер, viewport, время |

Снимок DOM — не картинка, а **разметка**: можно найти элемент, посмотреть атрибуты, проверить локатор
(кнопка «Pick locator» прямо в Trace Viewer).

### Как разбирать упавший тест

1. **Errors** — что именно упало: таймаут действия, проверка, strict mode.
2. **Actions** → упавший шаг → **Before**: что было на экране и в DOM. Элемент есть? Другой текст? Модалка сверху?
3. **Log** шага — чего ждал Playwright: `element is not visible`, `intercepts pointer events`.
4. **Network** вокруг шага — ответы сервера: 4xx/5xx, медленный ответ, ответа нет.
5. **Console** — JS-ошибки фронта.
6. Шаги **до** упавшего — часто причина раньше: пополнение не прошло → ордер не создался → упала проверка таблицы.

---

## 3. Ручная трассировка

Когда нужен trace без опции командной строки, или для context вне фикстур:

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
...
context.tracing.stop(path=tmp_path / "trace.zip")
```

Куски одной долгой сессии (session-scope context из U5.3):

```python
context.tracing.start(screenshots=True, snapshots=True)
for name in ("step1", "step2"):
    context.tracing.start_chunk(title=name)
    ...
    context.tracing.stop_chunk(path=f"{name}.zip")
context.tracing.stop()
```

Группы шагов в trace (как шаги Allure):

```python
context.tracing.group("Пополнить счёт")
...
context.tracing.group_end()
```

API-запросы через `context.request` тоже попадают в trace — подготовка через API (U5) видна рядом с UI-шагами.

---

## 4. Скриншоты

```python
page.screenshot(path=tmp_path / "page.png", full_page=True)
locator.screenshot(path="widget.png")                         # только элемент
page.screenshot(mask=[page.get_by_test_id("lab-clock")])       # закрасить динамику
```

`--screenshot only-on-failure` — последний кадр упавшего теста. Скриншоты для **сравнения** (визуальная
регрессия) — U8.

---

## 5. Видео

```bash
uv run pytest --video retain-on-failure
```

Видео пишется на context и **дописывается при его закрытии**. Вручную: `browser.new_context(record_video_dir=..., record_video_size=...)`,
путь — `page.video.path()` после `context.close()`.

**У нас локально видео нет.** Проверено: Playwright требует свой ffmpeg, а `playwright install ffmpeg` на macOS 12
отвечает `Playwright does not support ffmpeg on mac12`. Тест с `--video` падает на создании страницы.
Видео включают в CI (Linux/Docker, U9). Trace почти всегда полезнее видео: там тот же экран **плюс** DOM, сеть, консоль.

---

## 6. Артефакты в Allure

Хук из U4.4 прикладывал скриншот и URL. Добавить trace:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "teardown":                               # артефакты плагин пишет на teardown
        output = item.funcargs.get("output_path")               # фикстура плагина: папка артефактов теста
        if output and Path(output).is_dir():
            for file in Path(output).glob("*"):
                allure.attach.file(str(file), name=file.name)
```

`output_path` — фикстура pytest-playwright: путь к папке этого теста в `test-results`. Trace плагин записывает
**после** теста (в teardown context), поэтому прикладывать — на фазе teardown, а не call.

Allure сам не открывает trace — в отчёте он будет файлом для скачивания и просмотра на trace.playwright.dev.

---

## 7. Что включать где

| | Локально | CI |
|---|---|---|
| trace | `retain-on-failure` или вручную | `retain-on-failure` — **всегда** |
| скриншот | по желанию | `only-on-failure` |
| видео | нет (macOS 12) / по желанию | `retain-on-failure`, если хватает места |
| Allure | при необходимости | да, с вложениями |

`--tracing on` для всех тестов — тяжело (сотни МБ) и медленнее; включают точечно для расследования.

---

## Собес: вопросы и ответы

**1. Что такое Trace Viewer и как разбираешь по нему упавший тест?**
> Trace — запись теста: шаги с длительностью, снимки DOM до и после каждого действия, кадры экрана, сеть, консоль,
> лог ожиданий, исходник. Открываю `playwright show-trace` или на trace.playwright.dev. Сначала ошибка, потом
> упавший шаг и снимок Before — что было на экране и в DOM, лог действия — чего ждал Playwright, сеть и консоль
> вокруг шага, и шаги до — причина часто раньше.

**2. Какие артефакты собираешь при падении?**
> Trace с retain-on-failure — главный, плюс скриншот на падении, в CI — видео, если позволяет место. Всё
> прикладываю в Allure. Плюс логи стенда по request id (U2.4).

**3. Почему у теста нет trace, хотя опция включена?**
> Плагин пишет артефакты для context, созданных его фикстурами — `page`, `context`, `new_context`. Если тест
> создал context через `browser.new_context()`, артефактов нет. Решение — `new_context` или ручной
> `context.tracing.start/stop`.

**4. Trace или видео?**
> Trace почти всегда полезнее: там тот же экран плюс DOM, сеть, консоль и лог. Видео удобно показать не
> технарям — как воспроизводится баг. Видео тяжелее и требует ffmpeg.
