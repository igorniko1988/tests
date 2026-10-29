"""A0 · Раздел 1. Что такое Big-O — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска — обычно это число шагов или сравнений.
  - несколько строк вывода — через " | "; код падает — имя исключения.
Проверка (из папки a00_big_o): uv run python s01_what_is_big_o/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["1.1"] = """
n = 10
steps = 0
for i in range(n):
    steps += 1
for j in range(n):
    steps += 1
print(steps)
"""
A["1.1"] = ""


D["1.2"] = """
n = 10
steps = 0
for i in range(n):
    for j in range(n):
        steps += 1
print(steps)
"""
A["1.2"] = ""


D["1.3"] = """
n = 10
steps = 0
for i in range(n):
    for j in range(i + 1, n):
        steps += 1
print(steps)
"""
A["1.3"] = ""


D["1.4"] = """
n = 10
steps = 0
for i in range(n):
    for j in range(3):
        steps += 1
print(steps)
"""
A["1.4"] = ""


D["1.5"] = """
a = [1, 2, 3, 4, 5]
b = [1, 2, 3, 4]
steps = 0
for x in a:
    for y in b:
        steps += 1
print(steps)
"""
A["1.5"] = ""


D["1.6"] = """
items = [4, 8, 15, 16, 23, 42]
steps = 0
for x in items:
    steps += 1
    if x == 15:
        break
print(steps)
"""
A["1.6"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
