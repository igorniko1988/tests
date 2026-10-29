# A0 · Раздел 4. Скрытая сложность

[← раздел 3](../s03_python_ops/THEORY.md) · [оглавление урока](../README.md) · [раздел 5 →](../s05_memory/THEORY.md)

**Простыми словами.** Самая частая причина медленного решения на собесе — не явный вложенный
цикл, а **одна безобидная строка внутри цикла**, которая сама по себе O(n). Цикл на n шагов ×
операция за O(n) = O(n²). Интервьюер видит это сразу и спрашивает: «А какая здесь сложность?»

Правило оценки: **сложность цикла = число повторов × цена тела**. Цену тела считай по таблице
из раздела 3, а не по количеству строк.

---

### 1. `in` по списку внутри цикла

```python
def unique(items):
    result = []
    for x in items:              # n раз
        if x not in result:      #   × O(n): перебор списка result
            result.append(x)
    return result
# O(n²)
```

**Фикс:** держать рядом **множество** для проверки — оно отвечает за O(1).

```python
def unique(items):
    seen = set()
    result = []
    for x in items:              # n раз
        if x not in seen:        #   × O(1)
            seen.add(x)
            result.append(x)     # порядок сохраняем через список
    return result
# O(n)
```

### 2. `count` / `index` / `max` внутри цикла

```python
def first_unique(s):
    for i, ch in enumerate(s):   # n раз
        if s.count(ch) == 1:     #   × O(n): count проходит ВСЮ строку
            return i
    return -1
# O(n²)
```

**Фикс:** посчитать всё **один раз заранее** (`Counter`), потом спрашивать за O(1).

```python
from collections import Counter

def first_unique(s):
    counts = Counter(s)          # O(n) — один проход
    for i, ch in enumerate(s):   # O(n)
        if counts[ch] == 1:      #   × O(1)
            return i
    return -1
# O(n) + O(n) = O(n)
```

То же с `max(lst)` или `sorted(lst)` внутри цикла: если результат не меняется между
итерациями — вычисли его **до** цикла.

### 3. `pop(0)` и `insert(0, x)` у списка

```python
def process(queue):
    while queue:                 # n раз
        task = queue.pop(0)      #   × O(n): сдвиг всех оставшихся
        handle(task)
# O(n²)
```

**Фикс:** `collections.deque` и `popleft()` — O(1). Или идти по списку индексом, ничего не удаляя.

### 4. Сборка списка или строки через `+`

```python
result = []
for x in items:
    result = result + [x]        # каждый раз НОВЫЙ список с копией всего старого
# 1 + 2 + 3 + … + n ≈ n²/2 копирований → O(n²)

text = ""
for word in words:
    text += word + " "           # строка неизменяема — тоже копия на каждом шаге
```

**Фикс:** `result.append(x)` (меняет тот же список, C1 раздел 4) и `" ".join(words)`.

### 5. Срезы в рекурсии и в цикле

```python
def total(nums):
    if not nums:
        return 0
    return nums[0] + total(nums[1:])   # nums[1:] копирует n−1, n−2, … элементов
# O(n²) по времени, и все срезы живут одновременно в стеке вызовов → O(n²) памяти
```

**Фикс:** передавать **индекс** вместо среза: `total(nums, i + 1)`.

### 6. `remove` в цикле

```python
for bad in banned:               # m раз
    if bad in items:             #   O(n)
        items.remove(bad)        #   O(n): найти + сдвинуть хвост
# O(n · m)
```

**Фикс:** один проход с фильтром: `banned_set = set(banned)`,
`items = [x for x in items if x not in banned_set]` — O(n + m).

---

```
 ЦИКЛ на n шагов
 └── тело: x in list / s.count / lst.pop(0) / lst + [x] / s += / срез / remove / max / sorted
           ↑ каждая из этих операций — O(n)
 = O(n) × O(n) = O(n²)
```

**Частая ошибка.** Называть сложность по числу циклов в коде: «цикл один — значит O(n)». Всегда
спрашивай себя: **сколько стоит каждая строка тела цикла?**

<details><summary>Проверь себя: найди скрытый O(n)</summary>

```python
def report(orders, vip_ids):          # vip_ids — список
    lines = []
    for o in orders:
        if o["user_id"] in vip_ids:   # ← здесь
            lines.append(o["id"])
    return lines
```

`o["user_id"] in vip_ids` — перебор списка: O(n · m). Фикс: `vip = set(vip_ids)` до цикла →
O(n + m).
</details>

---

### Практика к разделу

Все команды — из папки `a00_big_o`.

- **Задача t01 «Оцени сложность»:** `t01_estimate.py` в этой папке — 10 фрагментов кода, для
  каждого впиши сложность по времени и по памяти. Проверка: `uv run python s04_hidden_cost/t01_estimate.py`
  (сверит и объяснит). Про память — раздел 5, его можно прочитать до задачи.
