"""C1. «Что выведет» — 15 фрагментов.

Правила:
1. Пиши ответ в ANSWERS внизу файла ДО запуска фрагмента.
2. Потом проверяй:  uv run python quiz.py 4      (один)
                    uv run python quiz.py all    (все подряд)
3. Если фрагмент падает, ответ — имя исключения (TypeError и т. п.).
4. Зачёт урока: не меньше 12 из 15 до запуска. Пиши в чат «готово C1 quiz».
"""

import sys

SNIPPETS = {
    1: """
a = [1, 2]
b = a[:]
b.append(3)
print(a, a is b)
""",
    2: """
s = "hi"
t = s
t += "!"
print(s, t)
""",
    3: """
x = [1]
y = x
x = x + [2]
print(y)
""",
    4: """
x = [1]
y = x
x += [2]
print(y)
""",
    5: """
a = [[1]] * 2
a[0].append(2)
print(a)
""",
    6: """
a = [[1]] * 2
a[0] = [9]
print(a)
""",
    7: """
import copy
src = {"k": [1]}
c = dict(src)
d = copy.deepcopy(src)
src["k"].append(2)
print(c["k"], d["k"])
""",
    8: """
def f(n, seen=set()):
    seen.add(n)
    return len(seen)

f(1)
f(2)
print(f(1))
""",
    9: """
def f(lst):
    lst = lst + [1]
    return lst

a = [0]
f(a)
print(a)
""",
    10: """
def f(lst):
    lst += [1]

a = [0]
f(a)
print(a)
""",
    11: """
print([] is [], [] == [], None is None)
""",
    12: """
t = ([],)
t[0].append(1)
print(t)
""",
    13: """
d = {1: "a", 1.0: "b"}
print(d, len(d))
""",
    14: """
print(hash((1, 2)) == hash((1, 2)))
print(hash((1, [2])))
""",
    15: """
from unittest.mock import Mock
m = Mock()
payload = {"qty": 1}
m(payload)
payload["qty"] = 5
print(m.call_args)
""",
}


def run(n: int) -> None:
    print(f"#{n}", SNIPPETS[n].rstrip(), "\n--- вывод ---", sep="")
    try:
        exec(SNIPPETS[n], {})
    except Exception as e:  # noqa: BLE001
        print(type(e).__name__ + ":", e)
    print()


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    for n in SNIPPETS if arg == "all" else [int(arg)]:
        run(n)


# ============================ ТВОИ ОТВЕТЫ ============================
# Пиши точный вывод (со скобками и кавычками) или имя исключения.
# Если строк вывода несколько — через " | ".

ANSWERS = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
    11: "",
    12: "",
    13: "",
    14: "",
    15: "",
}
