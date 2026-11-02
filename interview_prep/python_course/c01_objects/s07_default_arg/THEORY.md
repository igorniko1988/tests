# C1 · Раздел 7. Изменяемый аргумент по умолчанию

[← раздел 6](../s06_copy/THEORY.md) · [оглавление урока](../README.md) · [раздел 8 →](../s08_passing/THEORY.md)

**Простыми словами.** `def` — это не «объявление», а обычная команда, которая выполняется,
когда Python до неё доходит. Выполняясь, она создаёт объект-функцию и **в этот момент один
раз** вычисляет значения по умолчанию. Эти значения сохраняются в функции (`f.__defaults__`)
и используются во всех вызовах, где аргумент не передали.

Доказательство, что значение по умолчанию считается при `def`, а не при вызове:

```python
def f(x=print("считаю значение по умолчанию")):
    pass
# сообщение напечаталось СРАЗУ, ещё до вызова f

f(); f()                   # больше ничего не печатается
```

Если значение по умолчанию изменяемое, все вызовы делят **один** объект:

```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

r1 = add(1)                # bucket — список из __defaults__, он стал [1]
r2 = add(2)                # ТОТ ЖЕ список, он стал [1, 2]
print(r1, r2, r1 is r2)    # [1, 2] [1, 2] True
print(add.__defaults__)    # ([1, 2],)
```

**Правильный шаблон — `None` по умолчанию и создание объекта внутри:**

```python
def add(item, bucket=None):
    if bucket is None:     # не передали — создаём новый список на КАЖДЫЙ вызов
        bucket = []
    bucket.append(item)
    return bucket
```

Почему именно `None`: он неизменяем, и его нельзя «испортить». Если `None` — допустимое
значение аргумента, используют свой маркер: `_MISSING = object()` и `if x is _MISSING:`.

**Не только списки.** Та же проблема с `{}` и `set()`, а ещё со значениями, которые должны
быть «свежими» на каждый вызов:

```python
from datetime import datetime

def make_order(created_at=datetime.now()):   # время «замёрзло» в момент def!
    return {"created_at": created_at}

# все заказы получат одно и то же время — время загрузки модуля
```

**В dataclass** Python сам защищает от этой ошибки: `roles: list = []` выдаёт
`ValueError: mutable default <class 'list'> for field roles is not allowed`.
Правильно: `roles: list = field(default_factory=list)` — фабрика вызывается на каждый объект.

<details><summary>Проверь себя: что выведет?</summary>

```python
def f(n, seen=set()):
    seen.add(n)
    return len(seen)

f(1); f(2)
print(f(1))
```
`2`. Множество общее: после трёх вызовов в нём `{1, 2}` (повторная `1` не добавляет элемент).
</details>

**В визуализаторе:** вкладка «Аргумент по умолчанию» — https://claude.ai/artifact/TzYJP1PWSAMPkEiyaZNHLh

---

### Практика к разделу

Все команды — из папки `c01_objects`.

- **Упражнения:** `drills.py` в этой папке — впиши ответы под фрагментами, проверка: `uv run python s07_default_arg/drills.py`
- **Задача:** `t01_fix_default.py` в этой папке — проверка: `uv run pytest -k t01`
- **Quiz урока:** №8 в `quiz.py` — проверка: `uv run python quiz.py 8`
