"""Урок 5. Декораторы, шаг 1.

    python lessons/lesson_05_decorators.py
"""

# --- Шаг A. Функция это объект ------------------------------------------
def hello():
    return "hi"

f = hello                  # без скобок: второй ярлык на функцию
print(f())                 # hi


def call_twice(func):
    func()
    func()

call_twice(lambda: print("called"))   # called, called


# --- Шаг B. Функция возвращает функцию (замыкание) ----------------------
def make_greeter(name):
    def greet():
        return f"Hello, {name}"
    return greet           # возвращаем функцию, не вызывая

g = make_greeter("Igor")
print(g())                 # Hello, Igor


# --- Шаг C. Декоратор ----------------------------------------------------
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        result = func(*args, **kwargs)     # вызов оригинала
        print(f"done {func.__name__}")
        return result
    return wrapper


def add(a, b):
    return a + b

add = log_calls(add)       # заменяем add на обёртку
print(add(2, 3))           # calling add / done add / 5


# --- Шаг D. Запись через @ ----------------------------------------------
@log_calls
def multiply(a, b):
    return a * b           # то же самое, что multiply = log_calls(multiply)

print(multiply(4, 5))      # calling multiply / done multiply / 20
