"""U1. Урок 3 — как устроен Playwright.

Теория: practice/u1_03_architecture.md
Здесь не pytest, а обычные скрипты: без фикстур видно, что они делают за тебя.
Запуск:  uv run python practice/u1_03_architecture.py
Каждую задачу оформи функцией task_N() и вызывай нужную внизу в if __name__ == "__main__".
Браузер везде: p.chromium.launch(channel="chrome").

Задача 1. Sync без pytest.
    sync_playwright → browser (headless=False, slow_mo=300) → context (base_url="http://localhost:8080")
    → page. Открой "/app/", зарегистрируй нового пользователя, выведи print'ом текст user-email.
    Закрой context и browser.

Задача 2. То же на async API.
    async_playwright, все вызовы с await, запуск через asyncio.run(...).

Задача 3. Заглянуть внутрь.
    Запусти задачу 1 с DEBUG=pw:api, затем с DEBUG=pw:protocol (в терминале, перед командой).
    Запиши в «Ответы»:
        - какие проверки Playwright делал перед кликом по "Зарегистрироваться" (pw:api);
        - названия CDP-методов: создание context, переход по адресу, клик мышью (pw:protocol;
          ищи grep'ом "method").

Задача 4. Профиль устройства.
    Создай context из p.devices["iPhone 13"], открой /app/, сделай скриншот
    page.screenshot(path="iphone.png"). Выведи page.viewport_size.

Задача 5. CDP-сессия.
    а) Выведи метрики Nodes и JSHeapUsedSize для /app/ (Performance.getMetrics).
    б) Замерь время page.goto("/app/") (time.perf_counter) обычно и с эмуляцией медленной сети
       (Network.emulateNetworkConditions, latency 500). Выведи оба числа.

Задача 6. gather против очереди.
    async: функция открывает новый context, страницу /app/, закрывает context.
    Замерь 5 вызовов через asyncio.gather и 5 вызовов по очереди. Сделай один «прогревочный»
    вызов перед замерами. Запиши результат в «Ответы» и объясни, почему он такой.

Задача 7. Ошибка sync внутри async.
    Внутри async def вызови sync_playwright(). Запиши текст ошибки и объясни, почему так.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Чем Playwright отличается от Selenium?
    2. Чем Playwright отличается от Cypress?
    3. Как устроен Playwright внутри?
    4. Почему Playwright не может работать с обычным Firefox или Safari?
    5. sync или async API — что выбираешь и почему?
    6. Что делать, если нужной возможности нет в API Playwright?
    7. Почему тесты на Playwright стабильнее?
"""

import asyncio
import time
from uuid import uuid4

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


# Задача 1


# Задача 2


# Задача 4


# Задача 5


# Задача 6


# Задача 7


if __name__ == "__main__":
    pass


# Ответы
"""
Задача 3:

Задача 6:

Задача 7:

Собес:
"""
