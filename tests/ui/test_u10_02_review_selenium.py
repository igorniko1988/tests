"""U10. Урок 2 — ревью UI-тестов и Selenium на уровне собеседования.

Теория: practice/u10_02_review_selenium.md
Ревью: practice/u10_02_review_me.py
Запуск:
    uv run pytest tests/ui/test_u10_02_review_selenium.py -v

Задача 1. Финальное ревью — 30 минут.
    practice/u10_02_review_me.py: минимум 20 проблем, с уровнем (блокер / важно / мелочь) и ссылкой
    на урок, где это разбирали (каталог антипаттернов — раздел 2 теории).

Задача 2. Переписать.
    Тесты из review_me — здесь, на своём фреймворке (PO, компоненты, API-подготовка, фабрики, expect).
    Те же сценарии, но независимые, со своими данными, стабильные при -n 4 --count 3.

Задача 3. Ревью своего кода.
    Выбери 3 своих файла из U4–U9 и пройди по чек-листу из теории (раздел 1). Запиши замечания так, как
    оставил бы их в PR (файл:строка, что, чем грозит, как исправить). Исправь блокеры.

Задача 4. Гайдлайн команды (письменно, ui_framework/GUIDELINES.md).
    1–2 страницы: локаторы, ожидания, данные, PO, что нельзя, как писать тест, чек-лист PR.
    Это то, что ты принесёшь в новую команду (часть «Senior-навыков»).

Задача 5. Selenium на бумаге.
    Перепиши на Selenium (в «Ответах», без запуска) три теста: вход, пополнение с проверкой баланса,
    отмена ордера в строке таблицы. С WebDriverWait и expected_conditions, без implicit wait.
    Отметь места, где в Selenium пришлось бы бороться со StaleElementReferenceException (таблица перерисовывается
    раз в 2 с) и как.

Задача 6. Selenium в Docker (по желанию).
    docker run -d -p 4444:4444 --shm-size=2g --add-host=host.docker.internal:host-gateway selenium/standalone-chrome
    Тест через webdriver.Remote("http://localhost:4444"), base URL http://host.docker.internal:8080:
    регистрация и проверка email в шапке. Посмотри сессию на http://localhost:4444 (Grid UI).
    Локальный chromedriver на macOS 12 зависал при подготовке урока — поэтому через Docker.

Задача 7. Устно, по 2 минуты.
    «Чем Playwright лучше Selenium?» и «Когда вы бы выбрали Selenium?» — без подглядывания в таблицу.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как проводишь ревью UI-тестов?
    2. Чем implicit wait отличается от explicit?
    3. Что такое StaleElementReferenceException и почему её нет в Playwright?
    4. Что такое Selenium Grid?
    5. Почему Playwright, а не Selenium? Когда всё-таки Selenium?
"""

import pytest
from playwright.sync_api import expect

# Задача 2


# Задача 6


# Ответы
"""
Задача 3:

Задача 5:

Задача 7:

Собес:
"""
