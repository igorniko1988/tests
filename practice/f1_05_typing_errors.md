# F1. Урок 5 — типизация, исключения, `*args` / `**kwargs`

Задачи к уроку: `practice/f1_05_typing_errors.py`.

## Зачем это QA

- **Типы** — подсказки в PyCharm, меньше ошибок, читаемый фреймворк. Pydantic строит проверки именно по аннотациям.
- **Исключения** — тест падает = исключение. Нужно понимать, какие бывают, как их ловить и бросать свои.
- **`*args` / `**kwargs`** — в декораторах, обёртках клиента (`request(method, path, **kwargs)`), фабриках данных.

## 1. Аннотации типов

```python
def deposit(asset: str, amount: float) -> dict:
    return {"asset": asset, "amount": amount}


email: str = "a@b.com"
balances: dict[str, float] = {"USDT": 100.0}
ids: list[int] = [1, 2, 3]
```

**Python не проверяет типы при запуске.** `deposit(123, "abc")` выполнится. Аннотации нужны:
- людям — понять, что передавать;
- PyCharm и линтерам (mypy) — подсветить ошибку до запуска;
- Pydantic — он **по аннотациям** проверяет данные.

### Частые конструкции

```python
from typing import Literal

token: str | None = None                 # строка или None
side: Literal["BUY", "SELL"]             # только одно из значений
def get_user(user_id: int) -> "User": ...  # возвращает объект класса User
items: list[dict[str, str]]              # список словарей
```

### `Protocol` — «умеет вот это» (обзор)

```python
from typing import Protocol


class HasGet(Protocol):
    def get(self, path: str): ...


def ping(client: HasGet) -> None:   # подойдёт ЛЮБОЙ объект с методом get — наследоваться не нужно
    client.get("/health")
```

Это «утиная типизация» с подсказками: важно, **что объект умеет**, а не от какого класса он унаследован.

## 2. Исключения

Ошибка во время работы = **исключение**. Если его никто не поймал — программа (или тест) падает.

```python
try:
    value = int("abc")
except ValueError as error:          # поймать конкретный тип
    print("не число:", error)
else:
    print("ошибки не было")          # выполнится, только если в try не было исключения
finally:
    print("выполнится всегда")       # уборка — при ошибке и без
```

### Частые встроенные исключения

| Исключение | Когда |
|---|---|
| `ValueError` | значение неподходящее: `int("abc")` |
| `TypeError` | не тот тип: `"a" + 1` |
| `KeyError` | нет ключа в словаре: `d["нет"]` |
| `IndexError` | нет индекса в списке |
| `AttributeError` | нет атрибута: `None.json()` |
| `AssertionError` | упал `assert` — так падает тест |

### Правила

- **Лови конкретное**, а не всё подряд. `except Exception:` — только когда действительно нужно (как в retry).
- **Голый `except:`** — никогда: он ловит даже Ctrl+C.
- **Не глуши ошибки молча** (`except: pass`) — баг спрячется.
- **`raise`** без аргументов внутри `except` — пробросить пойманную ошибку дальше.

### Свои исключения

```python
class ApiError(Exception):
    def __init__(self, status_code: int, body: str):
        super().__init__(f"API вернул {status_code}: {body}")
        self.status_code = status_code
        self.body = body


raise ApiError(500, "Internal Server Error")
```

Свой класс исключения — понятное имя и полезные поля (статус, тело ответа).
Ловить можно точечно: `except ApiError as e: e.status_code`.

### `raise ... from ...` — сохранить причину

```python
try:
    data = response.json()
except ValueError as error:
    raise ApiError(response.status_code, response.text) from error
```

В трейсбеке будут видны обе ошибки: исходная причина и твоя.

## 3. `*args` и `**kwargs`

```python
def log(*args, **kwargs):
    print(args)      # кортеж позиционных аргументов
    print(kwargs)    # словарь именованных


log(1, 2, level="info")
# (1, 2)
# {'level': 'info'}
```

### Распаковка при вызове

```python
def create_user(email, password, role="user"): ...

data = {"email": "a@b.com", "password": "secret123"}
create_user(**data)              # то же, что create_user(email=..., password=...)

values = ["a@b.com", "secret123"]
create_user(*values)             # то же, что create_user("a@b.com", "secret123")
```

### Где это в тестах

```python
def request(self, method, path, **kwargs):          # клиент: принять любые опции requests
    kwargs.setdefault("timeout", self.timeout)
    return self._session.request(method, self.base_url + path, **kwargs)


def make_order(**overrides):                         # фабрика данных: значения по умолчанию + замены
    order = {"symbol": "ETH-USDT", "side": "BUY", "price": "2", "quantity": "1"}
    order.update(overrides)
    return order


make_order(side="SELL", price="5")
```

### Порядок параметров

```python
def f(a, b=2, *args, c, d=4, **kwargs): ...
#     обычные → *args → только именованные → **kwargs
```

Параметры после `*args` (здесь `c`, `d`) можно передать **только по имени**.

## Шпаргалка

| Что | Пример |
|---|---|
| аннотация | `def f(x: int) -> str:` |
| или None | `str \| None = None` |
| одно из | `Literal["BUY", "SELL"]` |
| поймать | `try / except Тип as e / else / finally` |
| бросить | `raise ValueError("...")` |
| пробросить | `raise` внутри `except` |
| своё исключение | `class ApiError(Exception): ...` |
| сохранить причину | `raise New(...) from error` |
| принять любые | `def f(*args, **kwargs)` |
| распаковать | `f(*список)`, `f(**словарь)` |

## Вопросы собеседования

1. Проверяет ли Python типы при запуске? Зачем тогда аннотации?
2. Чем `except Exception` отличается от голого `except:`? Почему нельзя `except: pass`?
3. Что делают `else` и `finally` в `try`?
4. Зачем свои классы исключений? Что даёт `raise ... from ...`?
5. Что такое `*args` и `**kwargs`? Что значит `**` при вызове функции?
6. Какое исключение бросает упавший `assert`?
