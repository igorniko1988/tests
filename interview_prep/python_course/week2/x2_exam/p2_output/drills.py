"""X2 · Часть 2. «Что выведет» — 10 фрагментов на замыкания, генераторы и декораторы. Время: 15 минут.

Впиши ответ в A[...] под каждым фрагментом ДО запуска, без IDE и без интерпретатора:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ, строки без кавычек,
    внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Зачёт: 8 из 10.
Проверка (из папки interview_prep/python_course/week2/x2_exam): uv run python p2_output/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["1"] = """
def make():
    fs = []
    for i in range(3):
        fs.append(lambda x: x + i)
    return fs

print([f(10) for f in make()])
"""
A["1"] = ""


D["2"] = """
def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

a, b = counter(), counter()
a(); a()
print(a(), b())
"""
A["2"] = ""


D["3"] = """
x = 5

def f():
    x += 1
    return x

print(f())
"""
A["3"] = ""


D["4"] = """
def f(a, *args, b=2, **kwargs):
    print(a, args, b, kwargs)

f(1, 2, 3, c=4)
"""
A["4"] = ""


D["5"] = """
def gen():
    for i in range(3):
        print("yield", i)
        yield i

g = gen()
print(next(g), next(g))
"""
A["5"] = ""


D["6"] = """
g = (x for x in [1, 2, 3])
print(sum(g), sum(g))
"""
A["6"] = ""


D["7"] = """
def gen():
    yield 1
    yield 2

g = gen()
print(list(g), next(g, "done"))
"""
A["7"] = ""


D["8"] = """
def deco(func):
    def wrapper(*args):
        return func(*args) + 1
    return wrapper

@deco
@deco
def five():
    return 5

print(five(), five.__name__)
"""
A["8"] = ""


D["9"] = """
calls = []

def deco(func):
    calls.append("deco")
    return func

@deco
def a(): pass

@deco
def b(): pass

print(calls)
"""
A["9"] = ""


D["10"] = """
from itertools import islice

def naturals():
    n = 1
    while True:
        yield n
        n += 1

print(list(islice((x * x for x in naturals() if x % 2), 3)))
"""
A["10"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from drill import run

    run(D, A, __file__)
