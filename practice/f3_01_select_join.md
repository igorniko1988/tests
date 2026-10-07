# F3. Урок 1 — SELECT, WHERE, ORDER BY, JOIN

Задания: `practice/f3_01_select_join.sql`.

## Подготовка (один раз)

```bash
docker compose up -d db
docker compose exec -T db psql -U exchange -d exchange < practice/f3_00_seed.sql   # учебные данные
docker compose exec db psql -U exchange -d exchange                                # консоль
```

В консоли `psql`:

```sql
SET search_path TO sql_practice;   -- работать с учебной схемой (иначе пиши sql_practice.users)
\dt                                -- список таблиц
\d orders                          -- колонки таблицы
\q                                 -- выйти
```

Можно и через GUI: DBeaver / DataGrip / PyCharm Database → host `localhost`, port `5432`,
user/password/db `exchange`.

## Учебные таблицы

```text
users     (id, email, country, created_at)
balances  (id, user_id → users.id, asset, available, locked)
orders    (id, user_id → users.id, symbol, side, price, quantity, filled_quantity, status, created_at)
```

## 1. SELECT и WHERE

```sql
SELECT * FROM users;                                  -- все колонки
SELECT id, email FROM users;                          -- нужные колонки
SELECT * FROM orders WHERE status = 'NEW';            -- строки — в одинарных кавычках
SELECT * FROM orders WHERE price > 2000 AND side = 'BUY';
SELECT * FROM orders WHERE status IN ('NEW', 'PARTIALLY_FILLED');
SELECT * FROM orders WHERE price BETWEEN 1900 AND 2100;   -- включительно
SELECT * FROM users WHERE email LIKE '%@test.io';     -- % — любые символы
SELECT * FROM users WHERE email ILIKE 'anna%';        -- без учёта регистра (Postgres)
SELECT * FROM users WHERE country IS NULL;            -- НЕ "= NULL"
```

**NULL** — «неизвестно». `country = NULL` всегда даёт «неизвестно», а не true, поэтому строк не найдёт.
Только `IS NULL` / `IS NOT NULL`.

## 2. ORDER BY, LIMIT, DISTINCT, AS

```sql
SELECT * FROM orders ORDER BY created_at DESC LIMIT 3;        -- 3 последних
SELECT * FROM orders ORDER BY status, price DESC;             -- по двум колонкам
SELECT DISTINCT symbol FROM orders;                           -- уникальные значения
SELECT id, price * quantity AS total FROM orders;             -- вычисляемая колонка с именем
```

## 3. JOIN — соединить таблицы

```sql
SELECT u.email, o.symbol, o.status
FROM orders o
JOIN users u ON u.id = o.user_id;          -- для каждого ордера подтянуть его пользователя
```

`o` и `u` — короткие псевдонимы таблиц. `ON` — по какому условию склеивать строки.

### INNER JOIN vs LEFT JOIN

```text
users:  1 anna, 3 carl (без ордеров)
orders: ордер anna

INNER JOIN — только пары, где совпало:   anna + ордер
LEFT JOIN  — ВСЕ строки левой таблицы:   anna + ордер, carl + NULL
```

```sql
SELECT u.email, o.id
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;     -- пользователи без ордеров тоже будут, o.id = NULL
```

`JOIN` = `INNER JOIN`. Есть ещё `RIGHT JOIN` (наоборот) и `FULL JOIN` (все с обеих сторон) — редко.

### Классика: «найди тех, у кого нет ...»

```sql
SELECT u.email
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;                         -- у кого не нашлось ни одного ордера
```

## 4. Порядок выполнения запроса

Пишем в одном порядке, а база выполняет в другом:

```text
FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

Поэтому псевдоним из `SELECT` (`AS total`) нельзя использовать в `WHERE`, но можно в `ORDER BY`.

## Шпаргалка

| Что | Как |
|---|---|
| фильтр | `WHERE a = 1 AND b IN (...)` |
| шаблон | `LIKE '%x%'`, `ILIKE` без регистра |
| пусто | `IS NULL` |
| сортировка | `ORDER BY col DESC` |
| первые N | `LIMIT N` |
| уникальные | `DISTINCT` |
| склеить | `JOIN t ON t.id = x.t_id` |
| все слева + совпавшие | `LEFT JOIN` |
| у кого нет | `LEFT JOIN ... WHERE right.id IS NULL` |

## Вопросы собеседования

1. Чем `INNER JOIN` отличается от `LEFT JOIN`?
2. Почему `WHERE country = NULL` ничего не находит?
3. Как найти пользователей без ордеров? (два способа — второй узнаешь в уроке 2)
4. В каком порядке выполняется SELECT-запрос? Почему нельзя использовать псевдоним в WHERE?
5. Чем `LIKE` отличается от `ILIKE`?
