"""t02 (разминка, 7 мин). Сжатие строки (Run-Length Encoding).

Подряд идущие одинаковые символы заменяются на символ и количество.

compress("aaabcc")  -> "a3b1c2"
compress("abc")     -> "a1b1c1"
compress("aabaa")   -> "a2b1a2"   # считаем только ПОДРЯД идущие
compress("")        -> ""

Без itertools.groupby (потом можно показать и его). O(n).
"""


def compress(s: str) -> str:
    raise NotImplementedError
