"""C1 t10 ★ (AQA, 20 мин). Записыватель вызовов, которому можно верить.

Теория: THEORY.md, раздел 10 («Мок хранит ссылку, а не снимок»).

ЗАЧЕМ ЭТО
Mock из unittest.mock запоминает аргументы каждого вызова, чтобы потом проверить
assert_called_with(...). Но запоминает он ССЫЛКИ на объекты. Если тест после вызова
поменяет объект, «история вызовов» поменяется задним числом, и проверка соврёт:

    payload = {"qty": 1}
    client.post(payload)          # отправили qty=1
    payload["qty"] = 5
    client.post.call_args         # call({'qty': 5})  ← будто отправили 5

Твой записыватель должен хранить СНИМКИ — глубокие копии аргументов на момент вызова.

ТЕРМИНЫ
- **снимок** (snapshot) — независимая глубокая копия: что бы потом ни случилось с
  оригиналом, снимок не меняется;
- **__call__** — специальный метод: если он есть у класса, объект можно «вызывать как
  функцию»: rec(1, 2) — это rec.__call__(1, 2). Именно так устроен Mock (подробно в C9);
- ***args, **kwargs** — все позиционные аргументы приходят кортежем args, все
  именованные — словарём kwargs. rec(payload, retry=True) → args == (payload,),
  kwargs == {"retry": True} (подробно в C4);
- **@property** — метод, который читается как атрибут: rec.calls без скобок (подробно в C7).
  Здесь он уже написан в заготовке, тебе нужно только тело.

ЧТО НУЖНО
rec = CallRecorder()
payload = {"qty": 1}
rec(payload, retry=True)
payload["qty"] = 5

rec.calls  -> [(({"qty": 1},), {"retry": True})]   # список пар (args, kwargs), qty=1!
rec.last   -> (({"qty": 1},), {"retry": True})     # последний вызов
rec.count  -> 1                                     # сколько было вызовов

- у пустого записывателя: calls == [], last is None, count == 0;
- историю нельзя испортить СНАРУЖИ: если тест возьмёт rec.calls и поменяет этот список
  или объекты внутри, следующий rec.calls вернёт исходную историю. Значит, наружу тоже
  отдаём копию, а не свой внутренний список (подумай, почему — раздел 2).

Где хранить историю: в атрибуте объекта, который создаётся в __init__
(например, self._calls = []). Метод __init__ добавь сам.

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
