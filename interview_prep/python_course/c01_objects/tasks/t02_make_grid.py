"""C1 t02 (разминка, 5 мин). Сетка без общих строк.

Верни сетку rows × cols, заполненную fill. Строки должны быть РАЗНЫМИ списками:
изменение одной клетки не трогает другие строки.

make_grid(2, 3)        -> [[0, 0, 0], [0, 0, 0]]
make_grid(2, 2, ".")   -> [[".", "."], [".", "."]]
make_grid(0, 5)        -> []

Проверка:  uv run pytest -k t02
"""


def make_grid(rows: int, cols: int, fill=0) -> list[list]:
    raise NotImplementedError
