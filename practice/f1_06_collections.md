# F1. Урок 6 — коллекции и задачи для лайвкодинга

Задачи к уроку: `practice/f1_06_collections.py`.

## Зачем это QA

На лайвкодинге AQA почти всегда дают задачу «обработай ответ API»: список словарей →
отфильтруй, сгруппируй, посчитай, найди дубли, сравни. Всё решается четырьмя коллекциями
и comprehension'ами.

## 1. Четыре коллекции

| Тип | Пример | Изменяемый | Порядок | Дубли | Поиск `in` |
|---|---|---|---|---|---|
| `list` | `[1, 2, 2]` | да | да | да | медленно (перебор) |
| `tuple` | `(1, 2)` | **нет** | да | да | медленно |
| `dict` | `{"a": 1}` | да | да (с 3.7) | ключи — нет | **быстро** по ключу |
| `set` | `{1, 2}` | да | **нет** | **нет** | **быстро** |

- Ключом `dict` и элементом `set` может быть только **неизменяемое** (str, int, tuple), не list.
- `set` — убрать дубли и быстро проверить «есть ли».

## 2. dict — главный тип для JSON

```python
order = {"id": 1, "status": "NEW"}

order["status"]                 # "NEW"; нет ключа → KeyError
order.get("price")              # None — без ошибки
order.get("price", "0")         # "0" — значение по умолчанию

for key, value in order.items():
    print(key, value)
```

### Счётчик и группировка

```python
from collections import Counter, defaultdict

statuses = ["NEW", "FILLED", "NEW"]
Counter(statuses)                       # Counter({'NEW': 2, 'FILLED': 1})
Counter(statuses).most_common(1)        # [('NEW', 2)]

groups = defaultdict(list)              # нет ключа → создаст пустой список
for order in orders:
    groups[order["status"]].append(order["id"])
```

## 3. Comprehension

```python
[o["id"] for o in orders]                               # список id
[o for o in orders if o["status"] == "NEW"]             # фильтр
{o["id"]: o["status"] for o in orders}                  # dict: id → статус
{o["symbol"] for o in orders}                           # set уникальных символов
```

Форма: `[ЧТО for ЭЛЕМЕНТ in КОЛЛЕКЦИЯ if УСЛОВИЕ]`.

## 4. set-операции — сравнение двух выборок

```python
expected = {"ETH-USDT", "BTC-USDT"}
actual = {"ETH-USDT", "SOL-USDT"}

expected - actual      # {'BTC-USDT'} — чего не хватает
actual - expected      # {'SOL-USDT'} — что лишнее
expected & actual      # {'ETH-USDT'} — общее
expected | actual      # всё вместе
```

## 5. Сортировка

```python
sorted(orders, key=lambda o: o["price"])                 # новый список, по цене
sorted(orders, key=lambda o: o["price"], reverse=True)   # по убыванию
sorted(orders, key=lambda o: (o["status"], o["id"]))     # по двум полям
orders.sort(key=...)                                     # меняет сам список, возвращает None
max(orders, key=lambda o: o["price"])                    # самый дорогой
```

`lambda o: o["price"]` — короткая функция «из ордера достань цену».

## 6. JSON

```python
import json

text = '{"id": 1, "tags": ["a"]}'
data = json.loads(text)                 # строка → dict
json.dumps(data, indent=2, ensure_ascii=False)   # dict → красивая строка
```

`response.json()` в requests — это и есть `json.loads(response.text)`.

## 7. Мутабельность — частая ловушка

```python
a = [1, 2]
b = a              # НЕ копия, а второе имя того же списка
b.append(3)
print(a)           # [1, 2, 3]

c = a.copy()       # поверхностная копия
import copy
d = copy.deepcopy(nested)   # глубокая — для вложенных dict/list

def add(item, items=[]):    # ❌ список по умолчанию создаётся ОДИН раз
    items.append(item)
    return items

def add(item, items=None):  # ✅
    items = [] if items is None else items
```

`is` — тот же объект; `==` — равные значения. `None` проверяют через `is None`.

## Шпаргалка

| Задача | Решение |
|---|---|
| убрать дубли | `set(items)` |
| найти дубли | `[x for x, n in Counter(items).items() if n > 1]` |
| посчитать | `Counter(items)` |
| сгруппировать | `defaultdict(list)` |
| индекс по id | `{o["id"]: o for o in orders}` |
| разница выборок | `set_a - set_b` |
| сортировка по полю | `sorted(items, key=lambda x: x["f"])` |
| безопасно достать | `d.get("key", default)` |

## Вопросы собеседования

1. Чем list отличается от tuple? Почему list не может быть ключом dict?
2. Почему `in` для set быстрее, чем для list?
3. Чем `sorted()` отличается от `.sort()`?
4. Что выведет `a = [1]; b = a; b.append(2); print(a)`? Как сделать копию?
5. В чём ловушка `def f(items=[])`?
6. `is` vs `==` — в чём разница?
