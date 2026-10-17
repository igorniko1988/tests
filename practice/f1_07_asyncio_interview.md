# F1. Урок 7 — asyncio и типовые Python-вопросы собеса

Задачи к уроку: `practice/f1_07_asyncio_interview.py`. Это последний урок модуля F1.

## Зачем это QA

- **asyncio** — async API Playwright, httpx, websockets (наш стакан ордеров на WebSocket),
  параллельные запросы в нагрузочных и интеграционных тестах.
- **GIL, потоки, процессы** — вопрос почти на каждом Senior-собесе: «почему pytest-xdist
  запускает процессы, а не потоки?».

## 1. Синхронно vs асинхронно

```python
import time

def fetch(n):
    time.sleep(1)          # ждём «сеть» и НИЧЕГО не делаем
    return n

[fetch(i) for i in range(3)]   # 3 секунды
```

Пока ждём сеть, процессор простаивает. Асинхронный код в это время переключается на другую задачу.

```python
import asyncio

async def fetch(n):            # async def → корутина
    await asyncio.sleep(1)     # await: «жду — можешь пока делать другое»
    return n

async def main():
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))   # параллельно
    print(results)             # [1, 2, 3] — за ~1 секунду, а не 3

asyncio.run(main())            # запустить event loop
```

| Слово | Что значит |
|---|---|
| `async def` | функция-корутина; вызов **не выполняет** её, а создаёт объект корутины |
| `await` | дождаться результата; можно только внутри `async def` |
| `asyncio.run()` | запустить event loop и главную корутину |
| `asyncio.gather()` | запустить несколько корутин одновременно и собрать результаты |
| `asyncio.wait_for(coro, timeout)` | ждать не дольше timeout → `TimeoutError` |
| event loop | «диспетчер»: крутит корутины, переключая их на каждом `await` |

### Главная ловушка

```python
async def bad():
    time.sleep(1)              # ❌ блокирует ВЕСЬ event loop — gather не поможет
async def good():
    await asyncio.sleep(1)     # ✅
```

Внутри async-кода нельзя вызывать блокирующее (`time.sleep`, `requests.get`). Нужны async-библиотеки:
`httpx.AsyncClient`, `aiohttp`, `playwright.async_api`.

## 2. Когда async нужен в тестах

| Нужен | Не нужен |
|---|---|
| WebSocket-подписка + действие одновременно | обычные API-тесты по одному запросу |
| много параллельных запросов (гонки, идемпотентность) | UI-тесты на sync API Playwright |
| async-фреймворк в проекте (pytest-asyncio) | параллельный запуск тестов — это xdist |

Тест на асинхронный код — через плагин `pytest-asyncio`:

```python
@pytest.mark.asyncio
async def test_parallel_orders():
    ...
```

## 3. GIL, потоки и процессы

- **GIL** (Global Interpreter Lock) — в CPython в один момент Python-код выполняет **один поток**.
- **Потоки** (`threading`) полезны для **ожидания** (сеть, диск): пока один ждёт, GIL отпущен.
  Для вычислений потоки не ускоряют.
- **Процессы** (`multiprocessing`) — у каждого свой интерпретатор и свой GIL → настоящий параллелизм.
- **asyncio** — один поток, переключение на `await`. Лёгкий, тысячи задач.

| Задача | Чем |
|---|---|
| много сетевых запросов | asyncio или потоки |
| тяжёлые вычисления | процессы |
| параллельные тесты | pytest-xdist (процессы: тесты изолированы, общий state не ломается) |

Python 3.13 умеет сборку без GIL (free-threaded), но экспериментально — по умолчанию GIL есть.

## 4. Типовые Python-вопросы собеса — короткие ответы

| Вопрос | Ответ |
|---|---|
| mutable / immutable | list, dict, set меняются; int, str, tuple — нет |
| `is` vs `==` | один объект vs равные значения |
| генератор vs список | лениво и один раз vs всё в памяти и много раз |
| `def f(x=[])` | дефолт создаётся один раз → общий для вызовов; используй `None` |
| shallow vs deep copy | копия верхнего уровня vs рекурсивная |
| `*args` / `**kwargs` | tuple позиционных / dict именованных |
| декоратор | функция, принимающая функцию и возвращающая обёртку |
| `@staticmethod` / `@classmethod` | без self и cls / получает cls (альтернативные конструкторы) |
| GIL | один поток исполняет Python-код за раз |
| `__init__` vs `__new__` | инициализирует уже созданный объект vs создаёт объект |
| LEGB | порядок поиска имён: Local → Enclosing → Global → Built-in |
| list comprehension vs `map` | одно и то же; comprehension читаемее |

## Вопросы собеседования

1. Что вернёт вызов `async def` функции без `await`?
2. Почему `time.sleep()` внутри корутины — ошибка? Что использовать?
3. Чем `asyncio.gather` отличается от последовательных `await`?
4. Что такое GIL? Помогут ли потоки ускорить вычисления? А сетевые запросы?
5. Почему pytest-xdist запускает процессы, а не потоки?
6. Когда в автотестах действительно нужен async?
