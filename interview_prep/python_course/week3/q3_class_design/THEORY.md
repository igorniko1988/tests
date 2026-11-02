# Q3 · Проектирование классов

**Смысл темы.** Частый формат собеса AQA — «спроектируй и напиши класс»: LRU-кэш, rate limiter,
банковский счёт, деньги, API-клиент. Проверяют не только код, но и решения: какой интерфейс,
какие инварианты (что всегда должно быть верно), какие ошибки и как их сообщать, как это
тестировать. Здесь собирается всё из C7–C9 и A-трека: property, магические методы, свои
исключения, `OrderedDict`, `deque`, подменяемые зависимости.

---

### 1. Как отвечать на «спроектируй класс»

1. **Уточни требования:** какие операции, какие ограничения (ёмкость, лимит, валюты), что делать
   при ошибке, нужна ли потокобезопасность.
2. **Интерфейс сначала:** имена методов, аргументы, что возвращают, какие исключения бросают.
3. **Инварианты:** «баланс не отрицательный», «в кэше не больше capacity», «сумма — Decimal».
   Их проверяем в одном месте (конструктор, setter, приватный метод).
4. **Структура данных под сложность:** LRU — O(1) на `get/put` → словарь + порядок (`OrderedDict`).
5. **Зависимости снаружи:** время (`clock`), HTTP-сессия, браузер — параметры конструктора,
   чтобы в тестах подставить фейк.
6. **Скажи, как будешь тестировать:** граничные случаи, ошибки, время.

---

### 2. LRU cache

**LRU (Least Recently Used)** — кэш ограниченного размера; при переполнении выбрасывает элемент,
к которому дольше всех не обращались. `get` и `put` — O(1).

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._data = OrderedDict()          # порядок: от давно использованного к свежему

    def get(self, key, default=None):
        if key not in self._data:
            return default
        self._data.move_to_end(key)         # обращение делает ключ «свежим»
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)  # выкинуть самый старый
```

- **`OrderedDict.move_to_end` и `popitem(last=False)`** — O(1). Обычный `dict` тоже хранит порядок,
  но «переместить в конец» у него — `pop` + вставка.
- **Руками (классика собеса):** dict «ключ → узел» + двусвязный список узлов; голова — старые,
  хвост — свежие. Перемещение узла — перецепить 4 ссылки, O(1).
- **`functools.lru_cache`** — тот же принцип для результатов функций.

---

### 3. Rate limiter

«Не больше N запросов за T секунд». Два варианта:

```python
from collections import deque

class SlidingWindowLimiter:
    def __init__(self, limit, window, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self._times = deque()                    # моменты разрешённых запросов

    def allow(self):
        now = self.clock()
        while self._times and self._times[0] <= now - self.window:
            self._times.popleft()                # вышли из окна
        if len(self._times) < self.limit:
            self._times.append(now)
            return True
        return False
```

- **Фиксированное окно:** счётчик сбрасывается в начале каждой секунды/минуты. Просто, но на стыке
  окон можно пропустить 2N запросов.
- **Скользящее окно:** храним времена последних запросов (deque — скользящее окно A4); честнее,
  памяти O(N).
- **Token bucket** — ещё вариант: «ведро» токенов пополняется с постоянной скоростью; допускает
  короткие всплески.
- **В AQA:** тестировать 429 и `Retry-After` у API (стенд: 5 неудачных входов за 60 с → 429), не
  перегружать сторонний сервис из нагрузочного скрипта.

---

### 4. Свои исключения

```python
class BankError(Exception):
    """Базовая ошибка домена — её ловят все, кому не важны детали."""

class InsufficientFunds(BankError):
    def __init__(self, balance, amount):
        super().__init__(f"balance {balance} < {amount}")
        self.balance, self.amount = balance, amount      # данные для обработчика и отчёта

class AccountClosed(BankError):
    pass
```

- **Иерархия:** общий базовый класс домена → конкретные. Код ловит ровно то, что умеет обработать:
  `except InsufficientFunds`, а остальное — `except BankError`.
- **Полезные атрибуты** (`status`, `body`, `balance`) вместо разбора текста сообщения.
- **Не глотать `Exception` целиком** и не использовать исключения для обычного управления потоком.
- **В фреймворке:** `ApiError(status, body)` вместо `assert resp.status_code == 200` внутри клиента —
  тест решает, ожидаемая ли это ошибка (`pytest.raises(ApiError)`).

---

### 5. Value object: Money

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```

- **Value object** — объект-значение: равенство по содержимому, неизменяемый, хешируемый. Деньги,
  координаты, диапазон дат.
- **Неизменяемость** — операции возвращают новый объект; нельзя случайно поменять сумму в чужом
  списке.
- **Запрет смешивать валюты** — инвариант, проверяемый в операторах.
- **Сравнение разных валют** (`<`) — тоже ошибка: `5 USD < 3 EUR` смысла не имеет.

---

### 6. API-клиент и Page Object

```python
class ApiError(Exception):
    def __init__(self, status, body):
        super().__init__(f"HTTP {status}: {body}")
        self.status, self.body = status, body

class ApiClient:
    def __init__(self, base_url, session, token=None):
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.token = token

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def request(self, method, path, **kwargs):
        resp = self.session.request(method, f"{self.base_url}{path}", headers=self._headers(), **kwargs)
        if resp.status >= 400:
            raise ApiError(resp.status, resp.body)
        return resp.body
```

- **Один `request` — всё общее** (URL, заголовки, ошибки, логирование, ретраи); `get`/`post` —
  тонкие обёртки.
- **Сессия снаружи** — в тестах фейк, в бою `requests.Session`.
- **Page Object** — композиция компонентов (C8): страница хранит части, методы возвращают данные,
  а проверки делает тест.

---

**Частые ошибки.**
- LRU: `get` не обновляет «свежесть» ключа; `put` существующего ключа не двигает его в конец.
- Rate limiter на `time.time()` внутри — тест вынужден спать.
- Исключения: `raise Exception("error")` без своего типа; потеря данных (`status`) в тексте.
- Money на float; изменяемый Money; сложение разных валют молча.
- Клиент делает `assert` внутри — нельзя проверить негативный сценарий.

---

### Собес

- **Как сделать LRU cache с O(1)?** Словарь для поиска плюс порядок использования: `OrderedDict`
  с `move_to_end` на каждом обращении и `popitem(last=False)` при переполнении. Руками — dict +
  двусвязный список, голова — давно использованные.
- **Как сделать rate limiter?** Фиксированное окно — счётчик на интервал (просто, но всплеск на
  стыке). Скользящее — deque времён запросов, выбрасываем устаревшие (точнее). Token bucket —
  пополняемое ведро токенов. Время передаю параметром, чтобы тестировать без sleep.
- **Зачем свои исключения?** Чтобы ловить конкретные ошибки и передавать данные (status, body,
  balance). Строю иерархию от базового исключения домена.
- **Что такое value object?** Объект, равный по значению, неизменяемый и хешируемый: Money,
  диапазон дат. Операции возвращают новые объекты, инварианты проверяются при создании.

---

### Задачи

Все команды — из папки `interview_prep/python_course/week3/q3_class_design`, тесты: `uv run pytest -k t01`.

- **Обязательные:** t01 LRU cache, t02 rate limiter, t03 банковский счёт, t04 Money.
- **★ по желанию:** t05 API-клиент, t06 LRU руками (без OrderedDict).
