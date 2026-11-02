# C8 · Наследование и проектирование

**Смысл темы.** Наследование — способ сказать «этот класс такой же, как тот, но…»: дочерний класс
получает атрибуты и методы родителя и может их дополнить или заменить. На собесе по этой теме
спрашивают четыре принципа ООП, `super()` и MRO (особенно «ромб»), абстрактные классы, «когда
композиция лучше наследования» и SOLID — обычно на примере своего фреймворка: BaseClient и клиенты
эндпоинтов, BasePage и страницы, компоненты страницы.

---

### 1. Четыре принципа ООП на примере фреймворка

- **Инкапсуляция** — данные и работа с ними в одном объекте, детали скрыты: клиент сам хранит
  сессию и токен, тест вызывает `orders.create(...)` и не знает про заголовки.
- **Наследование** — общий код в родителе: `BaseClient.request()` с логированием и ретраями,
  `UsersClient` и `OrdersClient` его наследуют.
- **Полиморфизм** — один интерфейс, разное поведение: у всех страниц есть `open()`, каждая
  открывает свой URL; код, который вызывает `page.open()`, не знает, какая это страница.
- **Абстракция** — выделить существенное и спрятать остальное: `BasePage` с абстрактным `open()`
  описывает «что такое страница», не говоря, как именно она открывается.

---

### 2. Наследование и переопределение

```python
class BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def headers(self):
        return {"Accept": "application/json"}

    def url(self, path):
        return self.base_url + path


class OrdersClient(BaseClient):            # в скобках — родитель
    def headers(self):                     # переопределили метод
        return {**super().headers(), "X-Client": "orders"}   # и расширили родительский

c = OrdersClient("http://localhost:8080")
print(c.url("/orders"))                    # метод родителя — унаследован
print(c.headers())                         # {'Accept': 'application/json', 'X-Client': 'orders'}
print(isinstance(c, BaseClient), issubclass(OrdersClient, BaseClient))   # True True
```

- **Поиск метода:** сначала в классе объекта, потом в родителе, потом выше — до `object`.
- **Переопределение** заменяет метод целиком; `super().method()` позволяет **дополнить**, а не
  переписать родительское поведение.
- **`isinstance(obj, Base)`** — True и для наследников. Это и есть полиморфизм на проверках типов.

---

### 3. `super()` и `__init__` наследника

```python
class AuthClient(BaseClient):
    def __init__(self, base_url, token):
        super().__init__(base_url)          # родитель заполнит self.base_url
        self.token = token                  # своё — после

    def headers(self):
        return {**super().headers(), "Authorization": f"Bearer {self.token}"}
```

- **Забыть `super().__init__`** — у объекта не будет атрибутов родителя: `AttributeError: 'AuthClient'
  object has no attribute 'base_url'`.
- **Если `__init__` у наследника не написан,** берётся родительский — ничего вызывать не надо.
- **`super()` — не «родитель», а «следующий по MRO»** (раздел 4). При одиночном наследовании это
  одно и то же, при множественном — нет.

---

### 4. MRO и «ромб»

**MRO (Method Resolution Order)** — порядок, в котором Python ищет атрибут по классам.

```python
class A:
    def hello(self):
        return ["A"]

class B(A):
    def hello(self):
        return ["B"] + super().hello()

class C(A):
    def hello(self):
        return ["C"] + super().hello()

class D(B, C):
    def hello(self):
        return ["D"] + super().hello()

print([k.__name__ for k in D.__mro__])   # ['D', 'B', 'C', 'A', 'object']
print(D().hello())                       # ['D', 'B', 'C', 'A']
```

```
        A
       / \
      B   C        «ромб»: D наследует A двумя путями
       \ /
        D
```

- **Порядок MRO (алгоритм C3):** класс, затем родители слева направо из `class D(B, C)`, при этом
  каждый класс идёт раньше своих родителей, а общий предок (`A`) — один раз и в конце.
- **`super()` в `B` вызывает `C`, а не `A`!** Следующий после `B` в MRO **объекта** `D` — это `C`.
  Так каждый метод в ромбе вызывается ровно один раз.
- **Проблема ромба** в других языках — неясно, чью версию взять и не вызвать ли `A` дважды.
  В Python её решают MRO и кооперативный `super()`: все классы цепочки зовут `super()`.
- **Посмотреть порядок:** `D.__mro__` или `D.mro()`.

---

### 5. Абстрактные классы

```python
from abc import ABC, abstractmethod

class BasePage(ABC):
    def __init__(self, browser):
        self.browser = browser

    @property
    @abstractmethod
    def path(self): ...                  # наследник обязан задать

    def open(self):                      # общий код — один раз
        self.browser.goto(self.path)
        return self

class LoginPage(BasePage):
    path = "/app/login.html"

BasePage(browser)       # TypeError: Can't instantiate abstract class BasePage ...
LoginPage(browser)      # ✓
```

- **`ABC` + `@abstractmethod`** — «контракт»: нельзя создать объект класса, у которого остались
  нереализованные абстрактные методы. Ошибка видна при создании, а не в середине теста.
- **Template method:** общий алгоритм (`open`) в базе, шаги, которые отличаются (`path`), — в
  наследниках.
- **Без ABC** часто пишут `raise NotImplementedError` в методе базы — ошибка всплывёт только при
  вызове.

---

### 6. Утиная типизация и Protocol

«Если ходит как утка и крякает как утка — это утка»: Python проверяет не тип, а наличие нужных
методов в момент вызова.

```python
class FakeSession:                        # не наследует requests.Session
    def __init__(self):
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url))
        return {"status": 200}

client = OrdersClient("http://x", session=FakeSession())   # работает: есть .request
```

```python
from typing import Protocol

class Session(Protocol):
    def request(self, method: str, url: str, **kwargs): ...

def make_client(session: Session): ...    # mypy проверит наличие метода, наследовать не нужно
```

- **Главная польза в тестах:** подменить настоящую сессию/браузер фейком без наследования.
- **`Protocol`** — описание «утки» для статической проверки типов (mypy, IDE), в рантайме ничего
  не делает.

---

### 7. Композиция против наследования

```python
class Header:
    def __init__(self, browser):
        self.browser = browser

    def logout(self):
        self.browser.click("[data-testid=logout]")

class OrderForm:
    def __init__(self, browser):
        self.browser = browser

    def submit(self, qty):
        self.browser.fill("[data-testid=qty]", str(qty))
        self.browser.click("[data-testid=submit]")

class DashboardPage:                      # ИМЕЕТ шапку и форму, а не ЯВЛЯЕТСЯ ими
    def __init__(self, browser):
        self.header = Header(browser)
        self.order_form = OrderForm(browser)
```

- **Наследование — «является»** (`AuthClient` — это `BaseClient`). **Композиция — «имеет»**
  (страница имеет шапку и форму).
- **Почему композиция чаще лучше:** части переиспользуются на разных страницах, меньше связность,
  нет глубоких иерархий, где непонятно, откуда метод. Правило: «предпочитай композицию наследованию».
- **Наследование оправдано** для общего поведения одного вида объектов: базовый клиент, базовая
  страница.

---

### 8. Mixin

```python
class LoggingMixin:
    def request(self, method, path, **kwargs):
        self.log.append(f"{method} {path}")
        return super().request(method, path, **kwargs)     # дальше по MRO

class LoggedOrdersClient(LoggingMixin, OrdersClient):      # mixin — слева
    pass
```

- **Mixin** — маленький класс с одной добавкой поведения, сам по себе не используется.
- **Ставится левее основного класса,** чтобы его метод был раньше в MRO, а `super()` передал
  вызов дальше — основному классу.

---

### 9. SOLID на примере фреймворка

- **S — Single responsibility:** у класса одна причина меняться. Клиент шлёт запросы, генератор
  данных создаёт данные, проверки — в тестах/хелперах. «Божественный» `OrderManager`, который и
  валидирует, и ходит в API, и форматирует отчёт, — нарушение.
- **O — Open/closed:** расширяем без правки существующего: новый эндпоинт — новый класс-клиент,
  а не `if` в базовом.
- **L — Liskov substitution:** наследник подходит везде, где ждут родителя. `ReadOnlyClient`,
  который бросает исключение на `post`, ломает код, ожидающий `BaseClient`.
- **I — Interface segregation:** маленькие интерфейсы. Странице поиска не нужен метод `upload_file`
  из общего «толстого» `BasePage`.
- **D — Dependency inversion:** зависеть от абстракций и получать зависимости снаружи: клиент
  принимает `session` в конструкторе — в тесте подставляем фейк (раздел 6).

---

**Частые ошибки.**
- Наследник забыл `super().__init__(...)` — нет атрибутов родителя.
- Считать, что `super()` — «родитель»: в ромбе он вызывает соседний класс по MRO.
- Наследовать ради переиспользования одного метода («страница наследует таблицу») — нужна композиция.
- Глубокие иерархии `BasePage → AuthPage → DashboardBasePage → ...` — трудно понять, откуда метод.
- Mixin справа от основного класса — его метод не будет вызван.

---

### Собес

- **Назови 4 принципа ООП с примерами.** Инкапсуляция — клиент прячет сессию и заголовки за
  методами. Наследование — `UsersClient(BaseClient)` получает общий `request`. Полиморфизм — у всех
  страниц `open()`, код вызывает его, не зная класса. Абстракция — `BasePage(ABC)` с абстрактным
  `path` задаёт контракт страницы.
- **Что такое MRO и как работает `super()`?** MRO — порядок поиска атрибутов: класс, затем родители
  слева направо, каждый раньше своих предков, общий предок в конце (алгоритм C3). `super()` берёт
  следующий класс в MRO объекта, а не обязательно родителя.
- **Что такое проблема ромба?** D наследует B и C, оба — от A. Вопрос: в каком порядке искать и не
  вызвать ли A дважды. В Python MRO = D, B, C, A, и при кооперативном `super()` каждый метод
  вызывается один раз.
- **Когда композиция лучше наследования?** Когда отношение «имеет», а не «является»: страница имеет
  шапку и форму. Композиция гибче: части переиспользуются, меньше связность, нет глубоких иерархий.
- **Расскажи SOLID на примере своего фреймворка.** S — клиенты только шлют запросы, проверки в
  тестах. O — новый эндпоинт = новый клиент. L — любой клиент подходит туда, где ждут `BaseClient`.
  I — маленькие компоненты страниц вместо толстого `BasePage`. D — клиент получает сессию снаружи,
  в юнит-тестах фреймворка подставляем фейк.

---

### Практика

Все команды — из папки `interview_prep/python_course/week3/c08_inheritance`.

- **Упражнения «что выведет»:** `drills.py`. Проверка: `uv run python drills.py`.
- **Задачи** (условия на английском, тесты: `uv run pytest -k t01`):
  - обязательные: t01 иерархия клиентов, t02 предскажи MRO, t03 абстрактная страница,
    t04 композиция, t05 рефакторинг по S;
  - ★ t06 mixin логирования.
