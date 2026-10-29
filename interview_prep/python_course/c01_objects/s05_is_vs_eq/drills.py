"""C1 · Раздел 5. is и == — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s05_is_vs_eq/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"5.4", "5.6"}  # доп. фрагменты: можно пропустить


D["5.1"] = """
a = [1, 2]
b = [1, 2]
c = a
print(a == b, a is b, a is c)
"""
A["5.1"] = "True, False, True"


D["5.2"] = """
class AlwaysEqual:
    def __eq__(self, other):
        return True

x = AlwaysEqual()
print(x == None, x is None)
"""
A["5.2"] = "True, False"


D["5.3"] = """
a = int("1000")
b = int("1000")
print(a == b, a is b)
"""
A["5.3"] = "True, False"


# доп. — по желанию
D["5.4"] = """
a = int("100")
b = int("100")
print(a is b)
"""
A["5.4"] = "True"


D["5.5"] = """
a = [1]
b = a[:]
print(a == b, a is not b)
"""
A["5.5"] = "True, True"


# доп. — по желанию
D["5.6"] = """
t1 = (1, [2])
t2 = (1, [2])
print(t1 == t2, t1 is t2)
"""
A["5.6"] = "True, False"


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
