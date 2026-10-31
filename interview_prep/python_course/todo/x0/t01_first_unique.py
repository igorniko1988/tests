"""X0 t01 (алгоритм, 20 минут). Первый неповторяющийся символ.

Верни индекс первого символа строки, который встречается в ней ровно один раз.
Если такого нет — верни -1.

first_unique("leetcode")      -> 0    # "l"
first_unique("loveleetcode")  -> 2    # "v"
first_unique("aabb")          -> -1
first_unique("")              -> -1

Регистр важен: "a" и "A" — разные символы.
Засеки время. После решения назови сложность по времени и памяти.

Проверка (из папки interview_prep/python_course/todo):  uv run pytest tests/test_x0.py -k t01
"""


def first_unique(s: str) -> int:
    raise NotImplementedError
