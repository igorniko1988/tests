"""C1 t04 (основная, 10 мин). Тело запроса из шаблона.

Теория: interview_prep/python_course/c01_objects/s06_copy/THEORY.md (раздел 6, копии) и interview_prep/python_course/c01_objects/s10_autotests/THEORY.md (раздел 10).

ЗАЧЕМ ЭТО
В API-тестах тело запроса обычно не пишут каждый раз с нуля: есть шаблон «нормального»
ордера, а тест меняет одно-два поля (side="sell", qty="0"). Шаблон общий для многих тестов.
Если тест случайно изменит шаблон, сломаются все следующие тесты — и только в общем прогоне.

ТЕРМИНЫ
- **template** (шаблон) — словарь-образец, его трогать нельзя;
- **changes** — изменения, переданные как именованные аргументы: build_payload(t, side="sell")
  внутри функции даёт changes == {"side": "sell"} (так работает **kwargs, подробно в C4);
- «ключи верхнего уровня» — заменяем целиком значение ключа первого уровня
  (side, symbol, meta), а не что-то внутри meta.

ПОЧЕМУ НЕ ХВАТИТ template.copy()
.copy() — поверхностная копия: внешний словарь новый, а вложенный meta и список tags —
ОБЩИЕ с шаблоном. Тест сделает p["meta"]["tags"].append("x") — и шаблон изменится.

    p        ──▶ {symbol, side, meta: ● }
                                      └──▶ {"tags": ● } ──▶ ["smoke"]   ← общие с ORDER!
    ORDER    ──▶ {symbol, side, meta: ● } ─┘

ЧТО НУЖНО
Верни НОВЫЙ dict: шаблон + изменения. Ни сейчас, ни после любых изменений результата
шаблон не должен меняться.

ORDER = {"symbol": "BTC/USDT", "side": "buy", "meta": {"tags": ["smoke"]}}

p = build_payload(ORDER, side="sell")
p   -> {"symbol": "BTC/USDT", "side": "sell", "meta": {"tags": ["smoke"]}}
p["meta"]["tags"].append("x")
ORDER["meta"]["tags"] -> ["smoke"]          # шаблон цел

И ещё одна тонкость: значение из changes тоже не должно «делиться» с вызывающим кодом:
tags = ["a"]; p = build_payload({}, tags=tags); p["tags"].append("b")  ->  tags всё ещё ["a"].

Проверка (из папки priority_c1_c2):  uv run pytest -k c1_t04
"""


def build_payload(template: dict, **changes) -> dict:
    raise NotImplementedError
