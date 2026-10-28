"""Урок 2. Ловушка со списком по умолчанию в аргументе.

    python lessons/lesson_02_default_args.py
"""

def add_tag(tag, tags=[]):       # [] создаётся ОДИН раз, когда Python читает def
    tags.append(tag)
    return tags

print(add_tag("a"))              # ['a']
print(add_tag("b"))              # ['a', 'b']  неожиданно!
print(add_tag.__defaults__)      # (['a', 'b'],) вот он, спрятанный общий список


def add_tag_ok(tag, tags=None):  # правильно: None + создаём внутри
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag_ok("a"))           # ['a']
print(add_tag_ok("b"))           # ['b']

# Безопасные значения по умолчанию: числа, строки, None, True/False, кортежи.
# Опасные: [], {}, set().
