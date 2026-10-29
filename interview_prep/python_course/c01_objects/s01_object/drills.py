"""C1 · Раздел 1. Что такое объект — упражнения «что выведет».

Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s01_object/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы


D["1.1"] = """
a = [1, 2]
b = [1, 2]
print(a == b, id(a) == id(b))
"""
A["1.1"] = "True, False"


D["1.2"] = """
nums = [3, 1, 2]
before = id(nums)
nums.sort()
print(nums, id(nums) == before)
"""
A["1.2"] = "[1,2,3], True"


D["1.3"] = """
nums = [3, 1, 2]
before = id(nums)
nums = sorted(nums)
print(nums, id(nums) == before)
"""
A["1.3"] = "[1,2,3], False"


D["1.4"] = """
d = {"k": 1}
before = id(d)
d["k"] = 2
d["n"] = 3
print(d, id(d) == before)
"""
A["1.4"] = "{'k': 2, 'n': 3}, True"


D["1.5"] = """
x = 5
x = "5"
print(type(x))
"""
A["1.5"] = "string"


D["1.6"] = """
print(type(type(5)), type(print))
"""
A["1.6"] = "type, print"


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__)
