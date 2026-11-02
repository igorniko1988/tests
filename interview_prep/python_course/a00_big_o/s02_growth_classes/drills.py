"""A0 · Раздел 2. Классы сложности — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска — обычно это число шагов или сравнений.
  - несколько строк вывода — через " | "; код падает — имя исключения.
Проверка (из папки a00_big_o): uv run python s02_growth_classes/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["2.1"] = """
n = 1024
steps = 0
while n > 1:
    n //= 2
    steps += 1
print(steps)
"""
A["2.1"] = ""


D["2.2"] = """
n = 1_000_000
steps = 0
while n > 1:
    n //= 2
    steps += 1
print(steps)
"""
A["2.2"] = ""


D["2.3"] = """
i = 1
steps = 0
while i < 100:
    i *= 2
    steps += 1
print(steps)
"""
A["2.3"] = ""


D["2.4"] = """
calls = 0


def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


fib(10)
print(calls)
"""
A["2.4"] = ""


D["2.5"] = """
from functools import cache

calls = 0


@cache
def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


fib(10)
print(calls)
"""
A["2.5"] = ""


D["2.6"] = """
n = 8
print(n * n, n * 3, 2 ** n)
"""
A["2.6"] = ""


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
