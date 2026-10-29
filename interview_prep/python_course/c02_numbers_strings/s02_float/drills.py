"""C2 · Раздел 2. float — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через пробел, строки без кавычек;
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c02_numbers_strings): uv run python s02_float/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["2.1"] = """
print(0.1 + 0.2)
"""
A["2.1"] = ""


D["2.2"] = """
print(0.1 + 0.2 == 0.3)
"""
A["2.2"] = ""


D["2.3"] = """
import math
print(math.isclose(0.1 + 0.2, 0.3))
"""
A["2.3"] = ""


D["2.4"] = """
print(round(2.5), round(3.5), round(-0.5))
"""
A["2.4"] = ""


D["2.5"] = """
print(round(2.675, 2))
"""
A["2.5"] = ""


D["2.6"] = """
n = float("nan")
print(n == n, n != n)
"""
A["2.6"] = ""


D["2.7"] = """
print(1e308 * 10, -1e308 * 10)
"""
A["2.7"] = ""


D["2.8"] = """
total = 0.0
for _ in range(10):
    total += 0.1
print(total == 1.0, total)
"""
A["2.8"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
