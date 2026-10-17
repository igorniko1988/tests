# F3. Урок 4 — SQL-задачи с лайвкодинга

Задания: `practice/f3_04_interview.sql`. Данные — учебная схема `sql_practice`.

## Как решать на собесе

1. **Уточни**: что вернуть (колонки), что делать с NULL и дублями, нужна ли сортировка.
2. Скажи вслух **план**: «соединю users и orders LEFT JOIN, отфильтрую тех, у кого нет пары».
3. Пиши **по частям**: сначала `FROM ... JOIN`, проверь, потом `WHERE`, потом `GROUP BY`.
4. Проверь на **краевых случаях**: пользователь без ордеров, NULL в колонке, одинаковые значения.

## Шаблоны, которые покрывают 90% задач

```sql
-- 1. «нет связанных» — LEFT JOIN + IS NULL  или  NOT EXISTS
SELECT u.* FROM users u LEFT JOIN orders o ON o.user_id = u.id WHERE o.id IS NULL;

-- 2. «сумма / количество по группам»
SELECT status, count(*), sum(quantity) FROM orders GROUP BY status;

-- 3. «дубли»
SELECT email, count(*) FROM users GROUP BY email HAVING count(*) > 1;

-- 4. «топ-N в каждой группе» / «последний»
SELECT * FROM (
    SELECT *, row_number() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn FROM orders
) t WHERE rn <= 2;

-- 5. «второе по величине»
SELECT DISTINCT price FROM orders ORDER BY price DESC OFFSET 1 LIMIT 1;
-- или: SELECT max(price) FROM orders WHERE price < (SELECT max(price) FROM orders);

-- 6. «удалить дубли, оставив одну строку»
DELETE FROM orders a USING orders b
WHERE a.id > b.id
  AND (a.user_id, a.symbol, a.side, a.price, a.quantity, a.created_at)
    = (b.user_id, b.symbol, b.side, b.price, b.quantity, b.created_at);

-- 7. «по дням»
SELECT date_trunc('day', created_at) AS day, count(*) FROM orders GROUP BY 1 ORDER BY 1;
```

Задачу 6 в учебной базе запускай внутри `BEGIN; ... ROLLBACK;` — или перезалей seed после.

## Вопросы, которые задают вместе с задачами

- Чем `DELETE`, `TRUNCATE` и `DROP` отличаются? (строки по условию с логом / все строки быстро / таблица целиком)
- `UNION` vs `UNION ALL`? (без дублей, медленнее / со всеми строками)
- Что такое первичный и внешний ключ? (уникальный идентификатор строки / ссылка на строку другой таблицы)
- Что такое нормализация? (разнести данные по таблицам без дублирования — email хранится в users, а не в каждом ордере)
