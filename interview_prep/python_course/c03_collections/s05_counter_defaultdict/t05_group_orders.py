"""C3 t05 (разминка, 10 мин). Сгруппировать ордера по статусу.

Теория: THEORY.md в этой папке (раздел 5: defaultdict, наружу — обычный dict).

ЗАЧЕМ ЭТО
«Сколько ордеров в каждом статусе», «какие тесты упали по каждой причине» — группировка
нужна постоянно: в отчётах, в проверках ответа, на лайвкодинге.

УСЛОВИЕ
group_orders(orders) -> dict[str, list[int]]
- orders — список словарей с ключами "id" и "status".
- Вернуть словарь «статус → список id» в порядке появления ордеров.
- Порядок статусов — по первому появлению.
- Вернуть ОБЫЧНЫЙ dict (тест проверит type(result) is dict).
- Исходный список не менять.

ПРИМЕР
    orders = [
        {"id": 1, "status": "NEW"},
        {"id": 2, "status": "FILLED"},
        {"id": 3, "status": "NEW"},
    ]
    group_orders(orders) → {"NEW": [1, 3], "FILLED": [2]}
    group_orders([])     → {}

ПОСЛЕ РЕШЕНИЯ ответь в чат: почему не defaultdict([])? И зачем отдавать dict(...),
если defaultdict == dict с тем же содержимым?
"""


def group_orders(orders: list[dict]) -> dict[str, list[int]]:
    raise NotImplementedError
