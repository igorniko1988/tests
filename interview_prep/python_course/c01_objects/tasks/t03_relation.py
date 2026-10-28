"""C1 t03 (разминка, 5 мин). Тот же, равный или другой.

Верни:
- "same"      — если a и b это один и тот же объект;
- "equal"     — если это разные объекты с равными значениями;
- "different" — во всех остальных случаях.

x = [1]
relation(x, x)        -> "same"
relation([1], [1])    -> "equal"
relation([1], [2])    -> "different"
relation(None, None)  -> "same"

Проверка:  uv run pytest -k t03
"""


def relation(a, b) -> str:
    raise NotImplementedError
