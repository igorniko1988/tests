# C6 · Декораторы

**Смысл темы.** Декоратор — функция, которая принимает функцию и возвращает новую, «обёрнутую»:
та делает что-то до и после вызова оригинала — замеряет время, логирует, повторяет при ошибке,
кэширует. Это классика лайвкодинга: «напиши `timer`», «напиши `retry` с параметрами» спрашивают
почти всегда. И это основа pytest: `@pytest.fixture`, `@pytest.mark.parametrize`, `@allure.step` —
всё декораторы. Собирается тема из двух кирпичиков C4: функции — объекты и замыкания.

---

### 1. Декоратор без «магии»

```python
import time

def timer(func):                      # принимает функцию
    def wrapper(*args, **kwargs):     # новая функция-обёртка
        start = time.perf_counter()
        result = func(*args, **kwargs)        # вызываем оригинал с теми же аргументами
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result                 # и возвращаем его результат
    return wrapper                    # возвращаем обёртку, НЕ вызывая её

def slow_add(a, b):
    time.sleep(0.1)
    return a + b

slow_add = timer(slow_add)            # имя slow_add теперь указывает на wrapper
print(slow_add(1, 2))                 # slow_add took 0.100s | 3
```

```
до:     slow_add ──▶ функция slow_add

после:  slow_add ──▶ wrapper ──(замыкание: func)──▶ исходная slow_add
```

- **`wrapper` помнит `func` через замыкание** (C4, раздел 6) — даже когда `timer` уже завершился.
- **`*args, **kwargs`** — обёртка принимает любые аргументы и прокидывает их без изменений:
  один декоратор подходит к любой функции.
- **`return result` обязателен:** без него задекорированная функция вернёт `None` — частая
  ошибка на собесе.
- **`return wrapper` без скобок:** возвращаем функцию, а не результат её вызова.

---

### 2. `@` — синтаксический сахар

```python
@timer
def slow_add(a, b):
    ...

# ровно то же самое, что:
def slow_add(a, b):
    ...
slow_add = timer(slow_add)
```

- **Декоратор срабатывает один раз — при определении функции** (при импорте модуля), а не при
  каждом вызове. При каждом вызове работает `wrapper`.
- **Это видно на print:** если в теле `timer` (вне `wrapper`) написать `print("decorating")`,
  он напечатается при `def`, даже если функцию ни разу не вызвали.

---

### 3. `functools.wraps`

Без него обёртка «теряет лицо» оригинала:

```python
@timer
def slow_add(a, b):
    """Складывает медленно."""

print(slow_add.__name__, slow_add.__doc__)    # wrapper None
```

```python
from functools import wraps

def timer(func):
    @wraps(func)                  # копирует __name__, __doc__, __module__, __qualname__ ...
    def wrapper(*args, **kwargs):
        ...
    return wrapper

print(slow_add.__name__, slow_add.__doc__)    # slow_add Складывает медленно.
print(slow_add.__wrapped__)                   # исходная функция — доступ к оригиналу
```

- **Зачем это на практике:** логи и отчёты показывают имя функции (`wrapper` вместо `test_login`
  бесполезен), pytest и allure берут имена и docstring, `inspect.signature` видит настоящую
  сигнатуру через `__wrapped__`.
- **`@wraps(func)` — сам декоратор с параметром** (раздел 4): `wraps(func)` возвращает декоратор,
  который применяется к `wrapper`.
- **Правило:** в любом декораторе пиши `@wraps(func)` — на собесе это проверяют.

---

### 4. Декоратор с параметрами

`@retry(times=3)` — сначала **вызывается** `retry(times=3)`, и уже его результат применяется
к функции. Значит, нужен ещё один уровень вложенности:

```python
import time
from functools import wraps

def retry(times=3, exceptions=(Exception,), delay=0.0):   # 1) параметры
    def decorator(func):                                  # 2) получает функцию
        @wraps(func)
        def wrapper(*args, **kwargs):                     # 3) заменяет функцию
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise                             # попытки кончились — пробросить
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(times=3, exceptions=(ConnectionError,), delay=0.5)
def get_price():
    ...

# то же самое: get_price = retry(times=3, exceptions=(ConnectionError,), delay=0.5)(get_price)
```

- **Три уровня:** фабрика параметров → декоратор → обёртка. Каждый следующий видит переменные
  предыдущих через замыкание.
- **`@retry` без скобок сломается:** функция придёт в параметр `times`, а результатом станет
  `decorator`. Нужно `@retry()`. (Как сделать, чтобы работали оба варианта, — раздел 8.)
- **`except exceptions:`** — `except` принимает кортеж классов исключений, ловит любой из них.
- **`raise` без аргумента** пробрасывает текущее исключение с исходным traceback.
- **Повторять можно только то, что безопасно повторять:** GET — да, POST «создать ордер» — только
  если сервер поддерживает идемпотентность, иначе получишь два ордера.

---

### 5. Несколько декораторов: порядок

```python
def bold(func):
    @wraps(func)
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@bold
@italic
def text():
    return "hi"

print(text())        # <b><i>hi</i></b>
```

- **Применяются снизу вверх:** `text = bold(italic(text))` — ближний к `def` применяется первым.
- **Выполняются сверху вниз, снаружи внутрь:** при вызове сначала работает внешняя обёртка
  (`bold`), она вызывает внутреннюю (`italic`), та — оригинал. «Матрёшка».
- **Порядок важен:** `@retry` над `@timer` замерит каждую попытку; `@timer` над `@retry` — все
  попытки вместе.

---

### 6. Декоратор-класс и состояние

Декоратором может быть любой вызываемый объект, в том числе класс с `__call__`:

```python
from functools import update_wrapper

class CountCalls:
    def __init__(self, func):
        update_wrapper(self, func)   # как @wraps, но для объекта
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):     # объект вызывают как функцию
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def ping():
    return "pong"

ping(); ping()
print(ping.count)        # 2 — ping теперь объект CountCalls
```

- **Состояние в атрибутах объекта** — удобнее, чем `nonlocal` в функции.
- **Состояние у функции-обёртки** тоже можно хранить атрибутом: `wrapper.calls = 0`.
- **`__call__`** — магический метод «вызов» (C9): `obj(...)` → `obj.__call__(...)`.
- **Подвох с методами:** класс-декоратор на методе класса теряет `self` (раздел 7, задача ★).

---

### 7. Декораторы на методах класса

```python
class Client:
    @timer
    def get(self, path):         # self попадёт в *args обёртки — функциональный декоратор работает
        ...

    @staticmethod                # тоже декораторы — встроенные (C7)
    def build_url(base, path): ...

    @classmethod
    def from_env(cls): ...

    @property
    def token(self): ...
```

- **Функция-декоратор работает и для функций, и для методов:** `self` — просто первый элемент
  `args`, его прокидывает `*args`.
- **Класс-декоратор на методе ломается:** `client.get(...)` найдёт в классе объект `CountCalls`,
  а не функцию, и `self` не подставится. Чинят методом `__get__` (дескриптор, ★-задача t06).
- **`@staticmethod`, `@classmethod`, `@property`** — встроенные декораторы, меняют, как метод
  получает первый аргумент.

---

### 8. Декоратор со скобками и без

```python
def retry(func=None, *, times=3):
    if func is None:                 # вызвали как @retry(times=5) — вернуть декоратор
        return lambda f: retry(f, times=times)

    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper

@retry
def a(): ...

@retry(times=5)
def b(): ...
```

- **Приём:** первый параметр — функция или `None`, остальные только именованные (`*`).
- **Нужен редко,** но показывает, что понимаешь, как применяется `@`.

---

### 9. Декораторы в автотестах

```python
import pytest

@pytest.fixture
def api():
    return ApiClient(base_url="http://localhost:8080")

@pytest.mark.parametrize(("side", "status"), [("BUY", 201), ("HOLD", 422)])
def test_create_order(api, side, status):
    ...

@pytest.mark.skip(reason="bug EX-42")
def test_known_bug(): ...

@pytest.mark.xfail(reason="price feed flaky")
def test_market_order(): ...
```

- **`@pytest.fixture`** регистрирует функцию как фикстуру; **`@pytest.mark.*`** вешает метку на
  тест — pytest читает её при сборе (`-m smoke`).
- **`retry` в своём фреймворке** — для нестабильных внешних вызовов (не для тестов целиком — так
  прячут баги). Для перезапуска тестов есть плагин `pytest-rerunfailures`.
- **`@allure.step("Создать ордер")`** — декоратор, который пишет шаг в отчёт.
- **Свой `@log_step`** в фреймворке: логирует имя метода, аргументы и время — это задачи урока.

---

**Частые ошибки.**
- Забыли `return result` в обёртке — функция стала возвращать `None`.
- `return wrapper()` вместо `return wrapper` — функция вызвалась при декорировании.
- Нет `@wraps(func)` — у всех задекорированных функций имя `wrapper`.
- `@retry` без скобок у декоратора с параметрами — функция попала в `times`.
- `retry` ловит `Exception` и повторяет даже на `AssertionError` или `TypeError` — баги в коде
  прячутся за ретраями. Ловить нужно конкретные сетевые исключения.
- Класс-декоратор на методе — теряется `self`.

---

### Собес

- **Что такое декоратор и как он работает?** Функция, которая принимает функцию и возвращает
  новую. Обычно внутри создаётся `wrapper(*args, **kwargs)`, который делает что-то до и после
  вызова оригинала и возвращает его результат; оригинал он помнит через замыкание. `@deco` над
  `def f` — то же, что `f = deco(f)`, выполняется один раз при определении функции.
- **Зачем `functools.wraps`?** Обёртка — другая функция, у неё имя `wrapper` и нет docstring.
  `@wraps(func)` копирует `__name__`, `__doc__`, `__module__` и ставит `__wrapped__`. Без этого
  логи, отчёты и инструменты (pytest, inspect) видят не ту функцию.
- **Напиши декоратор с параметром.** Три уровня: `def retry(times): def decorator(func):
  @wraps(func) def wrapper(*a, **kw): ...; return wrapper; return decorator`. `@retry(3)` сначала
  вызывает `retry(3)`, результат — декоратор — применяется к функции.
- **В каком порядке применяются два декоратора?** Снизу вверх: `@a @b def f` = `f = a(b(f))`.
  При вызове работают сверху вниз: сначала обёртка `a`, внутри неё — `b`, внутри — оригинал.
- **Какие декораторы есть в pytest?** `@pytest.fixture`, `@pytest.mark.parametrize`,
  `@pytest.mark.skip`/`skipif`/`xfail`, свои маркеры `@pytest.mark.smoke`. Плюс `@allure.step`
  и `@allure.title` в отчётах.
- **Чем опасен retry?** Повтор неидемпотентных запросов (создание ордера) даёт дубли; ловля
  широкого `Exception` прячет баги. Повторять только безопасное и только на конкретных ошибках
  (таймаут, 503), с задержкой и лимитом попыток.

---

### Практика

Все команды — из папки `interview_prep/python_course/week2/c06_decorators`.

- **Упражнения «что выведет»:** `drills.py`. Проверка: `uv run python drills.py`.
- **Задачи** (условия на английском, тесты: `uv run pytest -k t01`):
  - обязательные: t01 `timer`, t02 `log_calls`, t03 `retry`, t04 `CountCalls`, t05 `ttl_cache`;
  - ★ t06 декоратор-класс, который работает и на методах.
