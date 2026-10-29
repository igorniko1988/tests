"""C3 t06 (основная, 10 мин). Хранить только последние N событий.

Теория: THEORY.md в этой папке (раздел 6: deque(maxlen=N)).

ЗАЧЕМ ЭТО
Тест-раннер или клиент API держит последние N запросов, чтобы приложить их к отчёту при
падении. Поток событий может быть бесконечным — хранить всё нельзя.

УСЛОВИЕ
class RecentEvents:
- RecentEvents(n) — хранить не больше n последних событий. n < 1 — ValueError.
- add(event) — добавить событие.
- items() -> list — сохранённые события, от старых к новым (новый список: изменения
  в нём не должны портить хранилище).
- total — свойство (@property): сколько событий добавлено ЗА ВСЁ ВРЕМЯ, включая выпавшие.
- len(r) — сколько событий хранится сейчас.
- Память — O(n): тест прогонит 200 000 событий при n = 3.

ПРИМЕР
    r = RecentEvents(3)
    for e in ["e1", "e2", "e3", "e4"]:
        r.add(e)
    r.items()  → ["e2", "e3", "e4"]    # e1 выпал
    len(r)     → 3
    r.total    → 4

ТЕРМИНЫ
- @property — метод, который читается как поле: r.total без скобок (подробно в C9).

ПОСЛЕ РЕШЕНИЯ ответь в чат: почему не list с pop(0), когда он переполнен?
"""


class RecentEvents:
    def __init__(self, n: int) -> None:
        raise NotImplementedError

    def add(self, event) -> None:
        raise NotImplementedError

    def items(self) -> list:
        raise NotImplementedError

    @property
    def total(self) -> int:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
