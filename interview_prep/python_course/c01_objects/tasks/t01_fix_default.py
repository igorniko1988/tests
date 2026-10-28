"""C1 t01 (разминка, 5 мин). Почини аргумент по умолчанию.

Хелпер из тестового фреймворка добавляет тег к списку тегов. Сейчас он написан так:

    def add_tag(tag, tags=[]):
        tags.append(tag)
        return tags

и теги «протекают» между вызовами. Перепиши правильно:

add_tag("smoke")                -> ["smoke"]
add_tag("api")                  -> ["api"]          # а не ["smoke", "api"]
mine = ["ui"]; add_tag("x", mine) -> ["ui", "x"], и mine тоже ["ui", "x"] (свой список меняем)

Проверка:  uv run pytest -k t01
"""


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    raise NotImplementedError
