# Подготовка к интервью: Python core и live coding

Работаем так:
1. Открываешь урок в `lessons/`, запускаешь его (`python lessons/lesson_01_references.py`) и читаешь комментарии.
2. Открываешь задачу в `tasks/`, пишешь решение вместо `raise NotImplementedError`.
3. Проверяешь: `pytest -k task_02 -q` (одна задача) или `pytest -q` (все).
4. Пишешь в чат "готово task_02", Claude смотрит код и разбирает.

Папка `solutions/` с эталонными решениями. Не открывай её, пока не решишь сам.

Запуск тестов из папки модуля:
    cd module_1_types
    pytest -q
