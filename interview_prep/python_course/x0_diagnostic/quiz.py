"""X0. Диагностика, часть 1: «что выведет» (15 фрагментов, ~20 минут).

Правила:
1. Читаешь фрагмент и пишешь ответ внизу файла в ANSWERS. НЕ запускаешь.
2. Не знаешь — пиши "?" или свою догадку. Это диагностика: ошибки нужны, по ним строим курс.
3. Когда все 15 ответов написаны — пиши в чат «готово X0 quiz». Проверим вместе.

Запустить один фрагмент (только ПОСЛЕ ответа):
    uv run python quiz.py 4
Если фрагмент падает с ошибкой, ответ — название исключения (например, TypeError).
"""

import sys

SNIPPETS = {
    1: """
a = [1, 2, 3]
b = a
b += [4]
print(a)
""",
    2: """
t = (1, [2])
try:
    t[1] += [3]
except TypeError:
    print("err")
print(t)
""",
    3: """
def f(x, acc=[]):
    acc.append(x)
    return acc

f(1)
print(f(2))
""",
    4: """
fs = [lambda: i for i in range(3)]
print([f() for f in fs])
""",
    5: """
print(0.1 + 0.2 == 0.3, round(2.5), round(3.5))
""",
    6: """
grid = [[0] * 2] * 2
grid[0][0] = 1
print(grid)
""",
    7: """
g = (x * x for x in range(3))
print(sum(g), sum(g))
""",
    8: """
d = {True: "a", 1: "b", 1.0: "c"}
print(d)
""",
    9: """
class A:
    items = []

a1, a2 = A(), A()
a1.items.append(1)
print(a2.items)
""",
    10: """
class A:
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B" + super().who()

class C(A):
    def who(self):
        return "C" + super().who()

class D(B, C):
    pass

print(D().who())
""",
    11: """
def f():
    try:
        return 1
    finally:
        return 2

print(f())
""",
    12: """
print(type(True + True), True + True)
""",
    13: """
x = 10

def f():
    print(x)
    x = 5

f()
""",
    14: """
s = "abc"
print(s[::-1], s[5:], s[-1])
""",
    15: """
nums = [3, 1, 2]
r = nums.sort()
print(r, sorted(nums, reverse=True))
""",
}

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(SNIPPETS[n].strip(), "\n--- вывод ---")
    try:
        exec(SNIPPETS[n], {})
    except Exception as e:  # noqa: BLE001
        print(type(e).__name__, e)


# ============================ ТВОИ ОТВЕТЫ ============================
# Пиши, что напечатается (точно, со скобками и кавычками) или имя исключения.

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
