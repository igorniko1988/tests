"""C1 t09 ★ (сложная, 20 мин). Глубокая копия с циклическими ссылками.

То же, что t08, но объект может ссылаться сам на себя:

a = [1]
a.append(a)            # a == [1, [...]]
b = deepcopy_cycles(a)
b is not a             -> True
b[1] is b              -> True     # цикл сохранён, но уже на копию
b[0] == 1              -> True

И если один объект встречается дважды, в копии он тоже один:
shared = [0]
src = [shared, shared]
dst = deepcopy_cycles(src)
dst[0] is dst[1]       -> True
dst[0] is not shared   -> True

Достаточно поддержать list и dict (+ простые значения).
Подсказка: так же делает copy.deepcopy — словарь memo {id(оригинала): копия}.

Проверка:  uv run pytest -k t09
"""


def deepcopy_cycles(obj, memo: dict | None = None):
    raise NotImplementedError
