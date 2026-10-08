"""
F1. Урок 3 — декораторы.

Теория: practice/f1_03_decorators.md
Запуск: uv run python practice/f1_03_decorators.py

Задача 1. Функция как объект.
    Напиши функции add(a, b) и multiply(a, b) и функцию apply(func, a, b),
    которая вызывает переданную функцию с a и b. Проверь: apply(add, 2, 3) == 5,
    apply(multiply, 2, 3) == 6.

Задача 2. Декоратор логирования.
    Декоратор log_calls: перед вызовом печатает имя функции и аргументы,
    после — что функция вернула. Обязательно *args, **kwargs и @wraps.
    Задекорируй deposit(asset, amount) и вызови с позиционными и именованными аргументами.
    Проверь, что deposit.__name__ == "deposit" (благодаря @wraps).

Задача 3. Замер времени (частая задача на собесе).
    Декоратор timer: печатает, сколько секунд выполнялась функция
    (time.perf_counter() до и после). Задекорируй функцию, внутри которой time.sleep(0.3).

Задача 4. Декоратор с параметром.
    Декоратор retry(times): вызывает функцию, при исключении повторяет,
    всего не больше times попыток; если все неудачны — пробрасывает последнюю ошибку.
    Проверь на функции, которая падает первые 2 раза и на третий возвращает "OK"
    (счётчик вызовов — снаружи функции, как мы делали). Потом проверь с times=2 — должна упасть.

Задача 5. Проверка аргументов.
    Декоратор positive_amount: если именованный аргумент amount <= 0,
    бросает ValueError, а функцию не вызывает. Задекорируй deposit(asset, amount).

Задача 6 (со звёздочкой). Порядок декораторов.
    Повесь на одну функцию @log_calls и @timer в разном порядке и объясни,
    почему вывод отличается.

Вопросы собеса (ответь своими словами внизу файла):
    1. Что такое декоратор? Что на самом деле делает строка @decorator над функцией?
    2. Зачем в обёртке *args, **kwargs?
    3. Зачем functools.wraps?
    4. Как написать декоратор с параметрами (@retry(times=3))? Почему три уровня функций?
    5. В каком порядке применяются несколько декораторов?
"""
from functools import wraps


# --- Задача 1 ---
def add(a,b):
    return a + b

def multiply(a, b):
    return a * b

def apply(func, a, b):
    return func(a, b)

print(apply(multiply,2,5))
# --- Задача 2 ---


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Function name {func.__name__} with arguments {args} and {kwargs}')
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_calls
def print_hello(name):
    return f'hi {name}'

print(print_hello('niko'))

# --- Задача 3 ---
from time import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        result_time = time() - start
        return result_time
    return wrapper

@timer
def print_hello(name):
    return f'hi {name}'

print(print_hello('mik'))



# --- Задача 4 ---
def retry(retry_number):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for i in range(1, retry_number + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == retry_number:
                        raise
                    print('One more try')
        return inner
    return wrapper

@retry(4)
def print_number(number):
    for i in range(number):
        if i < 3:
            raise ValueError('too low number')
    return f'Final number is {number}'

print(print_number(5))

# --- Задача 5 ---
def positive_amount(func):
    if func.amount <= 0:
        raise ValueError



# --- Задача 6 ---


@timer
@log_calls
def print_hi():
    print('hi')
    return 'hi'

print_hi()
# --- Ответы на вопросы собеса ---
# 1. Decorator above function adds any aditional logic it depends on the needs
# 2. By this data we pass any arguments in the decorated function
# 3. functools.wraps stands for the correct name in the decorated function, if wraps doesnt exist the name by default wrapper or wrapped
# 4. Pass several layers of function first will take retry number, lower will take function and the last arguments
# 5. from down to up
