"""C6 · Декораторы — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки interview_prep/python_course/week2/c06_decorators): uv run python drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {'11', '12', '13', '14'}  # доп. фрагменты: можно пропустить


D["1"] = """
def deco(func):
    def wrapper():
        return func() * 2
    return wrapper

@deco
def five():
    return 5

print(five())
"""
A["1"] = ""


D["2"] = """
def deco(func):
    print("decorating", func.__name__)
    return func

@deco
def f():
    print("call")

print("before call")
f()
"""
A["2"] = ""


D["3"] = """
def deco(func):
    def wrapper(*args):
        func(*args)
    return wrapper

@deco
def add(a, b):
    return a + b

print(add(1, 2))
"""
A["3"] = ""


D["4"] = """
def deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@deco
def login():
    """Logs in."""

print(login.__name__, login.__doc__)
"""
A["4"] = ""


D["5"] = """
from functools import wraps

def deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@deco
def login():
    """Logs in."""

print(login.__name__, login.__doc__, login.__wrapped__.__name__)
"""
A["5"] = ""


D["6"] = """
def tag(name):
    def deco(func):
        def wrapper():
            return f"<{name}>{func()}</{name}>"
        return wrapper
    return deco

@tag("b")
@tag("i")
def text():
    return "hi"

print(text())
"""
A["6"] = ""


D["7"] = """
order = []

def a(func):
    def wrapper():
        order.append("a")
        return func()
    return wrapper

def b(func):
    def wrapper():
        order.append("b")
        return func()
    return wrapper

@a
@b
def f():
    order.append("f")

f()
print(order)
"""
A["7"] = ""


D["8"] = """
def count(func):
    def wrapper(*args):
        wrapper.calls += 1
        return func(*args)
    wrapper.calls = 0
    return wrapper

@count
def ping():
    return "pong"

ping(); ping(); ping()
print(ping.calls)
"""
A["8"] = ""


D["9"] = """
def retry(times):
    def deco(func):
        def wrapper():
            for _ in range(times):
                try:
                    return func()
                except ValueError:
                    pass
            return "gave up"
        return wrapper
    return deco

attempts = []

@retry(3)
def flaky():
    attempts.append(1)
    if len(attempts) < 2:
        raise ValueError
    return "ok"

print(flaky(), len(attempts))
"""
A["9"] = ""


D["10"] = """
def retry(times=3):
    def deco(func):
        return func
    return deco

@retry
def f():
    return 1

print(f())
"""
A["10"] = ""


# доп. — по желанию
D["11"] = """
class Count:
    def __init__(self, func):
        self.func = func
        self.n = 0

    def __call__(self, *args):
        self.n += 1
        return self.func(*args)

@Count
def double(x):
    return x * 2

print(double(4), double(5), double.n, type(double).__name__)
"""
A["11"] = ""


# доп. — по желанию
D["12"] = """
def deco(func):
    def wrapper(*args, **kwargs):
        print(type(args[0]).__name__, args[1:], kwargs)
        return func(*args, **kwargs)
    return wrapper

class Api:
    @deco
    def get(self, path, timeout=5):
        return path

print(Api().get("/x", timeout=1))
"""
A["12"] = ""


# доп. — по желанию
D["13"] = """
calls = []

def deco(func):
    calls.append("deco")
    def wrapper():
        calls.append("wrapper")
        return func()
    return wrapper

@deco
def f():
    calls.append("f")

f(); f()
print(calls)
"""
A["13"] = ""


# доп. — по желанию
D["14"] = """
from functools import lru_cache

@lru_cache(maxsize=None)
def square(n):
    print("compute", n)
    return n * n

print(square(3), square(3))
"""
A["14"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
