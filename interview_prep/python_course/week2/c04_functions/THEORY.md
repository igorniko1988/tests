# C4 · Функции и области видимости

**Смысл темы.** Функция в Python — обычный объект, как число или список: её можно положить в
переменную, передать в другую функцию, вернуть из функции и даже хранить в словаре. На этом
держится всё, что будет дальше: декораторы (C6), фикстуры pytest, `key=` в сортировке, колбэки
и фабрики тестовых данных. В уроке разбираем виды аргументов (`*args`, `**kwargs`, `*`, `/`),
как Python ищет переменную по имени (LEGB), что такое замыкание и почему лямбды в цикле
ведут себя «странно».

---

### 1. Функция — это объект

Строка `def greet(...)` делает две вещи: создаёт объект-функцию и привязывает к нему имя
`greet` — так же, как `x = 5` привязывает имя к числу.

```python
def greet(name):
    return f"Hello, {name}"

say = greet                 # второе имя на ТОТ ЖЕ объект, скобок нет — это не вызов
print(say("Ann"))           # Hello, Ann
print(greet.__name__)       # greet — имя, данное при def
print(type(greet))          # <class 'function'>

handlers = {"hello": greet, "upper": str.upper}   # функции — значения словаря
print(handlers["upper"]("abc"))                   # ABC


def apply(func, value):     # функция принимает функцию
    return func(value)

print(apply(len, "abcd"))   # 4
```

- **`greet` без скобок — объект, `greet()` — вызов:** самая частая ошибка новичка —
  `button.on_click(handler())` вместо `handler`: функция вызывается сразу, а передаётся её результат.
- **Функции высшего порядка:** принимают или возвращают функции — `sorted(key=...)`, `map`,
  `filter`, декораторы.
- **В тестах:** `pytest.raises(ValueError)` принимает класс, `parametrize` — данные, а
  `page.wait_for_function(...)` или свой `wait_until(condition)` (Q2) — функцию-условие.

---

### 2. Параметры и аргументы

**Параметр** — имя в сигнатуре `def f(a, b)`. **Аргумент** — значение, переданное при вызове
`f(1, b=2)`.

```python
def create_order(symbol, side, qty=1, price=None):
    return {"symbol": symbol, "side": side, "qty": qty, "price": price}

create_order("BTC", "BUY")                    # позиционно; qty и price — по умолчанию
create_order("BTC", side="SELL", qty=3)       # смешанно: позиционные ПЕРЕД именованными
create_order(side="BUY", symbol="ETH")        # все по имени — порядок любой
create_order(side="BUY", "ETH")               # SyntaxError: позиционный после именованного
create_order("BTC", "BUY", side="SELL")       # TypeError: got multiple values for argument 'side'
```

- **Позиционные идут первыми:** после первого `name=value` позиционных быть не может.
- **Значение по умолчанию вычисляется один раз** — при выполнении `def`. Поэтому изменяемое
  значение (`[]`, `{}`) по умолчанию делится между вызовами — это C1, раздел 7. Правильно:
  `def f(tags=None): if tags is None: tags = []`.
- **Параметры со значением по умолчанию — после обязательных:** `def f(a=1, b)` — SyntaxError.

---

### 3. `*args` и `**kwargs`

Звёздочка в **сигнатуре** собирает «лишние» аргументы:

```python
def log(*args, **kwargs):
    print(args, kwargs)

log(1, 2, x=3)          # (1, 2) {'x': 3}
log()                   # () {}
```

- **`*args`** — все лишние позиционные аргументы в **кортеж** (даже если один — `(1,)`).
- **`**kwargs`** — все лишние именованные в **словарь**.
- **Имена `args` и `kwargs` — соглашение,** важны только звёздочки: `*values`, `**params`.

Звёздочка при **вызове** — наоборот, раскладывает коллекцию в аргументы:

```python
def point(x, y):
    return f"({x}, {y})"

coords = [3, 4]
opts = {"x": 1, "y": 2}
print(point(*coords))       # (3, 4)   — то же, что point(3, 4)
print(point(**opts))        # (1, 2)   — то же, что point(x=1, y=2)
```

**Главное применение — обёртка, которая передаёт всё дальше, ничего не зная о сигнатуре:**

```python
def call_and_log(func, *args, **kwargs):
    print(f"call {func.__name__} args={args} kwargs={kwargs}")
    return func(*args, **kwargs)        # прокинули ровно то, что получили

call_and_log(create_order, "BTC", "BUY", qty=2)
```

- **Порядок в сигнатуре:** `def f(a, b=1, *args, c, d=2, **kwargs)` — обычные → `*args` →
  только именованные → `**kwargs`.
- **В тестах:** API-клиент `def post(self, path, **kwargs): return self.session.post(self.base + path, **kwargs)`
  прокидывает `json=`, `headers=`, `timeout=` в requests без перечисления.

---

### 4. Только именованные (`*`) и только позиционные (`/`)

```python
def get(url, *, timeout=5, retries=0):   # всё после * — только по имени
    ...

get("/orders", timeout=10)    # ✓
get("/orders", 10)            # TypeError: takes 1 positional argument but 2 were given


def distance(x, y, /):        # всё до / — только позиционно
    ...

distance(1, 2)                # ✓
distance(x=1, y=2)            # TypeError: got some positional-only arguments passed as keyword
```

- **`*` без имени** — граница: дальше только `name=value`. Защищает от `get("/x", 10, 3)`,
  где через полгода никто не помнит, что такое 10 и 3.
- **`/`** — имена параметров не входят в API функции, их можно переименовать без поломки
  вызывающего кода. Так устроены многие встроенные: `len(obj, /)`.
- **На собесе** спрашивают, зачем `*` в `def request(method, url, *, timeout)` — ответ: явность
  и защита от перепутанных позиционных аргументов.

---

### 5. Области видимости: LEGB

Когда Python встречает имя, он ищет его по очереди в четырёх местах:

```
L — Local      внутри текущей функции
E — Enclosing  в объемлющих функциях (если функция вложенная)
G — Global     на уровне модуля (файла)
B — Built-in   встроенные: len, print, id, list ...
```

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)        # local — нашли в L
    inner()

def outer2():
    x = "enclosing"
    def inner():
        print(x)        # enclosing — в L нет, нашли в E
    inner()

outer()
outer2()
print(len)              # <built-in function len> — дошли до B
```

**Правило, которое ломает всех:** если внутри функции есть **присваивание** имени (`x = ...`,
`x += ...`, `for x in`, `import x`), то это имя **локальное во всей функции** — даже в строках
ДО присваивания. Python решает это при компиляции функции, а не по ходу выполнения.

```python
count = 0

def bump():
    count += 1          # UnboundLocalError: cannot access local variable 'count'
                        # where it is not associated with a value
```

Здесь `count += 1` — присваивание, значит `count` локальная, а прочитать её до присваивания
нельзя. Два способа явно сказать «это не локальная»:

```python
count = 0

def bump():
    global count        # имя из модуля
    count += 1


def make_counter():
    n = 0
    def inc():
        nonlocal n      # имя из объемлющей функции
        n += 1
        return n
    return inc
```

- **`global`** — переменная модуля. В тестовом коде почти всегда признак плохого дизайна:
  тесты начинают зависеть друг от друга через общее состояние.
- **`nonlocal`** — переменная ближайшей объемлющей функции. Нужна в замыканиях (раздел 6).
- **Чтение без `global` работает:** `print(count)` внутри функции найдёт глобальную —
  проблемы начинаются только с присваиванием.
- **Изменение объекта — не присваивание:** `items.append(1)` внутри функции не делает `items`
  локальной, `global` не нужен.

---

### 6. Замыкание

**Замыкание** — вложенная функция, которая запоминает переменные объемлющей функции и
пользуется ими **после того, как объемлющая уже завершилась**.

```python
def make_counter(start=0):
    n = start                  # живёт после выхода из make_counter
    def counter():
        nonlocal n
        n += 1
        return n
    return counter             # возвращаем функцию, НЕ вызывая её

c1 = make_counter()
c2 = make_counter(100)
print(c1(), c1(), c2(), c1())  # 1 2 101 3
```

```
make_counter() вызван дважды → две независимые «ячейки» n

c1 ──▶ counter ──▶ ячейка n = 2
c2 ──▶ counter ──▶ ячейка n = 101
```

- **Как это хранится:** у функции есть `__closure__` — кортеж «ячеек» (cell) с захваченными
  переменными: `c1.__closure__[0].cell_contents` → `2`.
- **Каждый вызов внешней функции — новая ячейка,** поэтому `c1` и `c2` не мешают друг другу.
- **Замыкание захватывает переменную, а не значение:** если переменная потом изменится,
  функция увидит новое значение. Отсюда раздел 7.
- **Зачем:** состояние без класса (счётчики, кэш), фабрики функций, и главное — **декораторы**
  (C6): обёртка помнит исходную функцию через замыкание.
- **В pytest:** «фабрика как фикстура» — фикстура возвращает функцию `make_user(**overrides)`,
  которая помнит общие настройки и список созданного для teardown.

---

### 7. Позднее связывание: лямбды в цикле

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])     # [2, 2, 2], а не [0, 1, 2]
```

Каждая лямбда помнит **переменную** `i`, а не её значение в момент создания. Значение берётся
при **вызове** — а к этому времени цикл закончился и `i == 2`. Это называется поздним
связыванием (late binding).

Два стандартных способа починить:

```python
# 1) значение по умолчанию вычисляется в момент создания функции
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])     # [0, 1, 2]

# 2) functools.partial фиксирует аргумент сразу
from functools import partial

def identity(x):
    return x

funcs = [partial(identity, i) for i in range(3)]
print([f() for f in funcs])     # [0, 1, 2]
```

- **Трюк `i=i`:** слева — имя параметра лямбды, справа — текущее значение переменной цикла.
  Значения по умолчанию вычисляются при создании функции (раздел 2) — ровно то, что нужно.
- **Та же ловушка без лямбд:** `def` внутри цикла ведёт себя так же.
- **В тестах:** список колбэков или параметров, собранный в цикле, внезапно «видит» только
  последний элемент.

---

### 8. lambda и функции-ключи

`lambda` — короткая безымянная функция из **одного выражения**:

```python
square = lambda x: x * x            # то же, что def square(x): return x * x
print(square(4))                    # 16

orders = [{"id": 2, "price": "10.5"}, {"id": 1, "price": "9"}]
by_id = sorted(orders, key=lambda o: o["id"])
cheapest = min(orders, key=lambda o: Decimal(o["price"]))
```

- **Только выражение:** внутри нельзя `if` как оператор, `for`, присваивание. Можно тернарный
  `a if cond else b`.
- **Когда лучше `def`:** если лямбда не помещается в строку или её надо переиспользовать —
  дай имя через `def` (PEP 8 не советует `name = lambda ...`).
- **`operator` вместо простых лямбд:** `itemgetter("id")` = `lambda o: o["id"]`,
  `attrgetter("price")` = `lambda o: o.price`, `itemgetter("a", "b")` возвращает кортеж.
- **`key` вызывается один раз на элемент** — дорогой `key` (парсинг даты) не страшен.

---

### 9. functools: partial, cache, reduce

```python
from functools import cache, lru_cache, partial, reduce

def request(method, path, *, timeout=5):
    return f"{method} {path} timeout={timeout}"

get = partial(request, "GET")               # «заморозили» первый аргумент
slow_get = partial(request, "GET", timeout=30)
print(get("/orders"))                       # GET /orders timeout=5
print(slow_get("/report"))                  # GET /report timeout=30
print(get.func.__name__, get.args, get.keywords)   # request ('GET',) {}


@cache                                      # безлимитный кэш по аргументам
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))                              # мгновенно, без кэша — годы

print(reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1))   # 24
```

- **`partial(func, *args, **kwargs)`** возвращает новый вызываемый объект с частью аргументов
  заранее. Вызов `get("/x")` = `request("GET", "/x")`.
- **`@cache` / `@lru_cache(maxsize=128)`** запоминают результат по аргументам. Аргументы должны
  быть хешируемыми (C1): `fib([1])` — TypeError. `lru_cache` вытесняет давно не использованное.
- **`reduce`** сворачивает последовательность в одно значение. В Python чаще пишут цикл или
  `sum`/`math.prod` — так понятнее.
- **`wraps`** — для декораторов, подробно в C6.

---

### 10. Функции в автотестах

```python
# 1) фабрика данных: замыкание помнит счётчик и список созданного
def make_user_factory():
    created = []
    counter = 0
    def make_user(**overrides):
        nonlocal counter
        counter += 1
        user = {"email": f"user{counter}@test.io", "password": "secret", **overrides}
        created.append(user)
        return user
    make_user.created = created          # функции можно вешать атрибуты
    return make_user


# 2) ожидание условия: передаём функцию-проверку, а не результат
def wait_until(condition, timeout=5.0, interval=0.1):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return True
        time.sleep(interval)
    raise TimeoutError("condition not met")

wait_until(lambda: client.get_order(order_id)["status"] == "FILLED")
```

- **Фабрика вместо набора одинаковых фикстур:** `make_user(role="admin")` — один механизм на все
  варианты. В pytest её возвращает фикстура, а teardown удаляет всё из `created`.
- **Колбэк-условие:** `wait_until(lambda: ...)` — лямбда вызывается заново на каждой итерации.
  Передать `client.get_order(...)["status"] == "FILLED"` без лямбды — значит проверить один раз.
- **`partial` для клиентов:** `get_user = partial(api.request, "GET", "users")` — меньше
  повторов в тестах.

---

**Частые ошибки.**
- `button.on_click(handler())` — функция вызвана сразу; нужно `handler` без скобок.
- `count += 1` внутри функции без `global`/`nonlocal` → `UnboundLocalError`.
- Лямбды/функции в цикле видят последнее значение переменной цикла.
- `def f(items=[])` — общий список между вызовами (C1).
- `@cache` на функции с аргументом-списком → `TypeError: unhashable type: 'list'`.
- `**kwargs` перехватывает опечатку: `create(qyt=3)` молча попадёт в kwargs вместо ошибки.

---

### Собес

- **Что такое `*args` и `**kwargs`?** В сигнатуре `*args` собирает лишние позиционные аргументы
  в кортеж, `**kwargs` — именованные в словарь. При вызове звёздочки наоборот раскладывают
  коллекцию в аргументы. Главное применение — обёртки и клиенты, которые прокидывают аргументы
  дальше, не зная сигнатуры: `return func(*args, **kwargs)`.
- **Что такое замыкание? Приведи пример.** Вложенная функция, которая использует переменные
  объемлющей функции и сохраняет их после её завершения. Пример — счётчик: `make_counter`
  создаёт `n = 0` и возвращает `inc`, который делает `nonlocal n; n += 1`. Каждый вызов
  `make_counter` даёт независимую ячейку. На замыканиях построены декораторы.
- **Как Python ищет имя (LEGB)?** Local → Enclosing → Global → Built-in, до первого совпадения.
  Важная деталь: если в функции есть присваивание имени, оно локальное во всей функции, поэтому
  чтение до присваивания даёт `UnboundLocalError`.
- **Зачем `nonlocal` и `global`?** Чтобы присваивать имени из внешней области, а не создавать
  локальное. `global` — переменная модуля (в тестах почти всегда плохо: общее состояние),
  `nonlocal` — переменная объемлющей функции (замыкания, счётчики).
- **Что выведет список лямбд из цикла и как починить?** `[lambda: i for i in range(3)]` при
  вызове даст `2, 2, 2`: лямбды захватывают переменную, а значение берут при вызове. Чинят
  значением по умолчанию `lambda i=i: i` или `functools.partial`.
- **Что делает `functools.partial`?** Возвращает вызываемый объект, у которого часть аргументов
  уже подставлена: `get = partial(request, "GET")`. Удобно для колбэков и клиентов.
- **Зачем `*` в `def get(url, *, timeout)`?** Всё после `*` передаётся только по имени: вызов
  `get(url, 10)` упадёт. Это делает вызовы явными и защищает от перепутанных позиционных аргументов.

---

### Практика

Все команды — из папки `interview_prep/python_course/week2/c04_functions`.

- **Упражнения «что выведет»:** `drills.py`. Проверка: `uv run python drills.py`.
- **Задачи** (условия на английском, тесты: `uv run pytest -k t01`):
  - обязательные: t01 `make_counter`, t02 `call_logger`, t03 `make_multipliers`, t04 `sort_by`, t05 `build_client`;
  - ★ t06 `memoize`.
