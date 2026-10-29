"""C1 · Раздел 3. Изменяемые и неизменяемые объекты — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s03_mutability/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["3.1"] = """
s = " Bob "
s.strip()
print(repr(s))
"""
A["3.1"] = ""


D["3.2"] = """
n = [2, 1]
r = n.append(3)
print(n, r)
"""
A["3.2"] = ""


D["3.3"] = """
t = (1, [2])
t[1].extend([3])
print(t)
"""
A["3.3"] = ""


D["3.4"] = """
t = (1, [2])
t[1] = [5]
print(t)
"""
A["3.4"] = ""


D["3.5"] = """
w = "abc"
v = w.replace("a", "x")
print(w, v)
"""
A["3.5"] = ""


D["3.6"] = """
x = 10
y = x
x += 1
print(x, y)
"""
A["3.6"] = ""


D["3.7"] = """
t = ([],)
t[0].append(1)
print(t)
"""
A["3.7"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
