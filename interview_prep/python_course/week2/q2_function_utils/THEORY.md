# Q2 · Утилиты на функциях

**Смысл темы.** На собесе AQA вместо LeetCode часто просят написать кусок тестового фреймворка:
`retry` для нестабильного вызова, ожидание условия `wait_until`, шаг теста с логом и временем,
отправку пачками, разбор лога. Всё это — функции, замыкания, декораторы и генераторы из C4–C6,
собранные под реальные задачи. Важны и инженерные детали: что логировать, когда сдаваться, как не
спрятать баг за повтором, как тестировать без реального ожидания (подменяемые `sleep` и `clock`).

---

### 1. retry с экспоненциальной задержкой

```python
import time
from functools import wraps

def retry(times=3, delay=0.5, backoff=2.0, exceptions=(ConnectionError, TimeoutError)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    time.sleep(wait)
                    wait *= backoff            # 0.5 → 1 → 2 → 4 ...
        return wrapper
    return decorator
```

- **Exponential backoff:** каждая следующая пауза длиннее — сервис успевает «отдышаться». В бою
  добавляют **jitter** (случайный разброс), чтобы тысяча клиентов не ретраила синхронно.
- **Что повторять:** только временные ошибки — таймаут, разрыв соединения, 502/503/504, 429
  (с учётом `Retry-After`). 400/401/404/422 повторять бессмысленно.
- **Идемпотентность:** GET/PUT/DELETE безопасно повторять, POST «создать ордер» — нет, если сервер
  не принимает `Idempotency-Key`. Иначе — два ордера.
- **Не ретраить тесты целиком:** это прячет баги и флаки.

---

### 2. wait_until — своё ожидание условия

Так устроены `expect(...)` в Playwright и `WebDriverWait` в Selenium.

```python
import time

def wait_until(condition, timeout=5.0, interval=0.1, message="condition"):
    deadline = time.monotonic() + timeout
    while True:
        result = condition()
        if result:
            return result
        if time.monotonic() >= deadline:
            raise TimeoutError(f"{message} not met in {timeout}s")
        time.sleep(interval)
```

- **Передаём функцию, а не значение:** проверка выполняется заново на каждой итерации.
- **`time.monotonic()`:** монотонные часы не прыгают при переводе системного времени.
- **Проверка хотя бы один раз** — даже при `timeout=0`.
- **Понятная ошибка:** `TimeoutError("order filled not met in 10s")` сразу говорит, чего не дождались.
- **Почему не `time.sleep(5)`:** фиксированная пауза либо слишком длинная, либо слишком короткая (флаки).

---

### 3. Подменяемые зависимости: clock и sleep

Тест утилиты с `timeout=10` не должен идти 10 секунд. Делаем время параметром:

```python
def wait_until(condition, timeout=5.0, interval=0.1, *, clock=time.monotonic, sleep=time.sleep):
    ...

now = [0.0]                       # «фальшивое» время, его двигает fake_sleep

def fake_clock():
    return now[0]

def fake_sleep(seconds):
    now[0] += seconds

wait_until(lambda: False, timeout=10, clock=fake_clock, sleep=fake_sleep)   # мгновенно: TimeoutError
```

- **Dependency injection** в миниатюре: функция не знает, откуда время, — его подставляют.
- **Альтернатива — `monkeypatch`:** `monkeypatch.setattr(module.time, "sleep", fake)`.
- **Тот же приём** для `random`, UUID, текущей даты — всего недетерминированного.

---

### 4. Шаг теста: время и лог

```python
def step(name, log):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                log.append(f"STEP {name}: FAILED {type(error).__name__}")
                raise
            log.append(f"STEP {name}: PASSED in {time.perf_counter() - start:.2f}s")
            return result
        return wrapper
    return decorator
```

- **Так работает `allure.step`:** название шага, статус и время в отчёте.
- **Исключение не глотаем:** логируем и пробрасываем — тест должен упасть.

---

### 5. Пачки

```python
def send_in_batches(items, n, send):
    batch = []
    for item in items:                 # items может быть генератором — без len()
        batch.append(item)
        if len(batch) == n:
            send(batch)
            batch = []
    if batch:
        send(batch)                    # хвост
```

- **Зачем:** у bulk-эндпоинтов лимит размера тела, а по одному — медленно.
- **Ошибка в середине:** решаем заранее — остановиться или продолжить и собрать неудачные пачки.

---

### 6. Разбор логов генераторами

```python
def filter_log(lines, level="ERROR"):
    for number, line in enumerate(lines, start=1):
        parts = line.split(maxsplit=2)
        if len(parts) >= 2 and parts[1] == level:
            yield number, line
```

- **Номер строки** — чтобы найти место в исходном логе.
- **Уровень сравниваем точно** (`== "ERROR"`), а не `"ERROR" in line` — иначе `ERRORS` и слово
  ERROR в сообщении дадут ложные срабатывания.

---

**Частые ошибки.**
- `retry` ловит `Exception` и повторяет `AssertionError` или `TypeError` — баг прячется.
- `retry` спит после последней попытки.
- `wait_until` проверяет `condition` (функцию, всегда truthy), а не `condition()`.
- `time.sleep` в тестах вместо ожидания условия; ожидание без понятного сообщения.
- `len(items)` в функции, которая должна принимать генератор.

---

### Собес

- **Напиши retry. Что повторять, а что нет?** Декоратор с параметрами: попытки, задержка, backoff,
  кортеж исключений. Повторяю только временные ошибки (таймаут, разрыв, 5xx, 429) и только
  идемпотентные запросы. После последней попытки пробрасываю исключение и не сплю.
- **Как устроено ожидание в Playwright/Selenium?** Цикл: вызвать условие; истинно — вернуть;
  вышел таймаут — TimeoutError с понятным сообщением; иначе поспать интервал. Время по `monotonic`.
- **Как тестировать код со `sleep` и временем?** Делать `clock` и `sleep` параметрами и подставлять
  фальшивые, или `monkeypatch`. Тест мгновенный и детерминированный.
- **Чем опасны ретраи в автотестах?** Прячут баги и флаки, удлиняют прогон, для неидемпотентных
  запросов создают дубли.

---

### Задачи

Все команды — из папки `interview_prep/python_course/week2/q2_function_utils`, тесты: `uv run pytest -k t01`.

- **Обязательные:** t01 `retry` с backoff, t02 `step`, t04 `send_in_batches`, t06 `wait_until`.
- **★ по желанию:** t03 `filter_log`, t05 `flatten`.
