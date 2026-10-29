"""C1 · Раздел 7. Изменяемый аргумент по умолчанию — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s07_default_arg/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"7.2", "7.6", "7.7"}  # доп. фрагменты: можно пропустить


D["7.1"] = """
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

r1 = add(1)
r2 = add(2)
print(r1, r1 is r2)
"""
A["7.1"] = "[1], False"


# доп. — по желанию
D["7.2"] = """
def f(x=print("def!")):
    pass

print("call")
f()
f()
"""
A["7.2"] = ""


D["7.3"] = """
def add(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

add(1)
print(add(2))
"""
A["7.3"] = "[2]"


D["7.4"] = """
def f(d={}):
    d["n"] = d.get("n", 0) + 1
    return d["n"]

f()
f()
print(f())
"""
A["7.4"] = "3"


D["7.5"] = """
def f(lst=[]):
    lst.append(1)
    return lst

f()
print(f([5]), f())
"""
A["7.5"] = "[1,5,1]"


# доп. — по желанию
D["7.6"] = """
def f(x=[]):
    x.append(0)

f()
f()
print(f.__defaults__)
"""
A["7.6"] = ""


# доп. — по желанию
D["7.7"] = """
from dataclasses import dataclass

@dataclass
class User:
    roles: list = []

print(User())
"""
A["7.7"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
