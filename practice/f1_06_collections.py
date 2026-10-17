"""
F1. Урок 6 — коллекции и задачи для лайвкодинга.

Теория: practice/f1_06_collections.md
Запуск: uv run python practice/f1_06_collections.py

Данные для всех задач — «ответ API» ниже (ORDERS).

Задача 1. Comprehension.
    a) Список id всех ордеров.
    b) Список ордеров со статусом "NEW".
    c) dict id -> status.
    d) set уникальных symbol.

Задача 2. Подсчёт и группировка.
    a) Сколько ордеров в каждом статусе (Counter).
    b) dict symbol -> список id ордеров (defaultdict).
    c) Сумма quantity по каждому symbol (quantity — строки, переведи в float).

Задача 3. Дубли.
    В ORDERS есть повторяющиеся id. Найди их (список id, которые встречаются больше одного раза).
    Потом получи список ордеров без дублей (оставь первое вхождение, порядок сохранить).

Задача 4. Сортировка.
    a) Ордера по цене (price — строка! сортируй как число) по убыванию.
    b) Самый дорогой ордер через max.
    c) По status, а внутри статуса по id.

Задача 5. Сравнение выборок (частая проверка в тестах).
    EXPECTED_SYMBOLS = {"ETH-USDT", "BTC-USDT", "SOL-USDT"}
    Сравни с symbol из ORDERS: каких не хватает, какие лишние, какие совпали.

Задача 6. JSON.
    Строку RAW (ниже) преобразуй в dict, достань email пользователя и количество ордеров.
    Достань поле "phone" так, чтобы при его отсутствии получилось "нет" (без KeyError).
    Выведи dict обратно в строку с indent=2.

Задача 7. Мутабельность.
    a) a = [1, 2]; b = a; b.append(3) — выведи a. Потом сделай так, чтобы a не менялся.
    b) Напиши add_tag(tag, tags=[]) и вызови дважды без tags — что не так? Исправь.
    c) Сравни через is и == два списка [1, 2] и [1, 2].

Вопросы собеса (ответь своими словами внизу файла):
    1. Чем list отличается от tuple? Почему list не может быть ключом dict?
    2. Почему in для set быстрее, чем для list?
    3. Чем sorted() отличается от .sort()?
    4. Что выведет a = [1]; b = a; b.append(2); print(a)? Как сделать копию?
    5. В чём ловушка def f(items=[])?
    6. is vs == — в чём разница?
"""

ORDERS = [
    {"id": 1, "symbol": "ETH-USDT", "side": "BUY", "price": "2000", "quantity": "1.5", "status": "NEW"},
    {"id": 2, "symbol": "BTC-USDT", "side": "SELL", "price": "60000", "quantity": "0.1", "status": "FILLED"},
    {"id": 3, "symbol": "ETH-USDT", "side": "SELL", "price": "2100", "quantity": "2", "status": "NEW"},
    {"id": 2, "symbol": "BTC-USDT", "side": "SELL", "price": "60000", "quantity": "0.1", "status": "FILLED"},
    {"id": 4, "symbol": "DOGE-USDT", "side": "BUY", "price": "0.1", "quantity": "1000", "status": "CANCELLED"},
    {"id": 5, "symbol": "ETH-USDT", "side": "BUY", "price": "1950", "quantity": "0.5", "status": "FILLED"},
    {"id": 3, "symbol": "ETH-USDT", "side": "SELL", "price": "2100", "quantity": "2", "status": "NEW"},
]

RAW = '{"user": {"email": "a@b.com", "id": 7}, "orders": [{"id": 1}, {"id": 2}, {"id": 3}]}'


# --- Задача 1 ---


# --- Задача 2 ---


# --- Задача 3 ---


# --- Задача 4 ---


# --- Задача 5 ---


# --- Задача 6 ---


# --- Задача 7 ---


# --- Ответы на вопросы собеса ---
