"""C1 t10 ★ (AQA, 20 мин). Записыватель вызовов, которому можно верить.

Mock хранит в call_args ссылки на аргументы: поменяли объект после вызова — поменялась
«история» (см. THEORY.md, раздел 9). Напиши свой записыватель, который хранит снимки.

rec = CallRecorder()
payload = {"qty": 1}
rec(payload, retry=True)        # объект вызывается как функция (метод __call__)
payload["qty"] = 5
rec.calls  -> [(({"qty": 1},), {"retry": True})]     # снимок, а не ссылка
rec.last   -> (({"qty": 1},), {"retry": True})       # последний вызов
rec.count  -> 1

Требования:
- calls — список пар (args, kwargs), args — tuple, kwargs — dict;
- снаружи нельзя испортить историю: изменение rec.calls или вложенных объектов из
  него не меняет то, что вернёт следующий rec.calls;
- last у пустого записывателя — None.

Проверка:  uv run pytest -k t10
"""


class CallRecorder:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def calls(self) -> list[tuple[tuple, dict]]:
        raise NotImplementedError

    @property
    def last(self):
        raise NotImplementedError

    @property
    def count(self) -> int:
        raise NotImplementedError
