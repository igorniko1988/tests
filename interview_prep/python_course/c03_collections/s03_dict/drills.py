"""C3 · Раздел 3. dict — хеш-таблица — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c03_collections): uv run python s03_dict/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"3.5", "3.7", "3.8", "3.9"}  # доп. фрагменты: можно пропустить


D["3.1"] = """
d = {1: "int", 1.0: "float", True: "bool"}
print(d)
"""
A["3.1"] = ""


D["3.2"] = """
order = {"id": 7, "status": "NEW"}
print(order.get("price"), order.get("price", "0"), "NEW" in order)
"""
A["3.2"] = ""


D["3.3"] = """
order = {"id": 7}
print(order["price"])
"""
A["3.3"] = ""


D["3.4"] = """
d = {"x": 1, "y": 2}
d["x"] = 10
del d["y"]
d["y"] = 3
print(list(d))
"""
A["3.4"] = ""


# доп. — по желанию
D["3.5"] = """
print({"a": 1, "b": 2} == {"b": 2, "a": 1})
"""
A["3.5"] = ""


D["3.6"] = """
d = {"a": 1, "b": 0}
for k in d:
    if d[k] == 0:
        del d[k]
"""
A["3.6"] = ""


# доп. — по желанию
D["3.7"] = """
prices = {"BTC": 100}
keys = prices.keys()
prices["ETH"] = 5
print(keys)
"""
A["3.7"] = ""


# доп. — по желанию
D["3.8"] = """
d = {"a": 1}
m = d | {"a": 2, "b": 3}
print(d, m)
"""
A["3.8"] = ""


# доп. — по желанию
D["3.9"] = """
d = {}
d.setdefault("tags", []).append("x")
d.setdefault("tags", []).append("y")
print(d)
"""
A["3.9"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
