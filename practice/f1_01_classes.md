# F1. Урок 1 — классы и объекты

Задачи к уроку: `practice/f1_01_classes.py`.

## Зачем это QA

Почти весь код тестового фреймворка — классы: **Page Object** (страница), **клиент API**,
**сервисы**, **модели данных**. Понимаешь классы — понимаешь, как устроен любой фреймворк.

## 1. Класс и объект

**Класс** — чертёж. **Объект** — вещь, сделанная по чертежу.

```python
class User:              # чертёж «пользователь»
    pass


alice = User()           # объект № 1
bob = User()             # объект № 2 — отдельный, независимый
```

Чертёж один, объектов по нему — сколько угодно.

## 2. `__init__` и `self` — данные объекта

```python
class User:
    def __init__(self, email, balance):
        self.email = email           # сохранить в объект
        self.balance = balance


alice = User("alice@example.com", 100)
bob = User("bob@example.com", 0)

print(alice.email)                   # alice@example.com
print(bob.balance)                   # 0
```

- **`__init__`** выполняется **автоматически**, когда создаёшь объект: `User(...)`.
  Он заполняет новый объект данными.
- **`self`** — **сам объект**, который сейчас создаётся (или с которым работаем).
  `self.email = email` — «положи email в **этот** объект».
- `alice.email` и `bob.email` — разные значения: у каждого объекта свои данные.

Как читать `User("alice@example.com", 100)`: Python создаёт пустой объект → вызывает
`__init__(этот_объект, "alice@example.com", 100)` → внутри `self` — это и есть новый объект.

## 3. Методы — действия объекта

```python
class User:
    def __init__(self, email, balance):
        self.email = email
        self.balance = balance

    def deposit(self, amount):       # метод — функция внутри класса
        self.balance += amount

    def can_buy(self, price):
        return self.balance >= price


alice = User("alice@example.com", 100)
alice.deposit(50)
print(alice.balance)                 # 150
print(alice.can_buy(200))            # False
```

- **Метод** — функция внутри класса, первым параметром всегда `self`.
- При вызове `alice.deposit(50)` Python **сам** подставляет `alice` в `self` — ты передаёшь только `amount`.
- Метод может **менять данные объекта** (`deposit`) или **возвращать ответ** (`can_buy`).

## 4. Атрибут класса и атрибут объекта

```python
class User:
    min_password_length = 8          # атрибут КЛАССА — общий для всех

    def __init__(self, email):
        self.email = email           # атрибут ОБЪЕКТА — у каждого свой
```

`User.min_password_length` — одно значение на всех. `alice.email` — у каждой свой.

В тестах так хранят **общие константы** (например, адрес страницы в Page Object),
а в `self` — то, что у каждого объекта своё.

**Ловушка:** изменяемый атрибут класса (список, словарь) — **один на всех объектов**.
Если один объект добавит в него элемент, его увидят все. Об этом задача 5.

## 5. Как это выглядит в UI-тестах

Page Object страницы входа нашей биржи будет примерно таким:

```python
class LoginPage:
    url = "/app/"                                    # общее: адрес страницы

    def __init__(self, page):
        self.page = page                             # своё у каждого: вкладка браузера

    def open(self):
        self.page.goto(self.url)

    def login(self, email, password):
        self.page.get_by_test_id("email-input").fill(email)
        self.page.get_by_test_id("password-input").fill(password)
        self.page.get_by_test_id("login-button").click()
```

Те же четыре вещи: класс, `__init__`, `self`, методы. Ничего нового.

## Шпаргалка

| Что | Как выглядит | Зачем |
|---|---|---|
| класс | `class User:` | чертёж |
| объект | `alice = User(...)` | конкретная вещь по чертежу |
| `__init__` | `def __init__(self, ...):` | заполнить новый объект данными |
| `self` | `self.email = email` | «этот объект» |
| метод | `def deposit(self, amount):` | действие объекта |
| атрибут объекта | `self.email` | у каждого свой |
| атрибут класса | `url = "/app/"` в теле класса | общий для всех |

## Вопросы собеседования

1. Чем класс отличается от объекта?
2. Что такое `self` и почему его не передают при вызове метода?
3. Когда вызывается `__init__`? Это конструктор?
4. Чем атрибут класса отличается от атрибута объекта? Чем опасен изменяемый атрибут класса?
