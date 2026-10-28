"""C1 t04 (основная, 10 мин). Тело запроса из шаблона.

В API-тестах тело запроса собирают из шаблона и меняют пару полей.
Верни НОВЫЙ dict: шаблон + изменения из changes (ключи верхнего уровня).

Главное требование: шаблон не должен меняться НИКОГДА — ни сейчас, ни когда тест
потом поменяет что-то вложенное в результате.

ORDER = {"symbol": "BTC/USDT", "side": "buy", "meta": {"tags": ["smoke"]}}

p = build_payload(ORDER, side="sell")
p   -> {"symbol": "BTC/USDT", "side": "sell", "meta": {"tags": ["smoke"]}}
p["meta"]["tags"].append("x")
ORDER["meta"]["tags"] -> ["smoke"]          # шаблон цел

Проверка:  uv run pytest -k t04
"""


def build_payload(template: dict, **changes) -> dict:
    raise NotImplementedError
