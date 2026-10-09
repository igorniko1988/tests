# U3. Урок 2 — диалоги браузера, загрузка и скачивание файлов

Задания: `tests/ui/test_u3_02_dialogs_files.py`. Страница: лаборатория `/app/lab.html`
(блоки «Диалоги», «Импорт и экспорт»).

План: нативные диалоги `alert` / `confirm` / `prompt` / `beforeunload` и как Playwright с ними
работает (поведение по умолчанию — проверено); загрузка файлов — `set_input_files` с диска, из памяти,
несколько, очистка, file chooser; скачивание — `expect_download`, имя, сохранение, проверка содержимого;
генерация файлов для тестов.

---

## 1. Диалоги браузера

Это **нативные** окна браузера (`alert`, `confirm`, `prompt`), не HTML-модалки (U4.2). Пока диалог открыт,
страница заблокирована — JS ждёт ответа.

### Поведение по умолчанию

Если у страницы **нет** обработчика события `dialog`, Playwright **сам закрывает** диалог (`dismiss`).
Проверено: кнопка «Очистить избранное» без обработчика → `confirm` вернул `false` → «Отменено».
Для `confirm` это «Отмена», для `prompt` — `null`.

Поэтому тест «подтверждаю удаление» без обработчика молча проверит **отмену**.

### Обработчик

```python
page.once("dialog", lambda dialog: dialog.accept())        # один раз, на ближайший диалог
page.get_by_test_id("confirm-button").click()
expect(page.get_by_test_id("dialog-result")).to_have_text("Избранное очищено")
```

```python
def answer(dialog: Dialog) -> None:
    assert dialog.type == "prompt"
    assert dialog.message == "Новое имя портфеля"
    assert dialog.default_value == "Основной"
    dialog.accept("Агрессивный")                            # текст для prompt

page.once("dialog", answer)
page.get_by_test_id("prompt-button").click()
expect(page.get_by_test_id("portfolio-name")).to_have_text("Агрессивный")
```

| Свойство / метод | Что |
|---|---|
| `dialog.type` | `alert`, `confirm`, `prompt`, `beforeunload` |
| `dialog.message` | текст диалога |
| `dialog.default_value` | значение по умолчанию у `prompt` |
| `dialog.accept(text=None)` | «ОК» (для prompt — с текстом) |
| `dialog.dismiss()` | «Отмена» / закрыть |

Проверено на лаборатории: `alert` «Торги идут круглосуточно», `confirm` «Удалить всё избранное?»,
`prompt` с значением по умолчанию «Основной».

### Ловушки

- **Обработчик обязан ответить.** Если обработчик есть, но не вызвал `accept`/`dismiss`, диалог висит,
  и действие (`click`) висит до таймаута. Обработчик, который только логирует, — ошибка.
- `page.on("dialog", ...)` действует **до конца** жизни страницы — следующий диалог в тесте попадёт в тот же
  обработчик. Для одного диалога — `page.once`. Снять — `page.remove_listener("dialog", handler)`.
- Проверки (`assert`) внутри обработчика выполняются в обработчике событий: упавший `assert` может не уронить
  тест сразу и превратиться в непонятный таймаут. Надёжнее **сохранить** данные диалога и проверить их
  в теле теста:

```python
dialogs: list[tuple[str, str]] = []
page.once("dialog", lambda d: (dialogs.append((d.type, d.message)), d.accept()))
page.get_by_test_id("alert-button").click()
assert dialogs == [("alert", "Торги идут круглосуточно")]
```

- `beforeunload` («Уйти со страницы? Изменения не сохранятся») появляется при `page.close(run_before_unload=True)`
  или навигации; по умолчанию `page.close()` его не вызывает.

---

## 2. Загрузка файлов

### set_input_files

```python
upload = page.get_by_test_id("import-input")

upload.set_input_files("tests/ui/data/trades.csv")                    # путь
upload.set_input_files([path1, path2])                                 # несколько (если input multiple)
upload.set_input_files({"name": "bad.csv", "mimeType": "text/csv",     # из памяти, без файла на диске
                        "buffer": b"a,b\n1,2\n"})
upload.set_input_files([])                                             # очистить выбор
```

Проверено на лаборатории:
- CSV с двумя строками → «Импортировано строк: 2 (файлов: 1)»;
- неверные колонки из буфера → «Ошибка: Ожидались колонки: …»;
- пустой список → «Файлы не выбраны».

`set_input_files` работает с `<input type="file">` **напрямую** — системное окно выбора файла не открывается
(его автотест и не смог бы нажать). Input может быть скрытым (кастомная кнопка «Загрузить» поверх) — всё равно
вызывай на input.

### file chooser — когда input не найти

Если кнопка создаёт input динамически или его не достать локатором:

```python
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="Загрузить аватар").click()
chooser = fc_info.value
chooser.is_multiple()                    # можно ли несколько (проверено: аватар — False)
chooser.set_files("avatar.png")
```

### Drag & drop файла в зону загрузки

Зоны «перетащите файл сюда» слушают событие `drop` с `DataTransfer`. Обычно у них есть скрытый input — используй
его. Если нет — `dispatch_event("drop", {"dataTransfer": data_transfer})`, где `data_transfer` создают через
`page.evaluate_handle(...)`. Это редкий случай, достаточно знать, что так можно.

---

## 3. Скачивание файлов

```python
with page.expect_download() as download_info:
    page.get_by_test_id("export-button").click()
download = download_info.value

download.suggested_filename                         # имя, которое предлагает сайт: quotes-2026-10-10.csv
path = tmp_path / download.suggested_filename
download.save_as(path)                              # сохранить, пока context жив
rows = path.read_text(encoding="utf-8").splitlines()
assert rows[0] == "ticker,price,change"
```

Проверено: экспорт — `quotes-<дата>.csv`, 21 строка (заголовок + 20 котировок).

- скачанный файл лежит во временной папке и **удаляется при закрытии context** — сохраняй через `save_as`;
- `download.path()` — путь к временному файлу (ждёт завершения скачивания);
- `download.failure()` — `None`, если скачалось;
- имя файла с датой — тест не должен зависеть от «сегодня» (U4.4, U6.2): проверяй шаблон
  `re.fullmatch(r"quotes-\d{4}-\d{2}-\d{2}\.csv", name)` или зафиксируй время `page.clock`.

### Что проверять в скачанном файле

- формат: заголовки, разделитель, кодировка;
- содержимое **совпадает с тем, что на экране** (или в API) — это главное;
- для XLSX/PDF — библиотеки чтения (`openpyxl`, `pypdf`), проверка ключевых значений, а не байт в байт.

---

## 4. Файлы для тестов

| Нужно | Как |
|---|---|
| CSV / JSON | собрать в тесте (`csv`, `json`) в `tmp_path` или буфер в памяти |
| картинка | `page.screenshot(path=...)`, Pillow, или маленький PNG в `tests/ui/data/` |
| большой файл (проверка лимита) | `path.write_bytes(os.urandom(2 * 1024 * 1024))` |
| файл с «плохим» именем | `"отчёт 2030 (копия).csv"`, очень длинное, без расширения |
| неверный формат | `.exe` вместо `.csv`, CSV без заголовка, пустой файл |

Граничные кейсы загрузки (U5.2 + тест-дизайн F2): размер на границе лимита, 0 байт, неверный тип, несколько файлов,
повторная загрузка того же файла, отмена выбора.

---

## Собес: вопросы и ответы

**1. Как работать с alert / confirm / prompt в Playwright?**
> Подписаться на событие `dialog` до действия — `page.once` для одного диалога — и в обработчике вызвать
> `accept` или `dismiss`, для prompt — `accept(text)`. Без обработчика Playwright сам закрывает диалог через
> dismiss, поэтому «подтверждение» без обработчика на самом деле проверит отмену. Обработчик обязан ответить,
> иначе действие повиснет. Данные диалога сохраняю и проверяю в теле теста.

**2. Как протестировать загрузку файла?**
> `set_input_files` на `input type=file` — путь, список или файл из памяти с именем, типом и байтами; пустой
> список очищает. Системное окно не открывается. Если input не достать — `expect_file_chooser` вокруг клика.
> Проверяю результат в UI и граничные случаи: размер, тип, пустой файл, несколько файлов.

**3. Как протестировать скачивание файла?**
> `expect_download` вокруг клика, `save_as` в `tmp_path` — пока context жив, потом временный файл удалится.
> Проверяю имя (шаблоном, если в нём дата) и содержимое: формат и совпадение с данными на экране или в API.

**4. Чем нативный диалог отличается от модального окна?**
> Нативный — окно браузера, блокирует JS страницы; в DOM его нет, работаю через событие `dialog`.
> Модальное окно — обычный HTML-элемент с ролью dialog; с ним работаю локаторами и компонентом (U4.2).
