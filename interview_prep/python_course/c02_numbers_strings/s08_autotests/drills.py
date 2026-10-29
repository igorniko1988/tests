"""C2 · Раздел 8. Где это ломает автотесты — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через пробел, строки без кавычек;
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c02_numbers_strings): uv run python s08_autotests/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"8.2", "8.3"}  # доп. фрагменты: можно пропустить


D["8.1"] = """
import json
print(json.loads('{"p": 0.1}')["p"] + 0.2)
"""
A["8.1"] = ""


# доп. — по желанию
D["8.2"] = """
import json
from decimal import Decimal
d = json.loads('{"p": 0.1}', parse_float=Decimal)
print(d["p"] + Decimal("0.2"))
"""
A["8.2"] = ""


# доп. — по желанию
D["8.3"] = """
import pytest
print(0.1 + 0.2 == pytest.approx(0.3))
"""
A["8.3"] = ""


D["8.4"] = """
resp = {"balance": "100.50"}
print(resp["balance"] == 100.5)
"""
A["8.4"] = ""


D["8.5"] = """
from decimal import Decimal
print(Decimal("100.50") == Decimal("100.5"), "100.50" == "100.5")
"""
A["8.5"] = ""


D["8.6"] = """
data = {"count": 0}
print(bool(data.get("count")), "count" in data)
"""
A["8.6"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
