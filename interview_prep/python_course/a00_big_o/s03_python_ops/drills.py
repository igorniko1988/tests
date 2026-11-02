"""A0 · Раздел 3. Сколько стоят операции Python — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска — обычно это число шагов или сравнений.
  - несколько строк вывода — через " | "; код падает — имя исключения.
Проверка (из папки a00_big_o): uv run python s03_python_ops/drills.py
"""

# Общий код: выполняется перед КАЖДЫМ фрагментом. Item считает свои сравнения в calls.
SETUP = """
calls = 0


class Item:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):  # считаем каждое сравнение
        global calls
        calls += 1
        return self.v == other.v

    def __hash__(self):
        return hash(self.v)
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["3.1"] = """
items = [Item(i) for i in range(1000)]
Item(999) in items
print(calls)
"""
A["3.1"] = ""


D["3.2"] = """
items = [Item(i) for i in range(1000)]
Item(-1) in items
print(calls)
"""
A["3.2"] = ""


D["3.3"] = """
s = {Item(i) for i in range(1000)}
calls = 0
Item(999) in s
print(calls)
"""
A["3.3"] = ""


D["3.4"] = """
d = {Item(i): i for i in range(1000)}
calls = 0
Item(500) in d
print(calls)
"""
A["3.4"] = ""


D["3.5"] = """
d = {i: Item(i) for i in range(1000)}
Item(999) in d.values()
print(calls)
"""
A["3.5"] = ""


D["3.6"] = """
items = [Item(i) for i in range(1000)]
print(items.index(Item(10)), calls)
"""
A["3.6"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, setup=SETUP)
