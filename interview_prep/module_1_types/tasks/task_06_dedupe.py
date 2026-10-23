"""Задача 6. Убрать дубликаты, сохранив порядок.

dedupe([3, 1, 3, 2, 1]) -> [3, 1, 2]

Бонус: dedupe_dicts(items, key) для списка словарей, дубликат определяется
по значению ключа key. Остаётся первый встреченный.

dedupe_dicts([{"id": 1, "n": "a"}, {"id": 2, "n": "b"}, {"id": 1, "n": "c"}], "id")
    -> [{"id": 1, "n": "a"}, {"id": 2, "n": "b"}]

Проверка: pytest -k task_06 -q
"""


def dedupe(lst):
    raise NotImplementedError


def dedupe_dicts(items, key):
    raise NotImplementedError
