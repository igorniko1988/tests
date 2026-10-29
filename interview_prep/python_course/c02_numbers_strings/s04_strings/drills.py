"""C2 · Раздел 4. Строки — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через пробел, строки без кавычек;
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c02_numbers_strings): uv run python s04_strings/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["4.1"] = """
s = "pytest"
print(s[0], s[-1], s[1:3], s[::-1])
"""
A["4.1"] = ""


D["4.2"] = """
print("a,b,,c".split(","))
"""
A["4.2"] = ""


D["4.3"] = """
print("  a  b ".split())
"""
A["4.3"] = ""


D["4.4"] = """
print("-".join(["2026", "10", "29"]))
"""
A["4.4"] = ""


D["4.5"] = """
print("-".join([1, 2]))
"""
A["4.5"] = ""


D["4.6"] = """
print("abc".find("z"), "abc".index("c"))
"""
A["4.6"] = ""


D["4.7"] = """
print("abc".index("z"))
"""
A["4.7"] = ""


D["4.8"] = """
print("Hello".replace("l", "L", 1), "x" * 3)
"""
A["4.8"] = ""


D["4.9"] = """
print("ab" < "b", "Z" < "a", "10" < "9")
"""
A["4.9"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
