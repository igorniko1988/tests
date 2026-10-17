# F1. Урок 2 — наследование, композиция, `@property`, `@classmethod`, `@staticmethod`, dataclasses

Задачи к уроку: `practice/f1_02_inheritance.py`.

## 1. Наследование: «является»

Класс-наследник **получает** всё от родителя и может **добавить** своё или **переопределить**.

```python
class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(self.url)


class LoginPage(BasePage):           # LoginPage «является» страницей
    url = "/app/"

    def login(self, email, password):
        ...
```

`LoginPage` не пишет `__init__` и `open` — они достались от `BasePage`. Новое — только `url` и `login`.

### `super()` — вызвать метод родителя

```python
class DashboardPage(BasePage):
    url = "/app/"

    def __init__(self, page):
        super().__init__(page)                       # сначала то, что делает родитель
        self.toast = page.get_by_test_id("toast")    # потом своё
```

Без `super().__init__(page)` у объекта не появился бы `self.page` — родительский код просто не выполнился бы.

### Переопределение

Наследник может заменить метод родителя своим — с тем же именем. Тогда вызывается версия наследника.

## 2. Композиция: «содержит»

Объект **хранит внутри** другие объекты и пользуется ими.

```python
class OrdersTable:
    def __init__(self, page):
        self.rows = page.get_by_test_id("order-row")


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.orders = OrdersTable(page)      # страница СОДЕРЖИТ таблицу
```

**Правило:** наследование — когда «является» (`LoginPage` является страницей),
композиция — когда «содержит» (страница содержит таблицу, форму, тост).

**На практике чаще композиция:** её проще менять и переиспользовать.
Глубокие цепочки наследования (5 уровней) — антипаттерн: трудно понять, откуда взялся метод.

## 3. `@property` — метод, который читается как поле

```python
class Balance:
    def __init__(self, available, locked):
        self.available = available
        self.locked = locked

    @property
    def total(self):
        return self.available + self.locked


b = Balance(70, 30)
print(b.total)       # 100 — без скобок, как обычное поле
```

Зачем: значение **вычисляется** каждый раз из актуальных данных, а снаружи выглядит как поле.

Сеттер — контроль при записи:

```python
    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        if value < 0:
            raise ValueError("баланс не может быть отрицательным")
        self._available = value
```

`_available` с подчёркиванием — соглашение «внутреннее, снаружи не трогать».

## 4. `@classmethod` — альтернативный конструктор

Получает **класс** (`cls`), а не объект. Чаще всего — чтобы создать объект другим способом.

```python
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def from_dict(cls, data):
        return cls(data["email"], data["password"])


user = User.from_dict({"email": "a@b.com", "password": "secret123"})
```

`cls(...)` — то же, что `User(...)`. Вызывается **у класса**: `User.from_dict(...)`.

## 5. `@staticmethod` — функция внутри класса

Не получает ни `self`, ни `cls`. Это обычная функция, которая логически относится к классу.

```python
class User:
    @staticmethod
    def is_valid_email(email):
        return "@" in email


User.is_valid_email("a@b.com")       # True
```

| | первый параметр | зачем |
|---|---|---|
| обычный метод | `self` — объект | работать с данными объекта |
| `@classmethod` | `cls` — класс | альтернативный конструктор |
| `@staticmethod` | нет | вспомогательная функция «по теме» класса |

## 6. dataclasses — класс для данных без лишнего кода

```python
from dataclasses import dataclass, field


@dataclass
class Order:
    symbol: str
    side: str
    price: float
    quantity: float
    status: str = "NEW"                          # значение по умолчанию
    tags: list = field(default_factory=list)     # изменяемое — только так


order = Order("ETH-USDT", "BUY", 2, 3)
print(order)                  # Order(symbol='ETH-USDT', side='BUY', price=2, ...)
print(order == Order("ETH-USDT", "BUY", 2, 3))   # True — сравнение по полям
```

`@dataclass` сам пишет `__init__`, `__repr__` (красивый вывод) и `__eq__` (сравнение по полям).

- `field(default_factory=list)` — у каждого объекта **свой** список (вспомни ловушку из урока 1).
- `@dataclass(frozen=True)` — объект нельзя изменить после создания.

**dataclass vs Pydantic:** dataclass **не проверяет типы** — `Order("ETH", "BUY", "дорого", 3)` создастся.
Pydantic проверяет и приводит типы. Поэтому для ответов API — Pydantic, для простых тестовых данных — dataclass.

## Шпаргалка

| Что | Когда |
|---|---|
| наследование `class B(A)` | B «является» A, общая логика в родителе |
| `super().__init__(...)` | выполнить инициализацию родителя |
| композиция `self.x = X()` | объект «содержит» другой |
| `@property` | вычисляемое поле / контроль записи |
| `@classmethod` | альтернативный конструктор `from_...` |
| `@staticmethod` | вспомогательная функция по теме класса |
| `@dataclass` | класс-контейнер для данных |

## Вопросы собеседования

1. Чем наследование отличается от композиции? Что выбираешь чаще и почему?
2. Зачем `super()`? Что будет, если не вызвать `super().__init__()`?
3. Зачем `@property`, если можно сделать обычный метод?
4. Чем `@classmethod` отличается от `@staticmethod`? Пример, когда нужен каждый.
5. Что даёт `@dataclass`? Чем dataclass отличается от Pydantic-модели?
