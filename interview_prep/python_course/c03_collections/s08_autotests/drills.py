"""C3 · Раздел 8. коллекции в автотестах — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c03_collections): uv run python s08_autotests/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["8.1"] = """
order = {"id": 7, "side": "BUY", "status": "NEW"}
expected = {"side": "BUY", "status": "NEW"}
print(expected.items() <= order.items(), {"id", "price"} <= order.keys())
"""
A["8.1"] = ""


D["8.2"] = """
expected = {1, 2, 3}
actual = {2, 3, 4}
print(sorted(expected - actual), sorted(actual - expected))
"""
A["8.2"] = ""


D["8.3"] = """
from collections import Counter
ids = [1, 2, 2, 3, 3, 3]
print(len(ids) == len(set(ids)), [x for x, n in Counter(ids).items() if n > 1])
"""
A["8.3"] = ""


D["8.4"] = """
orders = [{"id": 1, "s": "NEW"}, {"id": 2, "s": "FILLED"}]
by_id = {o["id"]: o for o in orders}
print(by_id[2]["s"], 3 in by_id)
"""
A["8.4"] = ""


D["8.5"] = """
prices = ["9.50", "100.00", "10.00"]
print(prices == sorted(prices, reverse=True))
"""
A["8.5"] = ""


D["8.6"] = """
from decimal import Decimal
prices = ["9.50", "100.00", "10.00"]
print(prices == sorted(prices, key=Decimal, reverse=True))
"""
A["8.6"] = ""


D["8.7"] = """
a = [3, 1, 2]
print(all(x <= y for x, y in zip(a, a[1:])))
"""
A["8.7"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
