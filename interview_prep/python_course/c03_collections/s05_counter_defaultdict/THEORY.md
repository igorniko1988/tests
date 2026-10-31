# C3 · Раздел 5. Counter и defaultdict

[← раздел 4](../s04_set/THEORY.md) · [оглавление урока](../README.md) · [раздел 6 →](../s06_deque/THEORY.md)

**Простыми словами.** Модуль `collections` — готовые «улучшенные словари». Два самых нужных:

- **`Counter`** — словарь-счётчик: «элемент → сколько раз встретился». Считает частоты одной
  строкой.
- **`defaultdict`** — словарь, который **сам создаёт** значение для нового ключа. Группировка
  без проверок «а есть ли уже такой ключ».

Оба — подклассы `dict`: работают `[]`, `in`, `items()`, `len`, сравнение. На лайвкодинге они
экономят половину кода, и интервьюер ждёт, что ты их знаешь.

---

### 1. Counter: подсчёт

```python
from collections import Counter

c = Counter("banana")
print(c)                     # Counter({'a': 3, 'n': 2, 'b': 1})
print(c["a"])                # 3
print(c["z"])                # 0 — нет KeyError, и ключ НЕ добавляется
print(c.most_common(2))      # [('a', 3), ('n', 2)] — топ-2, список пар
print(c.total())             # 6 — сумма всех счётчиков (3.10+)

statuses = Counter(o["status"] for o in orders)   # частоты из ответа API
```

Что происходит внутри — то же, что ручной подсчёт:

```python
counts = {}
for ch in "banana":
    counts[ch] = counts.get(ch, 0) + 1
# {'b': 1, 'a': 3, 'n': 2}
```

```
"banana":  b → {b:1}
           a → {b:1, a:1}
           n → {b:1, a:1, n:1}
           a → {b:1, a:2, n:1}
           n → {b:1, a:2, n:2}
           a → {b:1, a:3, n:2}    most_common сортирует по счётчику: a(3), n(2), b(1)
```

### 2. most_common и ничьи

При равных счётчиках `most_common` оставляет порядок **первого появления** (сортировка
стабильна, раздел 7):

```python
Counter("abba").most_common()     # [('a', 2), ('b', 2)] — a встретилась раньше
Counter("baab").most_common()     # [('b', 2), ('a', 2)]
```

Если задача требует «при равенстве — по алфавиту», `most_common` этого **не делает**. Сортируй
сам: `sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))`. Это задача t04.

### 3. Арифметика и обновление

```python
a = Counter(x=3, y=1)
b = Counter(x=1, y=2)
a + b          # Counter({'x': 4, 'y': 3})
a - b          # Counter({'x': 2}) — нули и отрицательные выкидываются
a.update("xx") # прибавить на месте: x станет 5
a.subtract(b)  # вычесть на месте, отрицательные остаются
```

### 4. Сравнение «без учёта порядка, но с дублями»

Главное применение Counter в тестах:

```python
actual = ["BTC", "ETH", "BTC"]
expected = ["ETH", "BTC", "BTC"]

assert actual == expected                    # ✗ порядок разный
assert set(actual) == set(expected)          # ✓, но не заметит лишний или потерянный дубль
assert Counter(actual) == Counter(expected)  # ✓ порядок не важен, количество — важно
```

`Counter` работает за O(n), `sorted(a) == sorted(b)` — за O(n log n) и требует, чтобы элементы
можно было сравнивать (`<`). Если элементы — словари (нехешируемые), Counter не подойдёт,
остаётся sorted по ключу.

### 5. defaultdict: значение по умолчанию для нового ключа

`defaultdict(фабрика)` — при обращении `d[k]` к **отсутствующему** ключу вызывает
`фабрика()`, кладёт результат под ключ и возвращает его:

```python
from collections import defaultdict

groups = defaultdict(list)          # фабрика — list, list() даёт []
for o in orders:
    groups[o["status"]].append(o["id"])
# defaultdict(<class 'list'>, {'NEW': [1, 3], 'FILLED': [2]})
```

То же без defaultdict — три варианта, один длиннее другого:

```python
groups = {}
for o in orders:
    if o["status"] not in groups:
        groups[o["status"]] = []
    groups[o["status"]].append(o["id"])

groups.setdefault(o["status"], []).append(o["id"])   # короче, но [] создаётся каждый раз
```

Частые фабрики:

| Фабрика | Новое значение | Для чего |
|---|---|---|
| `list` | `[]` | группировка |
| `int` | `0` | подсчёт: `d[k] += 1` |
| `set` | `set()` | группировка без дублей |
| `lambda: "n/a"` | `"n/a"` | любое своё значение |

Фабрику передают **без скобок**: `defaultdict(list)`. `defaultdict([])` — TypeError: нужен
вызываемый объект, а не готовый список. Это и защищает от C1-ловушки «один список на всех»:
фабрика вызывается **заново** для каждого нового ключа.

### 6. Ловушка: чтение тоже создаёт ключ

```python
d = defaultdict(list)
if d["missing"]:      # прочитали → создался ключ 'missing' со значением []
    ...
print(dict(d))        # {'missing': []}  — «мусорный» ключ
```

Проверять наличие — через `in` или `get`: они ключ **не** создают.

```
d[k]         нет ключа → вызвать фабрику, ПОЛОЖИТЬ, вернуть
d.get(k)     нет ключа → None, ничего не кладёт
k in d       нет ключа → False, ничего не кладёт
```

### 7. Отдавать наружу — обычный dict

`defaultdict` печатается как `defaultdict(<class 'list'>, {...})`, а у потребителя продолжит
создавать ключи при опечатке. Из функции возвращают `dict(groups)`:

```python
def group_by_status(orders):
    groups = defaultdict(list)
    for o in orders:
        groups[o["status"]].append(o["id"])
    return dict(groups)
```

Сравнение `defaultdict == dict` с тем же содержимым — `True`, поэтому тест это не поймает, а вот
`type(result) is dict` и печать в логе — поймают.

---

**Частая ошибка.** `Counter(words).most_common(k)` как ответ на «топ-k, при равенстве — по
алфавиту». На ничьих порядок будет «кто раньше встретился», и тест на ничью упадёт. Читай условие
про ничьи и сортируй явно.

<details><summary>Проверь себя: что выведет?</summary>

```python
from collections import Counter, defaultdict
d = defaultdict(int)
d["a"] += 1
print(d["b"], len(d), Counter("aab")["c"], len(Counter("aab")))
```
`0 2 0 2`. `d["b"]` при чтении создал ключ `b` со значением `int()` = 0, поэтому ключей стало два.
Counter при чтении отсутствующего ключа отдаёт 0 и **не** добавляет ключ — в нём по-прежнему `a` и `b`.
</details>

---

### Практика к разделу

Все команды — из папки `interview_prep/python_course/c03_collections`.

- **Упражнения:** `drills.py` в этой папке. Проверка: `uv run python s05_counter_defaultdict/drills.py`
- **Задача t04 `top_words`** (`interview_prep/python_course/todo/c3/t04_top_words.py`) — топ-k слов текста без учёта регистра, ничьи по алфавиту.
  Проверка: `uv run pytest -k t04`
- **Задача t05 `group_orders`** (`interview_prep/python_course/todo/c3/t05_group_orders.py`) — сгруппировать id ордеров по статусу.
  Проверка: `uv run pytest -k t05`
- **Quiz урока:** №11, №12.
