"""C3 · Раздел 7. сортировка — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c03_collections): uv run python s07_sorting/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["7.1"] = """
a = [3, 1, 2]
b = sorted(a)
print(a, b)
"""
A["7.1"] = ""


D["7.2"] = """
print(sorted("cab"), sorted({"b": 1, "a": 2}))
"""
A["7.2"] = ""


D["7.3"] = """
print(sorted(["10", "9", "100"]), sorted(["10", "9", "100"], key=int))
"""
A["7.3"] = ""


D["7.4"] = """
print(sorted(["banana", "apple", "Cherry"]))
"""
A["7.4"] = ""


D["7.5"] = """
data = [("b", 2), ("a", 2), ("c", 1)]
print(sorted(data, key=lambda x: x[1]))
"""
A["7.5"] = ""


D["7.6"] = """
users = [("ann", 5), ("bob", 9), ("cat", 9)]
print(sorted(users, key=lambda u: (-u[1], u[0])))
"""
A["7.6"] = ""


D["7.7"] = """
print(sorted([3, None, 1]))
"""
A["7.7"] = ""


D["7.8"] = """
print(sorted([3, None, 1], key=lambda x: (x is None, x)))
"""
A["7.8"] = ""


D["7.9"] = """
words = ["bb", "a", "ccc"]
print(max(words, key=len), min([], default="пусто"))
"""
A["7.9"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
