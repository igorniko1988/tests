"""C1 · Раздел 4. a = a + b против a += b — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s04_plus_vs_iadd/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"4.5", "4.8"}  # доп. фрагменты: можно пропустить


D["4.1"] = """
a = [1]
b = a
a = a + [2]
print(a, b)
"""
A["4.1"] = "[1,2], [1]"


D["4.2"] = """
a = [1]
b = a
a += [2]
print(a, b)
"""
A["4.2"] = "[1,2], [1,2]"


D["4.3"] = """
s = "hi"
t = s
s += "!"
print(s, t)
"""
A["4.3"] = "'hi!', 'hi'"


D["4.4"] = """
a = [1]
a += "xy"
print(a)
"""
A["4.4"] = "[1,'x','y'"


# доп. — по желанию
D["4.5"] = """
a = [1]
a = a + "xy"
print(a)
"""
A["4.5"] = "Typerror"


D["4.6"] = """
t = (1, [2])
try:
    t[1] += [3]
except TypeError:
    print("error")
print(t)
"""
A["4.6"] = "'error'"


D["4.7"] = """
def add(lst):
    lst += [9]

data = [0]
add(data)
print(data)
"""
A["4.7"] = "[9]"


# доп. — по желанию
D["4.8"] = """
d = {"k": [1]}
v = d["k"]
v = v + [2]
print(d)
"""
A["4.8"] = "[1,2]"


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
