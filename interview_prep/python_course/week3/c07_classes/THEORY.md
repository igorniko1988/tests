# C7 · Классы и объекты

**Смысл темы.** Класс — чертёж, по которому создаются объекты: он описывает, какие данные
(атрибуты) есть у объекта и что объект умеет (методы). В тестовом фреймворке на классах построено
всё: API-клиент, Page Object, модели данных ответа. На собесе спрашивают не синтаксис, а
понимание: что такое `self`, где живут атрибуты класса и объекта, зачем `@property`, чем
`classmethod` отличается от `staticmethod` и есть ли в Python private.

---

### 1. Класс, объект, `self`

```python
class Order:
    def __init__(self, symbol, qty):     # вызывается при создании объекта
        self.symbol = symbol             # атрибут ОБЪЕКТА
        self.qty = qty

    def total(self, price):              # метод: первый параметр — сам объект
        return self.qty * price

order = Order("BTC", 2)                  # Order.__init__(order, "BTC", 2)
print(order.symbol, order.total(100))    # BTC 200
print(Order.total(order, 100))           # 200 — то же самое, self передали явно
```

- **`self` — просто первый параметр метода,** в него Python подставляет объект, у которого метод
  вызвали: `order.total(100)` превращается в `Order.total(order, 100)`. Имя `self` — соглашение.
- **`__init__` — не конструктор, а инициализатор:** объект уже создан (это делает `__new__`, C9),
  `__init__` только заполняет его атрибуты. Он ничего не возвращает.
- **Атрибуты можно добавить в любой момент:** `order.note = "x"` создаст новый атрибут только у
  этого объекта. Опечатка `order.qyt = 5` тоже молча создаст атрибут — классика багов.
- **Забыть `self`:** `def total(price)` → вызов `order.total(100)` даст TypeError: takes 1
  positional argument but 2 were given (объект пришёл в `price`, а 100 — лишний).

---

### 2. Атрибут класса и атрибут объекта

```python
class Client:
    base_url = "http://localhost:8080"     # атрибут КЛАССА — общий для всех объектов
    created = 0

    def __init__(self, token):
        self.token = token                 # атрибут ОБЪЕКТА — у каждого свой
        Client.created += 1                # меняем атрибут класса явно через класс

a, b = Client("t1"), Client("t2")
print(a.base_url, Client.created)          # http://localhost:8080 2

a.base_url = "http://stage"                # создали атрибут ОБЪЕКТА a, класс не тронут
print(a.base_url, b.base_url)              # http://stage http://localhost:8080
```

**Как Python ищет `obj.attr`:** сначала в словаре объекта `obj.__dict__`, потом в классе
`type(obj).__dict__`, потом в родителях (MRO, C8).

```
a.__dict__      = {'token': 't1', 'base_url': 'http://stage'}  ← нашли здесь
Client.__dict__ = {'base_url': 'http://localhost:8080', 'created': 2, ...}
b.__dict__      = {'token': 't2'}  → base_url ищется дальше, в классе
```

**Главная ловушка — изменяемый атрибут класса:**

```python
class Cart:
    items = []                  # ОДИН список на все корзины!

    def add(self, item):
        self.items.append(item) # self.items нашёлся в классе — меняем общий список

c1, c2 = Cart(), Cart()
c1.add("apple")
print(c2.items)                 # ['apple'] — чужая корзина «испачкалась»
```

- **Чинят так:** изменяемые значения создавать в `__init__`: `self.items = []`.
- **Присваивание создаёт атрибут объекта, а `append` меняет найденный:** `self.items = [...]`
  затенит атрибут класса, а `self.items.append(...)` изменит общий список.
- **В тестах:** общий список заголовков/кук в атрибуте класса клиента — тесты «текут» друг в друга.
- **Атрибуты класса хороши для констант:** `TIMEOUT = 5`, `ENDPOINT = "/orders"`, счётчики.

---

### 3. `@property`: метод, который читается как поле

```python
class User:
    def __init__(self, email):
        self.email = email               # пойдёт через setter — валидация и тут

    @property
    def email(self):                     # getter: user.email
        return self._email

    @email.setter
    def email(self, value):              # setter: user.email = "..."
        if "@" not in value:
            raise ValueError(f"bad email: {value!r}")
        self._email = value.strip().lower()

    @property
    def domain(self):                    # вычисляемое поле только для чтения
        return self._email.split("@")[1]

u = User(" Ann@Mail.com ")
print(u.email, u.domain)                 # ann@mail.com mail.com
u.email = "oops"                         # ValueError
u.domain = "x"                           # AttributeError: property has no setter
```

- **Зачем:** снаружи — простой атрибут, внутри — проверка, преобразование или вычисление. Можно
  начать с обычного атрибута, а потом сделать property, не меняя вызывающий код.
- **Данные хранятся в `self._email`** (с подчёркиванием). Если в getter написать `return self.email`,
  он вызовет сам себя — RecursionError.
- **Только для чтения:** property без setter — защита от случайной записи (`money.amount = ...`).
- **Вычисляемые поля:** `full_name`, `total`, `is_expired` — не хранятся, считаются при обращении.

---

### 4. `@classmethod` и `@staticmethod`

```python
class Order:
    def __init__(self, symbol, qty, price):
        self.symbol, self.qty, self.price = symbol, qty, price

    @classmethod
    def from_json(cls, data):            # альтернативный конструктор
        return cls(data["symbol"], int(data["qty"]), Decimal(data["price"]))

    @staticmethod
    def is_valid_symbol(symbol):         # обычная функция, «живущая» в классе
        return "/" in symbol

order = Order.from_json({"symbol": "BTC/USDT", "qty": "2", "price": "10.5"})
Order.is_valid_symbol("BTC")             # False
```

| | первый параметр | доступ | когда |
|---|---|---|---|
| обычный метод | `self` — объект | к объекту и классу | работа с данными объекта |
| `@classmethod` | `cls` — класс | к классу | альтернативные конструкторы, фабрики |
| `@staticmethod` | нет | ни к чему | утилита по смыслу класса |

- **`cls`, а не имя класса:** `cls(...)` в наследнике создаст объект наследника. `Order(...)`
  внутри создал бы всегда `Order`.
- **Альтернативные конструкторы** — главный случай classmethod: `from_json`, `from_env`,
  `datetime.fromisoformat`, `dict.fromkeys`.
- **staticmethod** можно вынести в модуль как функцию — его держат в классе только ради смысла.

---

### 5. «Приватность»: `_protected` и `__private`

```python
class Account:
    def __init__(self):
        self._balance = 0          # «не трогай снаружи» — соглашение
        self.__pin = "1234"        # name mangling: хранится как _Account__pin

a = Account()
print(a._balance)                  # 0 — доступ есть, это просто договорённость
print(a.__pin)                     # AttributeError
print(a._Account__pin)             # 1234 — «спрятано», но не защищено
```

- **В Python нет настоящего private.** `_name` — «внутреннее, используй на свой риск»;
  линтеры и IDE предупредят.
- **`__name`** переименовывается в `_Класс__name`. Цель — не секретность, а защита от случайного
  перекрытия атрибута в наследнике (C8).
- **Ответ на собесе:** «Приватности нет, есть соглашения: одно подчёркивание — внутреннее API,
  два — name mangling против конфликтов при наследовании».

---

### 6. Ленивый атрибут и `functools.cached_property`

```python
from functools import cached_property

class Report:
    def __init__(self, rows):
        self.rows = rows

    @cached_property
    def total(self):               # считается один раз при первом обращении
        print("computing")
        return sum(r["amount"] for r in self.rows)

r = Report([{"amount": 5}, {"amount": 7}])
print(r.total, r.total)            # computing | 12 12
```

- **Как работает:** при первом обращении результат кладётся в `r.__dict__["total"]`, и дальше
  Python находит его там, не вызывая метод.
- **Подвох:** если `rows` изменятся, `total` останется старым. Сбросить — `del r.total`.
- **В тестах:** дорогой токен авторизации, тяжёлая выборка — получить один раз на объект.

---

### 7. Классы в автотестах

```python
class OrdersClient:
    ENDPOINT = "/orders"                       # константа — атрибут класса

    def __init__(self, session, base_url):
        self.session = session                 # состояние — атрибуты объекта
        self.base_url = base_url

    def create(self, **body):
        return self.session.post(self.base_url + self.ENDPOINT, json=body)

    def get(self, order_id):
        return self.session.get(f"{self.base_url}{self.ENDPOINT}/{order_id}")
```

- **Состояние — в объекте, константы — в классе.** Сессии, токены, списки созданного — только в
  `__init__`, иначе тесты делят состояние.
- **Модель ответа:** `Order.from_json(resp.json())` — один раз распарсить, дальше работать с
  полями, а не со словарём (опечатку в ключе словаря IDE не поймает, в атрибуте — поймает).
- **Page Object** — класс страницы с локаторами и действиями (UI-курс), API-клиент — класс с методами
  эндпоинтов.

---

**Частые ошибки.**
- Изменяемое значение в атрибуте класса (`items = []`) — общее для всех объектов.
- `def method(arg)` без `self`.
- Getter property возвращает `self.x` вместо `self._x` — рекурсия.
- В classmethod создают `ИмяКласса(...)` вместо `cls(...)` — наследники ломаются.
- Опечатка в имени атрибута при присваивании молча создаёт новый атрибут.
- Вызов `Order.total(100)` у класса вместо объекта — нет `self`.

---

### Собес

- **Чем атрибут класса отличается от атрибута объекта?** Атрибут класса один на класс и виден из
  всех объектов; атрибут объекта лежит в `obj.__dict__` и у каждого свой. Чтение ищет сначала в
  объекте, потом в классе. Присваивание через объект создаёт атрибут объекта. Опасно хранить в
  классе изменяемое значение — его меняют все объекты.
- **classmethod против staticmethod.** classmethod получает класс (`cls`) — для альтернативных
  конструкторов и фабрик, корректно работает с наследниками. staticmethod не получает ничего —
  обычная функция в пространстве имён класса.
- **Зачем `@property`?** Чтобы атрибут выглядел как поле, а внутри была логика: валидация в
  setter, вычисление, запрет записи. Позволяет поменять реализацию, не меняя интерфейс.
- **Есть ли в Python private?** Нет. `_x` — соглашение «внутреннее», `__x` — name mangling в
  `_Class__x`, чтобы наследник случайно не перекрыл атрибут. Доступ всё равно возможен.
- **Что такое `self`?** Первый параметр метода — объект, у которого вызвали метод. `obj.m(1)` —
  это `Class.m(obj, 1)`. Через `self` метод читает и меняет данные своего объекта.

---

### Практика

Все команды — из папки `interview_prep/python_course/week3/c07_classes`.

- **Упражнения «что выведет»:** `drills.py`. Проверка: `uv run python drills.py`.
- **Задачи** (условия на английском, тесты: `uv run pytest -k t01`):
  - обязательные: t01 `User`, t02 `Order.from_json`, t03 счётчик объектов, t04 найди баг, t05 `Money`;
  - ★ t06 ленивый атрибут.
