"""C2 · Раздел 3. Decimal — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через пробел, строки без кавычек;
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c02_numbers_strings): uv run python s03_decimal/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"3.3", "3.5", "3.8"}  # доп. фрагменты: можно пропустить


D["3.1"] = """
from decimal import Decimal
print(Decimal(0.1))
"""
A["3.1"] = ""


D["3.2"] = """
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))
"""
A["3.2"] = "'0.3'"


# доп. — по желанию
D["3.3"] = """
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
"""
A["3.3"] = ""


D["3.4"] = """
from decimal import Decimal, ROUND_HALF_UP
x = Decimal("2.665")
print(x.quantize(Decimal("0.01")), x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
"""
A["3.4"] = ""


# доп. — по желанию
D["3.5"] = """
from decimal import Decimal
print(Decimal("1.10") * 3)
"""
A["3.5"] = ""


D["3.6"] = """
from decimal import Decimal
print(Decimal("1.5") + 0.5)
"""
A["3.6"] = ""


D["3.7"] = """
from decimal import Decimal
print(str(Decimal("10.50")), float(Decimal("10.50")))
"""
A["3.7"] = ""


# доп. — по желанию
D["3.8"] = """
from decimal import Decimal
print(Decimal("2.50") == Decimal("2.5"))
"""
A["3.8"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
