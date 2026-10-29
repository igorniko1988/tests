"""C3 · Раздел 5. Counter и defaultdict — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c03_collections): uv run python s05_counter_defaultdict/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["5.1"] = """
from collections import Counter
c = Counter("banana")
print(c.most_common(2), c["z"], len(c))
"""
A["5.1"] = ""


D["5.2"] = """
from collections import Counter
print(Counter("abba").most_common(1), Counter("baab").most_common(1))
"""
A["5.2"] = ""


D["5.3"] = """
from collections import Counter
print(Counter([1, 2, 2]) == Counter([2, 1, 2]), Counter([1, 2]) == Counter([1, 2, 2]))
"""
A["5.3"] = ""


D["5.4"] = """
from collections import Counter
a = Counter(x=3, y=1)
b = Counter(x=1, y=2)
print(a - b)
"""
A["5.4"] = ""


D["5.5"] = """
from collections import defaultdict
g = defaultdict(list)
g["NEW"].append(1)
g["NEW"].append(3)
g["FILLED"].append(2)
print(dict(g))
"""
A["5.5"] = ""


D["5.6"] = """
from collections import defaultdict
d = defaultdict(int)
d["a"] += 1
if d["b"]:
    pass
print(dict(d))
"""
A["5.6"] = ""


D["5.7"] = """
from collections import defaultdict
d = defaultdict(list)
print(d.get("x"), "x" in d, len(d))
"""
A["5.7"] = ""


D["5.8"] = """
from collections import defaultdict
d = defaultdict([])
"""
A["5.8"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
