"""X0 t02 (практика AQA, 25 минут). Отчёт по ошибкам из лога.

На вход — список строк лога вида:
    "2026-10-28T10:00:00 ERROR orders Timeout to price-feed"
    дата-время, уровень, сервис, сообщение (сообщение может содержать пробелы).

Верни список пар (service, count) по строкам с уровнем ERROR:
- отсортирован по count по убыванию;
- при равном count — по имени сервиса по алфавиту;
- не больше top пар (top по умолчанию 3).

Пустые строки и строки, где меньше четырёх частей, пропускай.

error_report([
    "2026-10-28T10:00:00 ERROR orders Timeout to price-feed",
    "2026-10-28T10:00:01 INFO orders Created 42",
    "2026-10-28T10:00:02 ERROR auth Bad token",
    "2026-10-28T10:00:03 ERROR orders Insufficient funds",
    "",
]) -> [("orders", 2), ("auth", 1)]

Проверка (из папки interview_prep/python_course/todo):  uv run pytest tests/test_x0.py -k t02
"""


def error_report(lines: list[str], top: int = 3) -> list[tuple[str, int]]:
    raise NotImplementedError
