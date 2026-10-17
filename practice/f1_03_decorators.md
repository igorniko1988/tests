# F1. Урок 3 — декораторы

Задачи к уроку: `practice/f1_03_decorators.py`.

## Зачем это QA

Декораторы в тестах на каждом шагу: `@pytest.fixture`, `@pytest.mark.parametrize`,
`@allure.step`, `@property`. Свои декораторы пишут для логирования шагов, замера времени,
повторов (retry). На собеседовании просят написать простой декоратор руками.

## 1. Функция — это объект

Функцию можно положить в переменную, передать в другую функцию и вернуть из функции.

```python
def hello():
    return "hello"


f = hello           # без скобок — сама функция, а не её результат
print(f())          # hello


def call_twice(func):
    func()
    func()

call_twice(hello)   # передали функцию как аргумент
```

`hello` — сама функция. `hello()` — **вызов** функции и её результат.

## 2. Функция внутри функции

```python
def make_greeter(name):
    def greet():
        return f"hello, {name}"      # внутренняя функция помнит name
    return greet                      # вернули функцию, не вызывая


greet_anna = make_greeter("Anna")
print(greet_anna())                   # hello, Anna
```

Внутренняя функция **запоминает** переменные внешней, даже когда внешняя уже закончилась.
Это называется **замыкание** (closure). На нём построены декораторы.

## 3. Декоратор — функция, которая оборачивает другую функцию

```python
def log_calls(func):
    def wrapper():
        print(f"вызываю {func.__name__}")
        result = func()                 # вызвать исходную функцию
        print(f"{func.__name__} закончила")
        return result
    return wrapper


def say_hi():
    print("hi")

say_hi = log_calls(say_hi)    # подменили функцию обёрткой
say_hi()
# вызываю say_hi
# hi
# say_hi закончила
```

Декоратор принимает функцию, создаёт **обёртку** (`wrapper`), которая делает что-то **до** и **после**
вызова, и возвращает обёртку вместо исходной функции.

### Синтаксис `@`

Строка `say_hi = log_calls(say_hi)` настолько частая, что для неё есть сокращение:

```python
@log_calls
def say_hi():
    print("hi")
```

`@log_calls` над функцией — **ровно то же самое**, что `say_hi = log_calls(say_hi)` после неё.

## 4. Обёртка для функций с любыми аргументами

У декорируемой функции могут быть аргументы. Обёртка должна принять **любые** и передать дальше:

```python
def log_calls(func):
    def wrapper(*args, **kwargs):              # принять что угодно
        print(f"вызываю {func.__name__} с {args} {kwargs}")
        return func(*args, **kwargs)           # передать как есть
    return wrapper


@log_calls
def deposit(asset, amount):
    return f"{asset}: +{amount}"


deposit("USDT", amount=100)
# вызываю deposit с ('USDT',) {'amount': 100}
```

- `*args` — кортеж позиционных аргументов;
- `**kwargs` — словарь именованных;
- `func(*args, **kwargs)` — «разложить» их обратно при вызове.

## 5. `functools.wraps` — сохранить имя функции

Без него у задекорированной функции имя станет `wrapper`, и в отчётах pytest / Allure будет путаница.

```python
from functools import wraps


def log_calls(func):
    @wraps(func)                     # скопировать имя, docstring и т.п. с func на wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

**Правило:** в каждом своём декораторе — `@wraps(func)`.

## 6. Декоратор с параметрами

`@retry(times=3)` — у декоратора есть свои параметры. Нужен ещё один уровень функции:

```python
from functools import wraps


def retry(times):                          # 1. принимает параметры декоратора
    def decorator(func):                   # 2. принимает функцию
        @wraps(func)
        def wrapper(*args, **kwargs):      # 3. принимает аргументы функции
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise              # попытки кончились — пробросить ошибку
                    print(f"попытка {attempt} не удалась, повторяю")
        return wrapper
    return decorator


@retry(times=3)
def flaky():
    ...
```

`@retry(times=3)` → сначала вызывается `retry(3)` и возвращает `decorator`, а уже он оборачивает функцию.

Запомни три уровня: **параметры декоратора → функция → аргументы функции**.

## 7. Несколько декораторов

```python
@log_calls
@retry(times=3)
def place_order(): ...
```

Применяются **снизу вверх**: сначала `retry`, потом `log_calls` оборачивает уже результат.
То есть `place_order = log_calls(retry(times=3)(place_order))`.

## 8. Декораторы, которые ты уже видел

| Декоратор | Что делает |
|---|---|
| `@property` | превращает метод в «поле» |
| `@staticmethod`, `@classmethod` | меняют, что получает метод первым аргументом |
| `@dataclass` | дописывает классу `__init__`, `__repr__`, `__eq__` (декоратор класса) |
| `@pytest.fixture` | регистрирует функцию как фикстуру |
| `@pytest.mark.parametrize(...)` | декоратор с параметрами: прогнать тест на наборах данных |
| `@allure.step("...")` | записать вызов функции шагом в отчёт |

## Шпаргалка

```python
from functools import wraps


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # до вызова
        result = func(*args, **kwargs)
        # после вызова
        return result
    return wrapper
```

## Вопросы собеседования

1. Что такое декоратор? Что на самом деле делает строка `@decorator` над функцией?
2. Зачем в обёртке `*args, **kwargs`?
3. Зачем `functools.wraps`?
4. Как написать декоратор с параметрами (например, `@retry(times=3)`)? Почему там три уровня функций?
5. В каком порядке применяются несколько декораторов?
6. Напиши декоратор, который замеряет время выполнения функции (частая задача на лайвкодинге).
