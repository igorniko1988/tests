"""C3 · Раздел 2. tuple и распаковка — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c03_collections): uv run python s02_tuple/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["2.1"] = """
a = (1)
b = (1,)
c = 1,
print(type(a).__name__, type(b).__name__, type(c).__name__)
"""
A["2.1"] = ""


D["2.2"] = """
t = ("NEW")
print(len(t), [s for s in t])
"""
A["2.2"] = ""


D["2.3"] = """
head, *rest = (1, 2, 3)
print(head, rest)
"""
A["2.3"] = ""


D["2.4"] = """
x, y = [1, 2, 3]
"""
A["2.4"] = ""


D["2.5"] = """
a, b = 1, 2
a, b = b, a + b
print(a, b)
"""
A["2.5"] = ""


D["2.6"] = """
t = (1, [2])
t[1].append(3)
print(t)
"""
A["2.6"] = ""


D["2.7"] = """
print(hash((1, [2])))
"""
A["2.7"] = ""


D["2.8"] = """
expected = {"id": 1},
print(type(expected).__name__, expected == {"id": 1})
"""
A["2.8"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
