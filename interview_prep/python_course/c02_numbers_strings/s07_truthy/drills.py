"""C2 · Раздел 7. bool, truthy и falsy — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через пробел, строки без кавычек;
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c02_numbers_strings): uv run python s07_truthy/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"7.5", "7.7", "7.8"}  # доп. фрагменты: можно пропустить


D["7.1"] = """
print(bool(0), bool(""), bool([]), bool("0"), bool([0]))
"""
A["7.1"] = "False, False, False, True, True"


D["7.2"] = """
print(0 or "default", 5 or "default")
"""
A["7.2"] = "default, 5"


D["7.3"] = """
print(repr("" and "x"), "a" and "x")
"""
A["7.3"] = "'', 'x"


D["7.4"] = """
qty = 0
print(qty or 1)
"""
A["7.4"] = "1"


# доп. — по желанию
D["7.5"] = """
print(True + True, True == 1, isinstance(True, int))
"""
A["7.5"] = ""


D["7.6"] = """
print(None == False, not None)
"""
A["7.6"] = "False, "


# доп. — по желанию
D["7.7"] = """
x = 5
print(1 < x < 10, 1 < x > 3)
"""
A["7.7"] = ""


# доп. — по желанию
D["7.8"] = """
print([] == False, bool([]) == False)
"""
A["7.8"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
