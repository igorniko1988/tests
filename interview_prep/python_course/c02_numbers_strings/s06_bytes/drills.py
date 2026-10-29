"""C2 · Раздел 6. str и bytes — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через пробел, строки без кавычек;
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c02_numbers_strings): uv run python s06_bytes/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["6.1"] = """
print(len("привет"), len("привет".encode("utf-8")))
"""
A["6.1"] = ""


D["6.2"] = """
print("hi".encode())
"""
A["6.2"] = ""


D["6.3"] = """
print(b"hi" == "hi")
"""
A["6.3"] = ""


D["6.4"] = r"""
print(b"\xd0\xbf".decode("utf-8"))
"""
A["6.4"] = ""


D["6.5"] = r"""
print(b"\xff".decode("utf-8"))
"""
A["6.5"] = ""


D["6.6"] = r"""
print(b"a\xffb".decode("utf-8", errors="replace"))
"""
A["6.6"] = ""


D["6.7"] = """
print(b"abc"[0], list(b"ab"))
"""
A["6.7"] = ""


D["6.8"] = """
print("€".encode("utf-8"))
"""
A["6.8"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
