"""Задача 5. Самые частые слова.

top_words(text, n=3) возвращает список из n пар (слово, сколько раз),
от частых к редким. Регистр игнорируем, знаки препинания не считаем частью слова.
Если частота равна, слово, встретившееся раньше, идёт первым.

top_words("the cat and the dog and the bird") ->
    [("the", 3), ("and", 2), ("cat", 1)]

Подсказка: re.findall(r"[a-z']+", text.lower()) и collections.Counter.

Проверка: pytest -k task_05 -q
"""


def top_words(text, n=3):
    raise NotImplementedError
