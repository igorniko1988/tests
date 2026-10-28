"""t02 (разминка, 7 мин). Сжатие строки (Run-Length Encoding).

Подряд идущие одинаковые символы заменяются на символ и количество.

compress("aaabcc")  -> "a3b1c2"
compress("abc")     -> "a1b1c1"
compress("aabaa")   -> "a2b1a2"   # считаем только ПОДРЯД идущие
compress("")        -> ""

Без itertools.groupby (потом можно показать и его). O(n).
"""


def compress(s: str) -> str:
    result = ''
    count = 0
    previous = None

    for symbol in s:
        if symbol == previous:
            count +=1
        else:
            if previous is None:
                previous = symbol
                count +=1
            else:
                result += previous + str(count)
                previous = symbol
                count = 1
    if previous is not None:
        result += previous + str(count)

    return result


print(compress('aabaa'))
