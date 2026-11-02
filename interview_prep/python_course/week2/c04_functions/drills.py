"""C4 · Функции и области видимости — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки interview_prep/python_course/week2/c04_functions): uv run python drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {'12', '13', '14', '15', '16'}  # доп. фрагменты: можно пропустить


D["1"] = """
def f(*args, **kwargs):
    print(args, kwargs)

f(1, 2, a=3)
f()
"""
A["1"] = ""


D["2"] = """
def f(a, b=2, *args):
    print(a, b, args)

f(1)
f(1, 3, 5, 7)
"""
A["2"] = ""


D["3"] = """
def point(x, y):
    return x - y

data = {"y": 1, "x": 10}
print(point(*[10, 1]), point(**data))
"""
A["3"] = ""


D["4"] = """
def get(url, *, timeout=5):
    return timeout

print(get("/a", timeout=1))
print(get("/a", 1))
"""
A["4"] = ""


D["5"] = """
x = 1

def f():
    print(x)
    x = 2

f()
"""
A["5"] = ""


D["6"] = """
x = 1

def f():
    global x
    x += 1
    return x

print(f(), f(), x)
"""
A["6"] = ""


D["7"] = """
def outer():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

a = outer()
b = outer()
print(a(), a(), b())
"""
A["7"] = ""


D["8"] = """
fs = [lambda: i for i in range(3)]
print([f() for f in fs])
"""
A["8"] = ""


D["9"] = """
fs = [lambda i=i: i * 10 for i in range(3)]
print([f() for f in fs])
"""
A["9"] = ""


D["10"] = """
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
print(square(5), square(base=3))
"""
A["10"] = ""


D["11"] = """
def greet():
    return "hi"

x = greet
y = greet()
print(type(x).__name__, y)
"""
A["11"] = ""


# доп. — по желанию
D["12"] = """
def add(item, items=[]):
    items.append(item)
    return items

add(1)
print(add(2), add.__defaults__)
"""
A["12"] = ""


# доп. — по желанию
D["13"] = """
def outer():
    x = "enclosing"
    def inner():
        return x
    x = "changed"
    return inner

print(outer()())
"""
A["13"] = ""


# доп. — по желанию
D["14"] = """
items = []

def add(x):
    items.append(x)

add(1)
add(2)
print(items)
"""
A["14"] = ""


# доп. — по желанию
D["15"] = """
from functools import cache

calls = 0

@cache
def slow(n):
    global calls
    calls += 1
    return n * 2

print(slow(2), slow(2), slow(3), calls)
"""
A["15"] = ""


# доп. — по желанию
D["16"] = """
print(sorted(["b", "A", "c"], key=str.lower), max([3, -7, 5], key=abs))
"""
A["16"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
