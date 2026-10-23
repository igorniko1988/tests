"""Задача 2. Первый неповторяющийся символ.

first_unique("swiss") -> "w"
first_unique("aabb")  -> None
first_unique("")      -> None

Подсказка: сначала посчитай, сколько раз встречается каждый символ.
Подумай, какая получится сложность.

Проверка: pytest -k task_02 -q
"""


def first_unique(s):
    counts_symbols = {}
    for symbol in s:
        counts_symbols[symbol] = counts_symbols.get(symbol, 0) + 1

    for symbol,count in counts_symbols.items():
        if count == 1:
            return symbol
    return None

print(first_unique('swiss'))