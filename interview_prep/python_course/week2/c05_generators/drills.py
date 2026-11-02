"""C5 · Comprehensions, итераторы, генераторы — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print: аргументы через ПРОБЕЛ (без запятых между ними),
    строки без кавычек, а внутри списков и словарей — как Python: [1, 2], {'a': 1};
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки interview_prep/python_course/week2/c05_generators): uv run python drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {'12', '13', '14', '15', '16'}  # доп. фрагменты: можно пропустить


D["1"] = """
nums = [1, 2, 3, 4]
print([x * 10 for x in nums if x % 2], ["e" if x % 2 == 0 else "o" for x in nums])
"""
A["1"] = ""


D["2"] = """
print({x % 3 for x in range(10)}, {x: x * x for x in range(3)})
"""
A["2"] = ""


D["3"] = """
it = iter([1, 2])
print(next(it), next(it), next(it, "end"))
"""
A["3"] = ""


D["4"] = """
gen = (x * x for x in range(3))
print(list(gen), list(gen))
"""
A["4"] = ""


D["5"] = """
def gen():
    print("start")
    yield 1
    print("middle")
    yield 2

g = gen()
print("created")
print(next(g))
"""
A["5"] = ""


D["6"] = """
def gen():
    yield 1
    return 5
    yield 2

print(list(gen()))
"""
A["6"] = ""


D["7"] = """
nums = [1, 2, 3]
squares = (x * x for x in nums)
nums.append(4)
print(sum(squares))
"""
A["7"] = ""


D["8"] = """
gen = (x for x in range(5))
print(3 in gen, list(gen))
"""
A["8"] = ""


D["9"] = """
print(len(x for x in "abc"))
"""
A["9"] = ""


D["10"] = """
from itertools import groupby
print([(k, len(list(g))) for k, g in groupby("aabaa")])
"""
A["10"] = ""


D["11"] = """
def flat(items):
    for x in items:
        if isinstance(x, list):
            yield from flat(x)
        else:
            yield x

print(list(flat([1, [2, [3]], 4])))
"""
A["11"] = ""


# доп. — по желанию
D["12"] = """
x = "outer"
squares = [x for x in range(3)]
print(x, squares)
"""
A["12"] = ""


# доп. — по желанию
D["13"] = """
m = map(str.upper, ["a", "b"])
print(m == ["A", "B"], list(m) == ["A", "B"])
"""
A["13"] = ""


# доп. — по желанию
D["14"] = """
from itertools import islice, count
print(list(islice(count(10, 5), 3)))
"""
A["14"] = ""


# доп. — по желанию
D["15"] = """
print(list(zip("abc", [1, 2])), dict(zip("ab", range(5))))
"""
A["15"] = ""


# доп. — по желанию
D["16"] = """
def counter():
    n = 0
    while True:
        n += 1
        yield n

c = counter()
print([next(c) for _ in range(3)], next(c))
"""
A["16"] = ""

# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
