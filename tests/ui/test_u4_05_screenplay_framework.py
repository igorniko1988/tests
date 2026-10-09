"""U4. Урок 5 — Screenplay, собес по модулю U4 и каркас фреймворка.

Теория и банк вопросов: practice/u4_05_screenplay_interview.md
Код: ui_framework/screenplay/{actor,abilities,tasks,questions}.py (заготовки есть).
Запуск:
    uv run pytest tests/ui/test_u4_05_screenplay_framework.py -v

Задача 1. Ядро (actor.py, abilities.py).
    Actor: can(...), ability_to(kind), attempts_to(*tasks), asks_for(question), memory.
    BrowseTheWeb(page): auth и dashboard — твои PO из U4.1–U4.2.

Задача 2. Задачи и вопросы (tasks.py, questions.py).
    Tasks: Register(email=None), Deposit(asset, amount), PlaceOrder(side, price, quantity, symbol),
           CancelOrder(order_id=None — если None, отменить последний из памяти).
    Questions: AvailableBalance(asset), LockedBalance(asset), LastOrderStatus() — возвращают Locator.
    Используй OrderData и unique_email из U4.4.

Задача 3. Сделка двух участников в стиле Screenplay.
    Фикстура actor_factory(name) -> Actor: новый context (new_context), BrowseTheWeb.
    Алиса продаёт ETH, Боб покупает по той же цене (isolated_price из U4.4).
    Проверь статусы и балансы обоих через asks_for + expect (таймаут — из settings).

Задача 4. Тот же сценарий на PO.
    Перепиши задачу 3 только через new_dashboard и PO (без screenplay).
    В «Ответах»: сравни два теста — строки, читаемость, что пришлось написать дополнительно,
    что проще поменять, если подготовку (регистрацию и пополнение) перенести на API.

Задача 5. Чек-лист каркаса.
    Пройди чек-лист из теории (раздел 5) по своему ui_framework/ — отметь в «Ответах» каждый пункт:
    ✅ / ❌ + что сделаешь. Исправь всё, что можно исправить за 30 минут.
    Обязательно: ui_framework/README.md (установка, стенд, запуск, окружения, Allure, структура,
    «как добавить страницу»).

Задача 6. Рассказ про фреймворк.
    Напиши в «Ответах» свой ответ на вопрос 3 банка («Расскажи про свой UI-фреймворк») по плану из теории.
    Потом расскажи его вслух под диктофон за 2–3 минуты, прослушай, сократи лишнее.

Задача 7. Лайвкодинг — 25 минут.
    «Добавь в фреймворк проверку частичного исполнения»:
    продавец SELL ETH-USDT кол-во 2, покупатель BUY кол-во 1 по той же цене.
    У продавца статус PARTIALLY_FILLED, исполнено 1, заблокировано ETH 1; фильтр «Статус» =
    PARTIALLY_FILLED показывает одну строку. Только через фреймворк (PO или screenplay — на выбор).
    Засеки время; что не успел — в «Ответах».

Задача 8. Устный собес по модулю U4.
    10 случайных вопросов из банка (U4.1–U4.5, всего 31), 40–90 с на ответ, вслух, без подглядывания.
    В «Ответах» — номера, на которых «поплыл».
"""

import pytest
from playwright.sync_api import expect

# Задача 3


# Задача 4


# Задача 7


# Ответы
"""
Задача 4:

Задача 5:

Задача 6:

Задача 7:

Задача 8:
"""
