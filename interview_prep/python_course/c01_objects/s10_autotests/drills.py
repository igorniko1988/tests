"""C1 · Раздел 10. Где это ломает автотесты — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s10_autotests/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"10.5", "10.6"}  # доп. фрагменты: можно пропустить


D["10.1"] = """
from unittest.mock import Mock
m = Mock()
p = {"qty": 1}
m(dict(p))
p["qty"] = 5
print(m.call_args)
"""
A["10.1"] = ""


D["10.2"] = """
BASE = {"roles": ["user"]}

def make_admin():
    u = BASE.copy()
    u["roles"].append("admin")
    return u

make_admin()
print(BASE)
"""
A["10.2"] = ""


D["10.3"] = """
import copy
BASE = {"roles": ["user"]}

def make_admin():
    u = copy.deepcopy(BASE)
    u["roles"].append("admin")
    return u

make_admin()
print(BASE)
"""
A["10.3"] = ""


D["10.4"] = """
from unittest.mock import Mock
m = Mock()
items = [1]
m.send(items)
items.append(2)
m.send.assert_called_with([1])
print("ok")
"""
A["10.4"] = ""


# доп. — по желанию
D["10.5"] = """
import itertools
counter = itertools.count(1)

def make_order(n=next(counter)):
    return n

print(make_order(), make_order())
"""
A["10.5"] = ""


# доп. — по желанию
D["10.6"] = """
_cache = {}

def default_order():
    return _cache.setdefault("o", {"qty": "1"})

default_order()["qty"] = "0"
print(default_order())
"""
A["10.6"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
