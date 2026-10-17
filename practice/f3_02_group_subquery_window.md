# F3. Урок 2 — GROUP BY, HAVING, подзапросы, оконные функции

Задания: `practice/f3_02_group_subquery_window.sql`.

## 1. Агрегатные функции

```sql
SELECT count(*) FROM orders;                 -- сколько строк
SELECT count(country) FROM users;            -- сколько НЕ NULL значений
SELECT sum(quantity), avg(price), min(price), max(price) FROM orders WHERE symbol = 'ETH-USDT';
```

## 2. GROUP BY — посчитать по группам

```sql
SELECT status, count(*) AS cnt
FROM orders
GROUP BY status;
```

```text
status            | cnt
NEW               | 4
FILLED            | 4
...
```

Правило: в `SELECT` — **только** колонки из `GROUP BY` и агрегаты. `SELECT status, price ... GROUP BY status`
— ошибка: какую из цен группы показать?

```sql
SELECT user_id, symbol, sum(price * quantity) AS volume   -- группа по двум колонкам
FROM orders
GROUP BY user_id, symbol;
```

## 3. HAVING — фильтр по группам

`WHERE` фильтрует **строки до** группировки, `HAVING` — **группы после**.

```sql
SELECT user_id, count(*) AS cnt
FROM orders
WHERE status <> 'CANCELED'        -- сначала выкинуть отменённые строки
GROUP BY user_id
HAVING count(*) >= 2;             -- потом оставить пользователей, у кого 2+ ордера
```

## 4. Подзапросы

Запрос внутри запроса.

```sql
-- в WHERE: ордера дороже средней цены
SELECT * FROM orders
WHERE price > (SELECT avg(price) FROM orders WHERE symbol = 'ETH-USDT')
  AND symbol = 'ETH-USDT';

-- IN: пользователи, у которых есть FILLED
SELECT email FROM users
WHERE id IN (SELECT user_id FROM orders WHERE status = 'FILLED');

-- NOT EXISTS: пользователи без ордеров (второй способ из урока 1)
SELECT email FROM users u
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

Ловушка: `NOT IN (подзапрос)`, если в подзапросе есть NULL, не вернёт **ничего**. `NOT EXISTS` безопаснее.

### CTE — `WITH` (читаемый подзапрос)

```sql
WITH active AS (
    SELECT * FROM orders WHERE status IN ('NEW', 'PARTIALLY_FILLED')
)
SELECT user_id, count(*) FROM active GROUP BY user_id;
```

## 5. CASE — условие в колонке

```sql
SELECT id,
       CASE WHEN side = 'BUY' THEN price * quantity ELSE 0 END AS buy_volume
FROM orders;

SELECT count(*) FILTER (WHERE status = 'FILLED') AS filled_cnt FROM orders;  -- Postgres-сокращение
```

## 6. Оконные функции (обзор)

Агрегат **без схлопывания строк**: каждая строка остаётся, а рядом — значение по её «окну».

```sql
SELECT id, user_id, price,
       row_number() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn,   -- номер внутри пользователя
       sum(quantity) OVER (PARTITION BY user_id) AS user_total_qty                -- сумма по пользователю
FROM orders;
```

- `PARTITION BY` — на какие группы делить (как GROUP BY, но строки не схлопываются);
- `ORDER BY` внутри `OVER` — порядок в окне.

Самое частое применение — **«последний ордер каждого пользователя»** / «топ-N в каждой группе»:

```sql
SELECT * FROM (
    SELECT o.*, row_number() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
    FROM orders o
) t
WHERE rn = 1;
```

Ещё полезно знать: `rank()` / `dense_rank()` (одинаковые значения — одинаковый номер),
`lag()` / `lead()` (значение из предыдущей / следующей строки).

## Шпаргалка

| Что | Как |
|---|---|
| посчитать по группам | `GROUP BY col` + `count(*)` |
| фильтр групп | `HAVING count(*) > 1` |
| дубли | `GROUP BY поля HAVING count(*) > 1` |
| есть / нет связанных | `EXISTS` / `NOT EXISTS` |
| читаемый подзапрос | `WITH name AS (...)` |
| условие в колонке | `CASE WHEN ... THEN ... END` |
| последний в группе | `row_number() OVER (PARTITION BY ... ORDER BY ... DESC) = 1` |

## Вопросы собеседования

1. Чем `WHERE` отличается от `HAVING`?
2. Почему нельзя `SELECT status, price ... GROUP BY status`?
3. Как найти дубли в таблице?
4. `NOT IN` vs `NOT EXISTS` — в чём ловушка с NULL?
5. Чем оконная функция отличается от `GROUP BY`?
6. Как получить последний ордер каждого пользователя?
7. `count(*)` vs `count(col)`?
