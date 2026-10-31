# C9 · Магические методы и dataclasses

**Смысл темы.** Магические (dunder) методы — `__repr__`, `__eq__`, `__len__`, `__add__` и другие с
двумя подчёркиваниями — это способ научить свой класс работать со встроенными операциями Python:
`print`, `==`, `len`, `in`, `for`, `+`, `sorted`, `with`. Python сам вызывает их: `a + b` — это
`a.__add__(b)`, `len(x)` — `x.__len__()`. Это называется **модель данных Python**. `dataclass`
генерирует самые нужные из них автоматически — так пишут модели ответов API в тестах. На собесе
спрашивают `__repr__` vs `__str__`, `__eq__` без `__hash__`, `__new__` vs `__init__` и dataclass vs pydantic.

---

### 1. `__repr__` и `__str__`

```python
class Order:
    def __init__(self, order_id, symbol):
        self.order_id, self.symbol = order_id, symbol

    def __repr__(self):                       # для разработчика: однозначно, как создать
        return f"Order(order_id={self.order_id!r}, symbol={self.symbol!r})"

    def __str__(self):                        # для человека: читаемо
        return f"order #{self.order_id} {self.symbol}"

o = Order(7, "BTC")
print(o)              # order #7 BTC          — print и str() берут __str__
print(repr(o))        # Order(order_id=7, symbol='BTC')
print([o])            # [Order(order_id=7, symbol='BTC')]  — внутри коллекций всегда __repr__
f"{o!r}"              # repr в f-строке
```

- **Без них** печатается `<__main__.Order object at 0x10a...>` — бесполезно в логах и в сообщении
  упавшего assert.
- **Нет `__str__` — используется `__repr__`.** Поэтому если писать один — пиши `__repr__`.
- **Хороший `__repr__`** выглядит как код, создающий объект: в отчёте pytest сразу видно, какой
  объект сравнивали.

---

### 2. `__eq__` и `__hash__`

```python
class Ticker:
    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def __eq__(self, other):
        if not isinstance(other, Ticker):
            return NotImplemented             # «не умею сравнивать с этим» — Python попробует иначе
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)              # по тем же полям, что и __eq__

print(Ticker("btc") == Ticker("BTC"))         # True
print(len({Ticker("btc"), Ticker("BTC")}))    # 1
```

- **По умолчанию `==` сравнивает идентичность** (`is`): два одинаковых по данным объекта не равны.
- **Определил `__eq__` без `__hash__` — объект стал НЕхешируемым:** Python ставит `__hash__ = None`,
  `set` и ключ dict дают `TypeError: unhashable type`. Это защита: равные объекты обязаны иметь
  равный хеш, а старый хеш (по `id`) это нарушил бы.
- **Правило:** если `a == b`, то `hash(a) == hash(b)`. Хешируй по тем же полям, что сравниваешь,
  и только по **неизменяемым** — иначе объект «потеряется» в set после изменения поля (C3).
- **`NotImplemented`** (не `False` и не `NotImplementedError`) — Python попробует отражённую
  операцию `other.__eq__(self)`, а если и она не умеет — сравнит по идентичности.

---

### 3. Сравнение и сортировка

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):                   # a < b
        return self.parts < other.parts        # кортежи сравниваются поэлементно

print(sorted(["1.10.0", "1.9.3", "1.2"], key=Version))   # ['1.2', '1.9.3', '1.10.0']
print(Version("2.0") >= Version("1.10"))                 # True — >= достроил total_ordering
```

- **`__lt__` достаточно для `sorted`, `min`, `max`.** Для `<=`, `>`, `>=` нужны свои методы или
  `@total_ordering`, который достроит их из `__eq__` и одного из сравнений.
- **Строки версий сравнивать как строки нельзя:** `"1.10" < "1.9"` — True посимвольно.

---

### 4. Арифметика

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):                 # v + w
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):                     # v * 3
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__                        # 3 * v: int не умеет, Python вызывает v.__rmul__(3)

    def __abs__(self):                        # abs(v)
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

- **Отражённые методы `__radd__`, `__rmul__`:** `3 * v` — сначала `int.__mul__(3, v)` →
  `NotImplemented`, затем `v.__rmul__(3)`.
- **`sum(vectors)`** начинает с `0`: `0 + v` вызовет `v.__radd__(0)` — либо реализуй его,
  либо передай старт: `sum(vectors, Vector(0, 0))`.
- **Возвращай новый объект,** не меняй `self` — так ведут себя числа (иммутабельность).
- **`__iadd__`** — для `+=`; если его нет, Python использует `__add__` и перепривязывает имя (C1).

---

### 5. Контейнерные методы

```python
class Cart:
    def __init__(self):
        self._items = {}                      # товар -> количество

    def add(self, item, qty=1):
        self._items[item] = self._items.get(item, 0) + qty

    def __len__(self):                        # len(cart)
        return len(self._items)

    def __contains__(self, item):             # "apple" in cart
        return item in self._items

    def __getitem__(self, item):              # cart["apple"]
        return self._items[item]

    def __iter__(self):                       # for item, qty in cart
        return iter(self._items.items())

    def __bool__(self):                       # if cart:  (без него — по __len__)
        return bool(self._items)
```

- **Python ищет запасные варианты:** без `__contains__` оператор `in` переберёт `__iter__`;
  без `__iter__` — будет звать `__getitem__(0)`, `(1)`, … до IndexError; без `__bool__` —
  `__len__() != 0`.
- **`__getitem__` получает и срезы:** `cart[1:3]` придёт как `slice(1, 3)`.
- **Так ведут себя объекты-ответы в клиентах:** `response.json()`, `headers["X-Request-ID"]`.

---

### 6. `__call__` и контекстный менеджер

```python
class Multiplier:
    def __init__(self, k):
        self.k = k

    def __call__(self, x):                    # объект вызывается как функция
        return x * self.k

double = Multiplier(2)
print(double(5), callable(double))            # 10 True


class Timer:
    def __enter__(self):                      # with Timer() as t:  — вход
        self.start = time.perf_counter()
        return self                           # это попадёт в "as t"

    def __exit__(self, exc_type, exc, tb):    # выход — даже при исключении
        self.elapsed = time.perf_counter() - self.start
        return False                          # False — исключение не глотаем
```

- **`__call__`** — декоратор-класс (C6), объект-стратегия, фейк функции в тестах.
- **`__enter__`/`__exit__`** гарантируют «уборку» при любом выходе из блока: закрыть файл, откатить
  транзакцию, остановить браузер. Подробнее — урок C10. `__exit__`, вернувший `True`, проглотит
  исключение — почти всегда это баг.

---

### 7. `__new__` против `__init__`, метаклассы

```python
class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):        # создаёт объект (получает класс)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance                  # одиночка: всегда один и тот же объект

    def __init__(self, env="test"):           # заполняет объект (получает self)
        self.env = env

print(Config() is Config())                   # True
```

- **`__new__`** — создаёт и возвращает объект, первым аргументом получает класс. Нужен редко:
  синглтон, наследование от неизменяемых (`int`, `str`, `tuple`), кэш экземпляров.
- **`__init__`** — инициализирует уже созданный объект, ничего не возвращает. Вызывается, только
  если `__new__` вернул экземпляр этого класса.
- **Ловушка синглтона выше:** `__init__` выполняется при каждом `Config()` и перезаписывает `env`.
- **Метакласс одной фразой:** класс, экземплярами которого являются классы (`type` — метакласс по
  умолчанию); позволяет менять создание классов — так устроены ORM и ABC. В тестовом коде почти не
  нужен.

---

### 8. dataclass

```python
from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class Order:
    symbol: str
    side: str
    qty: int = 1
    price: Decimal = Decimal("0")
    tags: list[str] = field(default_factory=list)   # НЕ tags: list = []

    def __post_init__(self):                         # после сгенерированного __init__
        self.side = self.side.upper()
        if self.qty <= 0:
            raise ValueError("qty must be positive")

o = Order("BTC", "buy", qty=2)
print(o)                      # Order(symbol='BTC', side='BUY', qty=2, price=Decimal('0'), tags=[])
print(o == Order("BTC", "BUY", 2))   # True — __eq__ по полям
```

- **Генерирует:** `__init__`, `__repr__`, `__eq__` по полям в порядке объявления.
- **`field(default_factory=list)`** — изменяемые значения по умолчанию (иначе ValueError при
  объявлении: dataclass защищает от бага C1).
- **`frozen=True`** — поля нельзя менять, и появляется `__hash__` (можно в set). **`order=True`** —
  `<`, `>` по кортежу полей. **`slots=True`** — меньше памяти, нельзя добавлять атрибуты.
- **`__post_init__`** — валидация и нормализация.
- **`asdict(o)`** — в словарь (для тела запроса), `replace(o, qty=5)` — копия с изменением.

**dataclass против pydantic**

| | dataclass | pydantic |
|---|---|---|
| откуда | стандартная библиотека | внешняя библиотека |
| проверка типов | нет (`qty="2"` пройдёт) | да, при создании |
| преобразование | нет | `"2"` → `2`, строка → `Decimal`, `datetime` |
| JSON | `asdict` + `json.dumps` | `model_validate(json)`, `model_dump_json()` |
| когда в тестах | простые модели, тестовые данные | валидация ответов API по схеме |

---

**Частые ошибки.**
- `__eq__` без `__hash__` — объекты нельзя положить в set.
- `__hash__` по изменяемому полю — объект «теряется» в set после изменения.
- `return False` вместо `NotImplemented` в `__eq__` для чужих типов.
- `__repr__` возвращает не строку или печатает вместо возврата.
- В dataclass `tags: list = []` — ошибка при объявлении; нужно `field(default_factory=list)`.
- Ожидать, что dataclass проверит типы — не проверит.

---

### Собес

- **`__new__` против `__init__`.** `__new__` создаёт объект и возвращает его, получает класс;
  `__init__` заполняет уже созданный объект, получает `self` и ничего не возвращает. `__new__` нужен
  для синглтона и наследования от неизменяемых типов.
- **Что сломается, если переопределить `__eq__` без `__hash__`?** Python сделает `__hash__ = None`:
  объект станет нехешируемым, его нельзя положить в set или сделать ключом dict. Это защита
  инварианта «равные объекты — равные хеши». Решение — `__hash__` по тем же неизменяемым полям.
- **`__repr__` против `__str__`.** `__repr__` — для разработчика, однозначный, в идеале как код
  создания объекта, используется в коллекциях, отладке и отчётах pytest. `__str__` — для человека,
  его берёт `print`. Без `__str__` используется `__repr__`.
- **Зачем dataclass и чем он отличается от pydantic?** dataclass генерирует `__init__`, `__repr__`,
  `__eq__` по аннотациям — меньше шаблонного кода. Типы не проверяет. pydantic проверяет и
  преобразует данные при создании и умеет JSON — им валидируют ответы API.
- **Что такое метакласс, одной фразой?** Класс классов: он создаёт классы так же, как класс создаёт
  объекты; по умолчанию это `type`.

---

### Практика

Все команды — из папки `interview_prep/python_course/week3/c09_magic_methods`.

- **Упражнения «что выведет»:** `drills.py`. Проверка: `uv run python drills.py`.
- **Задачи** (условия на английском, тесты: `uv run pytest -k t01`):
  - обязательные: t01 `Vector`, t02 `Cart`, t03 `Version`, t04 dataclass `Order`, t05 хешируемый `Ticker`;
  - ★ t06 свой `Recorder` (mock).
