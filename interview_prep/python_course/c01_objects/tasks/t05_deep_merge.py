"""C1 t05 (основная, 15 мин). Глубокое слияние настроек.

Верни НОВЫЙ dict: base, поверх которого наложен override.
- если ключ есть в обоих и оба значения dict — сливаем их рекурсивно;
- иначе значение из override заменяет значение из base;
- base и override не меняются;
- результат не делит изменяемых объектов с base и override
  (поменял список в результате — во входных данных ничего не изменилось).

base     = {"api": {"url": "http://x", "timeout": 5}, "tags": ["a"]}
override = {"api": {"timeout": 10}, "debug": True}
deep_merge(base, override)
  -> {"api": {"url": "http://x", "timeout": 10}, "tags": ["a"], "debug": True}

Проверка:  uv run pytest -k t05
"""


def deep_merge(base: dict, override: dict) -> dict:
    raise NotImplementedError
