"""C1 · Раздел 6. Копирование: псевдоним, поверхностная и глубокая копия — упражнения «что выведет».

Обязательные — все фрагменты, кроме помеченных «# доп.» (их можно пропустить).
Впиши ответ в A[...] под каждым фрагментом ДО запуска:
  - точный вывод, как напечатает print (со скобками и кавычками);
  - несколько строк вывода — через " | ";
  - код падает — имя исключения: "TypeError".
Проверка (из папки c01_objects): uv run python s06_copy/drills.py
"""

D: dict[str, str] = {}  # фрагменты
A: dict[str, str] = {}  # твои ответы
OPTIONAL = {"6.2", "6.7", "6.8"}  # доп. фрагменты: можно пропустить


D["6.1"] = """
src = [[1, 2], [3]]
sh = src.copy()
src[0].append(9)
print(sh)
"""
A["6.1"] = "[[1,2,9],[3]"


# доп. — по желанию
D["6.2"] = """
src = [[1], [2]]
sh = list(src)
src.append([3])
print(len(sh))
"""
A["6.2"] = "2"


D["6.3"] = """
import copy
src = {"a": {"b": 1}}
dc = copy.deepcopy(src)
src["a"]["b"] = 2
print(dc)
"""
A["6.3"] = '{"a": {"b": 1}}'


D["6.4"] = """
grid = [[0] * 2] * 2
grid[1][0] = 5
print(grid)
"""
A["6.4"] = ""


D["6.5"] = """
grid = [[0] * 2 for _ in range(2)]
grid[1][0] = 5
print(grid)
"""
A["6.5"] = ""


D["6.6"] = """
d = dict.fromkeys(["x", "y"], [])
d["x"].append(1)
print(d)
"""
A["6.6"] = "{'x':[1],'y'=[]"


# доп. — по желанию
D["6.7"] = """
row = [0] * 3
row[0] = 7
print(row)
"""
A["6.7"] = "[7][0][0]"


# доп. — по желанию
D["6.8"] = """
import copy
inner = [1]
src = [inner, inner]
dc = copy.deepcopy(src)
dc[0].append(2)
print(dc, dc[0] is dc[1])
"""
A["6.8"] = "[[1,2],[1], False"


D["6.9"] = """
base = {"tags": ["a"]}
c = {**base}
c["tags"].append("b")
c["id"] = 1
print(base)
"""
A["6.9"] = "{'tags':['a','b'], ['id']: 1"


# ---------------------------- проверка — не трогай ----------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drill import run

    run(D, A, __file__, optional=OPTIONAL)
