"""C3 · Раздел 6. deque — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c03_collections): uv run python s06_deque/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["6.1"] = """
from collections import deque
q = deque([1, 2, 3])
q.appendleft(0)
q.append(4)
print(q.popleft(), q.pop(), list(q))
"""
A["6.1"] = ""


D["6.2"] = """
from collections import deque
last = deque(maxlen=3)
for e in "abcde":
    last.append(e)
print(list(last))
"""
A["6.2"] = ""


D["6.3"] = """
from collections import deque
q = deque([1, 2, 3], maxlen=3)
q.appendleft(0)
print(list(q))
"""
A["6.3"] = ""


D["6.4"] = """
from collections import deque
print(len(deque("abc")), len(deque(["abc"])))
"""
A["6.4"] = ""


D["6.5"] = """
from collections import deque
q = deque([1, 2])
q.extendleft([3, 4])
print(list(q))
"""
A["6.5"] = ""


D["6.6"] = """
from collections import deque
q = deque([1, 2, 3, 4])
q.rotate(1)
print(list(q))
"""
A["6.6"] = ""


D["6.7"] = """
from collections import deque
print(deque([1, 2, 3])[0:2])
"""
A["6.7"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
