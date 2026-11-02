"""X3 · Часть 2. «Что выведет» — 10 фрагментов на MRO, атрибуты класса и магические методы. Время: 15 минут.

Впиши ответ в A[...] под каждым фрагментом ДО запуска, без IDE и без интерпретатора:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ, строки без кавычек,
    внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Зачёт: 8 из 10.
Проверка (из папки interview_prep/python_course/week3/x3_exam): uv run python p2_output/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["1"] = """
class Config:
    headers = {}

a, b = Config(), Config()
a.headers["X"] = "1"
b.headers = {"Y": "2"}
print(a.headers, b.headers, Config.headers)
"""
A["1"] = ""


D["2"] = """
class A:
    def f(self):
        return "A"

class B(A):
    def f(self):
        return "B" + super().f()

class C(A):
    def f(self):
        return "C" + super().f()

class D(C, B):
    pass

print(D().f(), [k.__name__ for k in D.__mro__][1:3])
"""
A["2"] = ""


D["3"] = """
class P:
    @property
    def x(self):
        return 1

p = P()
p.x = 2
"""
A["3"] = ""


D["4"] = """
class Base:
    @classmethod
    def make(cls):
        return cls.__name__

class Child(Base):
    pass

print(Base.make(), Child.make(), Child().make())
"""
A["4"] = ""


D["5"] = """
class K:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

print(K(1) == K(1), K(1) in [K(1)])
print(len({K(1)}))
"""
A["5"] = ""


D["6"] = """
class V:
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return f"V({self.n})"

    def __add__(self, other):
        return V(self.n + other.n)

    def __radd__(self, other):
        return self if other == 0 else NotImplemented

print(sum([V(1), V(2), V(3)]))
"""
A["6"] = ""


D["7"] = """
from dataclasses import dataclass, field

@dataclass
class Order:
    symbol: str
    tags: list = field(default_factory=list)

a, b = Order("BTC"), Order("BTC")
a.tags.append("x")
print(a == b, b.tags)
"""
A["7"] = ""


D["8"] = """
class Counter:
    total = 0

    def __init__(self):
        Counter.total += 1
        self.total = 100

Counter(); Counter()
print(Counter.total, Counter().total, Counter.total)
"""
A["8"] = ""


D["9"] = """
class Box:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]

b = Box([3, 1, 2])
print(len(b), b[-1], sorted(b), 1 in b)
"""
A["9"] = ""


D["10"] = """
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        print("B init")

class C(B):
    def __init__(self):
        super().__init__()
        print("C init")

C()
"""
A["10"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from drill import run

    run(D, A, __file__)
