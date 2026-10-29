"""C2 t07 (разминка, 5 мин). Первое значение, которое не None.

Теория: interview_prep/python_course/c02_numbers_strings/s07_truthy/THEORY.md (раздел 7: ловушка `x or default`).

ЗАЧЕМ ЭТО
В конфиге фреймворка значение берут «из аргумента, иначе из переменной окружения, иначе
по умолчанию». Если сделать это через or, то timeout=0 или пустой префикс "" молча
заменятся значением по умолчанию. Это реальный баг тестовых фреймворков.

УСЛОВИЕ
coalesce(*values, default=None) -> значение
- Вернуть первое из values, которое НЕ None — даже если оно falsy (0, "", [], False).
- Если все None или values пусто — вернуть default.

ПРИМЕРЫ (разбор)
    coalesce(None, 0, 5)          → 0       # 0 — не None, его и возвращаем
    coalesce(None, "", "x")       → ""
    coalesce(None, None)          → None
    coalesce(None, default=1)     → 1
    coalesce(False, True)         → False

ТЕРМИНЫ
- *values — все позиционные аргументы собираются в кортеж (подробно в C4).
- default=None после *values — аргумент, который можно передать только по имени.

ПОСЛЕ РЕШЕНИЯ ответь в чат: что вернёт `None or 0 or 5` и почему это не годится здесь?

Проверка (из папки priority_c1_c2):  uv run pytest -k c2_t07
"""


def coalesce(*values, default=None):
    raise NotImplementedError
