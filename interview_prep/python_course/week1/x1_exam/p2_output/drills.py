"""X1 · Часть 2. «Что выведет» — 10 фрагментов по C1–C3. Время: 15 минут.

Впиши ответ в A[...] под каждым фрагментом ДО запуска, без IDE и без интерпретатора:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ, строки без кавычек,
    внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Зачёт: 8 из 10.
Проверка (из папки interview_prep/python_course/week1/x1_exam): uv run python p2_output/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["1"] = """
a = [1, 2]
b = [a, a]
a.append(3)
print(b)
"""
A["1"] = ""


D["2"] = """
def f(x, acc=[]):
    acc.append(x)
    return len(acc)

print(f(1), f(2), f(3, []))
"""
A["2"] = ""


D["3"] = """
t = (1, 2, [3])
try:
    t[2] += [4]
except TypeError:
    print("error")
print(t)
"""
A["3"] = ""


D["4"] = """
print(0.1 + 0.2 == 0.3, round(2.5), round(3.5))
"""
A["4"] = ""


D["5"] = """
s = "Hello"
print(s[::-1], s[1:-1], s * 0 == "")
"""
A["5"] = ""


D["6"] = """
print(bool("0"), bool([]), None or "x", 0 and 1 / 0)
"""
A["6"] = ""


D["7"] = """
d = {1: "a", True: "b", 1.0: "c"}
print(d)
"""
A["7"] = ""


D["8"] = """
from collections import Counter
print(Counter("abracadabra").most_common(2))
"""
A["8"] = ""


D["9"] = """
d = {"a": 1, "b": 2}
for k in d:
    d[k + "!"] = 0
print(d)
"""
A["9"] = ""


D["10"] = """
data = [("b", 2), ("a", 2), ("c", 1)]
print(sorted(data, key=lambda x: -x[1])[0], max(data, key=lambda x: x[1]))
"""
A["10"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from drill import run

    run(D, A, __file__)
