"""C3. «Что выведет» — 15 фрагментов на весь урок.

Правила:
1. Пиши ответ в ANSWERS внизу файла ДО запуска фрагмента.
2. Потом проверяй:  uv run python quiz.py 4      (один)
                    uv run python quiz.py all    (все подряд)
3. Если фрагмент падает, ответ — имя исключения (TypeError и т. п.).
4. Зачёт урока: не меньше 12 из 15 до запуска. Пиши в чат «готово C3 quiz».
"""

import sys

SNIPPETS = {
    1: """
a = [1, 2, 3]
b = a
a += [4]
a = a + [5]
print(len(a), len(b))
""",
    2: """
a = [1, 2, 3]
print(a.reverse(), a[::-1])
""",
    3: """
a = [0, 0, 1, 0]
for x in a:
    if x == 0:
        a.remove(x)
print(a)
""",
    4: """
t = ([1], 2)
t[0] += [3]
""",
    5: """
first, *middle, last = "abcd"
print(first, middle, last)
""",
    6: """
d = {"a": 1}
d[True] = 2
d[1] = 3
print(d)
""",
    7: """
d = {"b": 1, "a": 2}
d["b"] = 5
print(list(d.items()))
""",
    8: """
users = {"ann": 1}
print(users.get("bob", 0) + users["ann"], "ann" in users.values())
""",
    9: """
a = {1, 2, 3}
a &= {2, 3, 4}
print(sorted(a), {} == set())
""",
    10: """
print(len({"a", "A", "a", "b"}), len(set("hello")))
""",
    11: """
from collections import Counter
c = Counter(["x", "y", "x"])
c["z"] += 0
print(c.most_common(), len(c))
""",
    12: """
from collections import defaultdict
d = defaultdict(set)
d["a"].add(1)
d["a"].add(1)
d["b"]
print({k: sorted(v) for k, v in d.items()})
""",
    13: """
from collections import deque
q = deque(maxlen=2)
q.extend([1, 2, 3])
q.appendleft(0)
print(list(q))
""",
    14: """
data = ["b10", "a2", "b9", "a10"]
print(sorted(data, key=lambda s: (s[0], int(s[1:]))))
""",
    15: """
nums = [5, 3, 9]
print(sorted(nums)[-1] == max(nums), nums.sort() == sorted(nums))
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
