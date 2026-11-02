# C3 · Раздел 8. Коллекции в автотестах

[← раздел 7](../s07_sorting/THEORY.md) · [оглавление урока](../README.md) · [раздел 9 →](../s09_cheatsheet/THEORY.md)

**Простыми словами.** Почти каждый API-тест — это работа с коллекциями: ответ — список словарей,
надо найти нужный элемент, сравнить с ожиданием, проверить порядок, уникальность, состав полей.
Выбор коллекции решает, будет ли проверка **точной** (не пропустит баг), **понятной** (по
сообщению видно, что сломалось) и **быстрой**. Ниже — типовые проверки на примере стенда
«мини-биржа».

---

### 1. Сравнить списки без учёта порядка

API не обещает порядок — `GET /orders` вернул те же ордера в другом порядке. Три способа:

```python
actual = [o["id"] for o in resp.json()]

assert set(actual) == {1, 2, 3}           # ✗ не заметит дубль [1, 1, 2, 3]
assert sorted(actual) == [1, 2, 3]        # ✓ дубли видны, O(n log n), элементы должны сравниваться
assert Counter(actual) == Counter([1, 2, 3])   # ✓ дубли видны, O(n), элементы хешируемые
```

Список словарей (нехешируемых) — сортируй по ключу: `sorted(items, key=itemgetter("id"))`.

### 2. Проверить, что элементы на месте, и показать разницу

```python
expected = {1, 2, 3}
actual = {o["id"] for o in resp.json()}
missing, extra = expected - actual, actual - expected
assert not missing and not extra, f"missing={sorted(missing)} extra={sorted(extra)}"
```

Сообщение `missing=[3] extra=[]` сразу говорит, что сломалось. Голый `assert a == b` на больших
множествах pytest покажет хуже.

### 3. Частичное совпадение словаря

Ответ содержит `id`, `created_at` и прочее, что заранее неизвестно. Проверяем только то, что знаем:

```python
expected = {"symbol": "BTC-USD", "side": "BUY", "status": "NEW"}
order = resp.json()

assert expected.items() <= order.items()                 # все пары expected есть в ответе
assert {k: order[k] for k in expected} == expected       # то же, но pytest покажет разницу полей
assert {"id", "created_at"} <= order.keys()              # обязательные поля есть
```

Второй вариант лучше для отчёта: при падении pytest покажет, какое поле отличается.

### 4. Найти элемент по id — индекс

```python
orders_by_id = {o["id"]: o for o in resp.json()}         # один проход, O(n)
assert orders_by_id[created_id]["status"] == "NEW"       # KeyError = ордера нет в ответе
```

Вместо `next(o for o in orders if o["id"] == created_id)` в каждом тесте — особенно если искать
нужно много раз.

### 5. Уникальность

```python
ids = [o["id"] for o in orders]
assert len(ids) == len(set(ids))                         # есть ли дубли
dups = [x for x, n in Counter(ids).items() if n > 1]     # какие именно
assert not dups, f"повторяются id: {dups}"
```

### 6. Порядок сортировки из API

```python
prices = [Decimal(o["price"]) for o in resp.json()]   # строки → Decimal (раздел 7)
assert prices == sorted(prices, reverse=True), "стакан bids должен идти по убыванию цены"
```

Проверка «отсортировано» через `sorted` — O(n log n). Через соседей — O(n):
`all(a >= b for a, b in zip(prices, prices[1:]))`.

### 7. Пагинация: собрать всё и проверить стыки

```python
seen = []
page = 1
while True:
    items = client.get_orders(page=page, size=50)
    if not items:
        break
    seen.extend(o["id"] for o in items)
    page += 1
assert len(seen) == len(set(seen)), "элементы повторяются на стыке страниц"
```

Дубли и пропуски на границах страниц — классический баг пагинации, и находит его как раз сравнение
длины списка и множества.

### 8. Параметризация — кортежи

```python
@pytest.mark.parametrize(("side", "status"), [("BUY", 201), ("SELL", 201), ("HOLD", 422)])
def test_create_order(side, status): ...
```

Каждый набор — кортеж, распаковка по именам параметров (раздел 2). Один параметр:
`parametrize("side", ["BUY", "SELL"])` — список значений, не кортежи.

---

**Частая ошибка.** Сравнить ответ целиком с заранее записанным словарём
(`assert resp.json() == EXPECTED`), а там `id` и `created_at` меняются от запуска к запуску. Тест
либо всегда красный, либо его «чинят», удаляя проверку. Проверяй известные поля частичным
сравнением, а изменчивые — по типу и формату.

<details><summary>Проверь себя: что выведет?</summary>

```python
order = {"id": 7, "side": "BUY", "status": "NEW"}
print({"side": "BUY"}.items() <= order.items(), {"side": "SELL"}.items() <= order.items())
```
`True False`. `items()` ведёт себя как множество пар: `("side", "BUY")` в ордере есть,
`("side", "SELL")` — нет.
</details>

---

### Практика к разделу

- Задач нет — приёмы отсюда используются в задачах урока и в Q1.
- **Упражнения:** `drills.py` в этой папке. Проверка: `uv run python s08_autotests/drills.py`
