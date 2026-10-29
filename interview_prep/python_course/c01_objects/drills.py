"""C1. Практика по разделам теории — «что выведет».

Как работать:
1. Прочитал раздел N в THEORY.md → иди к блоку «Раздел N» ниже.
2. Под каждым фрагментом впиши ответ в A["N.M"] = "..." — ДО запуска.
   - точный вывод, как его напечатает print (со скобками и кавычками);
   - несколько строк вывода — через " | ";
   - если код падает — имя исключения: "TypeError".
3. Проверка (из папки c01_objects):
       uv run python drills.py 3      — раздел 3
       uv run python drills.py all    — все разделы
   Скрипт сам запустит код, сравнит с твоим ответом и покажет объяснение.
   Пока ответ пустой, правильный вывод не показывается — не подсмотришь.
"""

D: dict[str, str] = {}  # фрагменты кода
A: dict[str, str] = {}  # твои ответы

# ============================ Раздел 1. Что такое объект ============================

D["1.1"] = """
a = [1, 2]
b = [1, 2]
print(a == b, id(a) == id(b))
"""
A["1.1"] = ""

D["1.2"] = """
nums = [3, 1, 2]
before = id(nums)
nums.sort()
print(nums, id(nums) == before)
"""
A["1.2"] = ""

D["1.3"] = """
nums = [3, 1, 2]
before = id(nums)
nums = sorted(nums)
print(nums, id(nums) == before)
"""
A["1.3"] = ""

D["1.4"] = """
d = {"k": 1}
before = id(d)
d["k"] = 2
d["n"] = 3
print(d, id(d) == before)
"""
A["1.4"] = ""

D["1.5"] = """
x = 5
x = "5"
print(type(x))
"""
A["1.5"] = ""

D["1.6"] = """
print(type(type(5)), type(print))
"""
A["1.6"] = ""

# ===================== Раздел 2. Переменная — это имя, а не коробка =====================

D["2.1"] = """
a = [1]
b = a
a.append(2)
a = [7]
print(a, b)
"""
A["2.1"] = ""

D["2.2"] = """
x = {"n": 1}
y = x
y["n"] += 1
print(x)
"""
A["2.2"] = ""

D["2.3"] = """
s = "hi"
t = s
t = t.upper()
print(s, t)
"""
A["2.3"] = ""

D["2.4"] = """
data = [1, 2]
backup = data
data.clear()
print(backup)
"""
A["2.4"] = ""

D["2.5"] = """
p = [1]
q = p
del p
print(q)
"""
A["2.5"] = ""

D["2.6"] = """
u = [0]
v = u
v = [0]
print(u is v, u == v)
"""
A["2.6"] = ""

# ================== Раздел 3. Изменяемые и неизменяемые объекты ==================

D["3.1"] = """
s = " Bob "
s.strip()
print(repr(s))
"""
A["3.1"] = ""

D["3.2"] = """
n = [2, 1]
r = n.append(3)
print(n, r)
"""
A["3.2"] = ""

D["3.3"] = """
t = (1, [2])
t[1].extend([3])
print(t)
"""
A["3.3"] = ""

D["3.4"] = """
t = (1, [2])
t[1] = [5]
print(t)
"""
A["3.4"] = ""

D["3.5"] = """
w = "abc"
v = w.replace("a", "x")
print(w, v)
"""
A["3.5"] = ""

D["3.6"] = """
x = 10
y = x
x += 1
print(x, y)
"""
A["3.6"] = ""

D["3.7"] = """
t = ([],)
t[0].append(1)
print(t)
"""
A["3.7"] = ""


# ============================ запуск и проверка — не трогай ============================

import contextlib  # noqa: E402
import io  # noqa: E402
import sys  # noqa: E402


def actual_output(code: str) -> str:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {})
    except Exception as e:  # noqa: BLE001
        lines = buf.getvalue().splitlines()
        return " | ".join([*lines, type(e).__name__])
    return " | ".join(buf.getvalue().splitlines())


def normalize(text: str) -> str:
    return " | ".join(part.strip() for part in text.strip().split("|"))


def check(key: str) -> bool | None:
    try:
        from solutions.drills_explain import EXPLAIN
    except ImportError:
        EXPLAIN = {}
    print(f"── {key} " + "─" * 50, D[key].rstrip(), sep="")
    mine = A.get(key, "").strip()
    if not mine:
        print("   ответ не вписан — впиши A[" + repr(key) + "] и запусти снова\n")
        return None
    real = actual_output(D[key])
    ok = normalize(mine) == normalize(real)
    print(f"   твой ответ: {mine}")
    print(f"   на деле:    {real}")
    print("   ✅ верно" if ok else "   ❌ ошибка")
    if key in EXPLAIN:
        print("   почему:", EXPLAIN[key])
    print()
    return ok


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    keys = [k for k in D if arg == "all" or k.split(".")[0] == arg]
    results = [check(k) for k in keys]
    done = [r for r in results if r is not None]
    print(f"Итого: верно {sum(done)} из {len(done)}, не отвечено {results.count(None)}")
