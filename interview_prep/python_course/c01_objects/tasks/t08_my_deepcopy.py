"""C1 t08 (основная, 15 мин). Своя глубокая копия.

Без модуля copy напиши глубокую копию для list, dict, tuple, set и
«простых» значений (int, float, str, bool, None).
- результат равен исходному (==);
- каждый вложенный list / dict / set — новый объект (is not);
- изменения в копии не видны в оригинале и наоборот.

src = {"a": [1, {"b": [2]}], "c": (3, [4])}
dst = my_deepcopy(src)
dst["a"][1]["b"].append(99)
src["a"][1]["b"]   -> [2]

Проверка:  uv run pytest -k t08
"""


def my_deepcopy(obj):
    raise NotImplementedError
