"""C9 · Магические методы и dataclasses — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки interview_prep/python_course/week3/c09_magic_methods): uv run python drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {'11', '12', '13', '14'}  # доп. фрагменты: можно пропустить


D["1"] = """
class P:
    def __repr__(self):
        return "P()"

    def __str__(self):
        return "p"

print(P(), [P()], f"{P()!r}")
"""
A["1"] = ""


D["2"] = """
class P:
    def __repr__(self):
        return "P()"

print(str(P()), P())
"""
A["2"] = ""


D["3"] = """
class A:
    def __init__(self, v):
        self.v = v

print(A(1) == A(1), A(1) is A(1))
"""
A["3"] = ""


D["4"] = """
class A:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

print(A(1) == A(1))
print({A(1)})
"""
A["4"] = ""


D["5"] = """
class A:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

    def __hash__(self):
        return hash(self.v)

print(len({A(1), A(1), A(2)}))
"""
A["5"] = ""


D["6"] = """
class V:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):
        return V(self.x + other.x)

    def __repr__(self):
        return f"V({self.x})"

print(V(1) + V(2))
print(sum([V(1), V(2)]))
"""
A["6"] = ""


D["7"] = """
class Box:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

print(len(Box([1, 2])), bool(Box([])), bool(Box([0])))
"""
A["7"] = ""


D["8"] = """
class Seq:
    def __getitem__(self, i):
        if i >= 3:
            raise IndexError
        return i * 10

print(list(Seq()), 20 in Seq())
"""
A["8"] = ""


D["9"] = """
from functools import total_ordering

@total_ordering
class Ver:
    def __init__(self, s):
        self.p = tuple(map(int, s.split(".")))

    def __eq__(self, o):
        return self.p == o.p

    def __lt__(self, o):
        return self.p < o.p

print(Ver("1.10") > Ver("1.9"), "1.10" > "1.9")
"""
A["9"] = ""


D["10"] = """
from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    qty: int = 1

print(Order("BTC"), Order("BTC") == Order("BTC", 1))
"""
A["10"] = ""


# доп. — по желанию
D["11"] = """
from dataclasses import dataclass

@dataclass
class O:
    qty: int

print(O(qty="lots"))
"""
A["11"] = ""


# доп. — по желанию
D["12"] = """
from dataclasses import dataclass

@dataclass(frozen=True)
class P:
    x: int

p = P(1)
print(hash(p) == hash(P(1)))
p.x = 2
"""
A["12"] = ""


# доп. — по желанию
D["13"] = """
class S:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
        return cls._inst

    def __init__(self):
        print("init")

print(S() is S())
"""
A["13"] = ""


# доп. — по желанию
D["14"] = """
class Mul:
    def __init__(self, k):
        self.k = k

    def __call__(self, x):
        return x * self.k

triple = Mul(3)
print(triple(4), callable(triple), callable(3))
"""
A["14"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
