"""C1 · Раздел 2. Переменная — это имя, а не коробка — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s02_names/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["2.1"] = """
a = [1]
b = a
a.append(2)
a = [7]
print(a, b)
"""
A["2.1"] = "[7], [1,2]"


D["2.2"] = """
x = {"n": 1}
y = x
y["n"] += 1
print(x)
"""
A["2.2"] = "{'n': 2}"


D["2.3"] = """
s = "hi"
t = s
t = t.upper()
print(s, t)
"""
A["2.3"] = "'hi','HI!'"


D["2.4"] = """
data = [1, 2]
backup = data
data.clear()
print(backup)
"""
A["2.4"] = "[]"


D["2.5"] = """
p = [1]
q = p
del p
print(q)
"""
A["2.5"] = "[1]"


D["2.6"] = """
u = [0]
v = u
v = [0]
print(u is v, u == v)
"""
A["2.6"] = "False, True"


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
