# Модуль 3. Selenium (практика)

Страницы для тренировки лежат в `site/` и открываются **локально**, интернет не нужен.
Тесты сами поднимают маленький веб-сервер (фикстура `base_url` в `conftest.py`).

## Установка (один раз)
    uv add selenium pytest        # или: pip install selenium pytest

## Как работать
1. Читаешь шаг в чате.
2. Открываешь `tasks/task_NN_*.py`, пишешь код вместо `raise NotImplementedError`.
3. Запускаешь: `uv run pytest -k task_01 -q` (или `pytest -k task_01 -q`).
4. Видимое окно браузера: `pytest -k task_01 --headed`. По умолчанию браузер без окна.
5. Пишешь в чат "готово task_NN", разбираем вместе.

`solutions/` не открывать, пока не решишь сам.

## Параметры запуска
    --headed            показать окно браузера
    --browser chrome    chrome (по умолчанию) или firefox

## Страницы
- `site/login.html`   форма входа (логин `tomsmith`, пароль `SuperSecretPassword!`)
- `site/dynamic.html` элемент появляется через 2 секунды после клика (для ожиданий)
- `site/form.html`    поля, список, чекбоксы, таблица (для локаторов и действий)
