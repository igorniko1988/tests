"""C7 · Классы и объекты — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки interview_prep/python_course/week3/c07_classes): uv run python drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {'11', '12', '13', '14'}  # доп. фрагменты: можно пропустить


D["1"] = """
class A:
    x = 1

a, b = A(), A()
a.x = 5
print(a.x, b.x, A.x)
"""
A["1"] = ""


D["2"] = """
class A:
    x = 1

a = A()
A.x = 7
print(a.x)
"""
A["2"] = ""


D["3"] = """
class Cart:
    items = []

    def add(self, item):
        self.items.append(item)

c1, c2 = Cart(), Cart()
c1.add("apple")
print(c2.items)
"""
A["3"] = ""


D["4"] = """
class Cart:
    items = []

    def reset(self):
        self.items = []

c1, c2 = Cart(), Cart()
c1.reset()
c1.items.append(1)
print(c1.items, c2.items, Cart.items)
"""
A["4"] = ""


D["5"] = """
class P:
    def hello():
        return "hi"

print(P().hello())
"""
A["5"] = ""


D["6"] = """
class Temp:
    def __init__(self, c):
        self.c = c

    @property
    def f(self):
        return self.c * 9 / 5 + 32

t = Temp(100)
t.c = 0
print(t.f)
"""
A["6"] = ""


D["7"] = """
class Temp:
    @property
    def f(self):
        return 1

t = Temp()
t.f = 2
"""
A["7"] = ""


D["8"] = """
class Base:
    @classmethod
    def create(cls):
        return cls()

class Child(Base):
    pass

print(type(Child.create()).__name__)
"""
A["8"] = ""


D["9"] = """
class M:
    @staticmethod
    def add(a, b):
        return a + b

print(M.add(1, 2), M().add(3, 4))
"""
A["9"] = ""


D["10"] = """
class Acc:
    def __init__(self):
        self.__pin = 1

a = Acc()
print(a._Acc__pin)
print(a.__pin)
"""
A["10"] = ""


# доп. — по желанию
D["11"] = """
class Counter:
    count = 0

    def __init__(self):
        self.count += 1

a = Counter()
b = Counter()
print(a.count, b.count, Counter.count)
"""
A["11"] = ""


# доп. — по желанию
D["12"] = """
class U:
    def __init__(self, name):
        self.name = name

u = U("ann")
u.nmae = "bob"
print(u.name, sorted(vars(u)))
"""
A["12"] = ""


# доп. — по желанию
D["13"] = """
from functools import cached_property

class R:
    @cached_property
    def total(self):
        print("calc")
        return 42

r = R()
print(r.total, r.total)
"""
A["13"] = ""


# доп. — по желанию
D["14"] = """
class A:
    def m(self):
        return "A"

a = A()
a.m = lambda: "patched"
print(a.m(), A().m())
"""
A["14"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
