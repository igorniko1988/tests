"""
F1. Урок 5 — типизация, исключения, *args / **kwargs.

Теория: practice/f1_05_typing_errors.md
Запуск: uv run python practice/f1_05_typing_errors.py

Задача 1. Аннотации.
    Перепиши функцию с аннотациями типов (аргументы и возвращаемое значение):
        def place_order(symbol, side, price, quantity, idempotency_key=None):
            return {"symbol": symbol, "side": side, "price": price, "quantity": quantity}
    side — только "BUY" или "SELL" (Literal), idempotency_key — строка или None.
    Вызови с неправильным типом (например, price="abc") — упадёт ли при запуске? Почему?

Задача 2. Ловим разные исключения.
    Функция parse_balance(data: dict) -> float возвращает float(data["available"]).
    Вызови её с тремя входами и поймай каждую ошибку отдельным except, напечатав тип:
        {"available": "100.5"}  -> работает
        {"available": "abc"}    -> ValueError
        {}                      -> KeyError
    Добавь else (печатает "ок") и finally (печатает "проверка закончена").

Задача 3. Своё исключение.
    Класс ApiError(Exception) с полями status_code и body и понятным сообщением.
    Функция check_response(status_code: int, body: str): если status_code >= 400 —
    raise ApiError(...). Поймай ApiError и выведи status_code из пойманного объекта.

Задача 4. raise ... from ...
    Функция load_json(text: str) -> dict: пробует json.loads(text), а при ошибке
    бросает ApiError(0, text) from исходной ошибки. Вызови с "не json" без try —
    посмотри трейсбек: видны ли обе ошибки? Потом закомментируй вызов.

Задача 5. *args и **kwargs.
    a) Функция total(*amounts) возвращает сумму всех переданных чисел: total(1, 2, 3) == 6.
    b) Функция make_order(**overrides) возвращает словарь ордера по умолчанию
       {"symbol": "ETH-USDT", "side": "BUY", "price": "2", "quantity": "1"},
       заменяя поля из overrides. Проверь make_order(side="SELL", price="5").
    c) Есть данные user = {"email": "a@b.com", "password": "secret123"}.
       Вызови register(email, password) через распаковку **user.

Задача 6. Тест «падает» — это исключение.
    Напиши assert 1 == 2, "числа не равны" внутри try и поймай исключение.
    Выведи его тип и сообщение. Какой тип?

Вопросы собеса (ответь своими словами внизу файла):
    1. Проверяет ли Python типы при запуске? Зачем тогда аннотации?
    2. Чем except Exception отличается от голого except:? Почему нельзя except: pass?
    3. Что делают else и finally в try?
    4. Зачем свои классы исключений? Что даёт raise ... from ...?
    5. Что такое *args и **kwargs? Что значит ** при вызове функции?
    6. Какое исключение бросает упавший assert?
"""


# --- Задача 1 ---

def place_order(symbol: str, side: str, price: float | int, quantity: int, idempotency_key: str | None = None) -> dict:
    return {"symbol": symbol, "side": side, "price": price, "quantity": quantity}

# --- Задача 2 ---

def parse_balance(data: dict) -> float:
    try:
        return float(data['available'])
    except ValueError('invalid value') as e:
        print(f'check the erro {e}')
    except KeyError as e:
        print(f'there is no such key {e}')

# parse_balance({"available": "abc"})
# --- Задача 3 ---

class ApiError(Exception):
    def __init__(self, status_code, body):
        super().__init__(status_code, body)


def check_status(status_code: int, message: str):
    if status_code == 400:
        raise ApiError('check body')
# --- Задача 4 ---


# --- Задача 5 ---

def total_amount(*amounts):
    return sum(amounts)

def make_order(**overrides):
    orders = {"symbol": "ETH-USDT", "side": "BUY", "price": "2", "quantity": "1"}
    orders.update(overrides)
    return orders

g = make_order(side='SELL', price=5)
print(g)


user = {"email": "a@b.com", "password": "secret123"}

def register(email, password):
    return {'email': email, 'password': password}

print(register(**user))
# --- Задача 6 ---


# --- Ответы на вопросы собеса ---
# 1. For the human to know what type of data pass into functions
# 2. if expect pass so its dificult to debug the problem
# 3. finally executes that part of code every time, else its like another leg of logic
# 4. raise from give ability to read the detail of error
# 5. ** means that you unpack passed data inot function/method
# 6. AssertionError. is thrown in case of assert
