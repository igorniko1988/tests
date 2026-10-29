"""C1 · Раздел 8. Как передаются аргументы в функцию — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s08_passing/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"8.3", "8.5"}  # доп. фрагменты: можно пропустить


D["8.1"] = """
def change(lst, n):
    lst.append(1)
    lst = [0]
    n += 1

nums, k = [], 5
change(nums, k)
print(nums, k)
"""
A["8.1"] = "[1], 5"


D["8.2"] = """
def f(d):
    d["x"] = 1
    d = {}
    d["y"] = 2

data = {}
f(data)
print(data)
"""
A["8.2"] = "{'x':1}"


# доп. — по желанию
D["8.3"] = """
def f(s):
    s += "!"
    return s

a = "hi"
b = f(a)
print(a, b)
"""
A["8.3"] = ""


D["8.4"] = """
def f(lst):
    lst[:] = [9]

a = [1, 2]
f(a)
print(a)
"""
A["8.4"] = "[1,2]"


# доп. — по желанию
D["8.5"] = """
def f(lst):
    lst = sorted(lst)
    return lst

a = [3, 1]
f(a)
print(a)
"""
A["8.5"] = ""


D["8.6"] = """
def f(lst):
    lst.sort()

a = [3, 1]
print(f(a), a)
"""
A["8.6"] = "1,3"


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
