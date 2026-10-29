"""C2 t06 (основная, 20 мин). Декодировать тело HTTP-ответа и не упасть.

Теория: THEORY.md в этой папке (раздел 6: encode/decode, errors="replace").

ЗАЧЕМ ЭТО
Свой HTTP-клиент, логирование ответов в Allure, чтение вебхуков — везде на входе bytes, а для
отчёта нужен текст. Сервер может прислать другую кодировку, опечатку в ней или битые байты —
логирование при этом не должно ронять тест.

УСЛОВИЕ
decode_body(data, content_type=None) -> str
- data — тело ответа (bytes). content_type — значение заголовка Content-Type или None.
- Кодировку взять из параметра charset заголовка: "text/plain; charset=windows-1251".
  - имя параметра без учёта регистра (charset, Charset, CHARSET);
  - значение может быть в кавычках: charset="utf-8";
  - вокруг ";" и "=" могут быть пробелы.
- Нет заголовка или нет charset — UTF-8.
- Неизвестная кодировка (Python её не знает) — UTF-8.
- Битые байты не роняют функцию: на их месте символ замены \\ufffd (�).

ПРИМЕРЫ
    decode_body(b'{"a": 1}')                                         → '{"a": 1}'
    decode_body("привет".encode("cp1251"), "text/plain; charset=windows-1251")  → "привет"
    decode_body(b"ok", 'text/html; Charset="UTF-8"')                 → "ok"
    decode_body(b"ok", "text/plain; charset=no-such-codec")          → "ok"   # fallback UTF-8
    decode_body(b"a\\xffb")                                           → "a\\ufffdb"

ТЕРМИНЫ
- bytes.decode(encoding, errors="replace") — декодировать с заменой битых байтов.
- Неизвестное имя кодировки: bytes.decode бросает LookupError. Проверить заранее можно
  codecs.lookup(name) — он тоже бросает LookupError.

ПОСЛЕ РЕШЕНИЯ ответь в чат: чем errors="replace" лучше errors="ignore" для логов тестов?
"""


def decode_body(data: bytes, content_type: str | None = None) -> str:
    raise NotImplementedError
