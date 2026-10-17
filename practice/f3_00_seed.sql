-- Учебные данные для модуля F3 (SQL).
-- Живут в отдельной схеме sql_practice, таблицы стенда (public) не трогают.
-- Загрузить (можно повторно — схема пересоздаётся):
--   docker compose exec -T db psql -U exchange -d exchange < practice/f3_00_seed.sql
-- Открыть консоль:
--   docker compose exec db psql -U exchange -d exchange
--   SET search_path TO sql_practice;

DROP SCHEMA IF EXISTS sql_practice CASCADE;
CREATE SCHEMA sql_practice;
SET search_path TO sql_practice;

CREATE TABLE users (
    id         serial PRIMARY KEY,
    email      varchar(320) NOT NULL UNIQUE,
    country    varchar(2),
    created_at timestamptz NOT NULL
);

CREATE TABLE balances (
    id        serial PRIMARY KEY,
    user_id   int NOT NULL REFERENCES users (id),
    asset     varchar(10) NOT NULL,
    available numeric(36, 18) NOT NULL DEFAULT 0,
    locked    numeric(36, 18) NOT NULL DEFAULT 0,
    UNIQUE (user_id, asset)
);

CREATE TABLE orders (
    id              serial PRIMARY KEY,
    user_id         int NOT NULL REFERENCES users (id),
    symbol          varchar(20) NOT NULL,
    side            varchar(4) NOT NULL,
    price           numeric(36, 18) NOT NULL,
    quantity        numeric(36, 18) NOT NULL,
    filled_quantity numeric(36, 18) NOT NULL DEFAULT 0,
    status          varchar(20) NOT NULL,
    created_at      timestamptz NOT NULL
);

INSERT INTO users (id, email, country, created_at) VALUES
    (1, 'anna@test.io',   'DE', '2026-09-01 10:00+00'),
    (2, 'boris@test.io',  'PL', '2026-09-02 11:30+00'),
    (3, 'carl@test.io',   'DE', '2026-09-03 09:15+00'),
    (4, 'dina@test.io',   NULL, '2026-09-05 18:00+00'),
    (5, 'egor@test.io',   'UA', '2026-09-10 08:45+00'),
    (6, 'fiona@test.io',  'PL', '2026-09-15 20:10+00'),
    (7, 'ANNA@test.io',   'DE', '2026-09-20 12:00+00');   -- «почти дубль» по email
SELECT setval('users_id_seq', 7);

INSERT INTO balances (user_id, asset, available, locked) VALUES
    (1, 'USDT', 5000, 2000),
    (1, 'ETH',  3,    0),
    (2, 'USDT', 100,  0),
    (2, 'BTC',  0.5,  0.1),
    (3, 'USDT', 0,    0),
    (5, 'USDT', 12000, 6200),
    (5, 'ETH',  10,   2),
    (6, 'BTC',  1,    0),
    (7, 'USDT', -50,  0);                                   -- отрицательный баланс: так быть не должно

INSERT INTO orders (user_id, symbol, side, price, quantity, filled_quantity, status, created_at) VALUES
    (1, 'ETH-USDT', 'BUY',  2000,  1,   0,   'NEW',              '2026-09-21 10:00+00'),
    (1, 'ETH-USDT', 'BUY',  1950,  0.5, 0.5, 'FILLED',           '2026-09-21 10:05+00'),
    (1, 'BTC-USDT', 'SELL', 61000, 0.1, 0,   'CANCELED',         '2026-09-22 14:00+00'),
    (2, 'BTC-USDT', 'SELL', 60000, 0.1, 0,   'NEW',              '2026-09-22 15:00+00'),
    (2, 'BTC-USDT', 'SELL', 60500, 0.2, 0.2, 'FILLED',           '2026-09-23 09:00+00'),
    (5, 'ETH-USDT', 'SELL', 2100,  2,   1,   'PARTIALLY_FILLED', '2026-09-23 11:00+00'),
    (5, 'ETH-USDT', 'BUY',  2050,  3,   0,   'NEW',              '2026-09-24 12:00+00'),
    (5, 'BTC-USDT', 'BUY',  59000, 0.05,0,   'NEW',              '2026-09-24 12:30+00'),
    (5, 'ETH-USDT', 'BUY',  2000,  1,   1,   'FILLED',           '2026-09-25 16:00+00'),
    (6, 'BTC-USDT', 'SELL', 62000, 0.5, 0,   'CANCELED',         '2026-09-26 10:00+00'),
    (6, 'BTC-USDT', 'SELL', 62000, 0.5, 0,   'CANCELED',         '2026-09-26 10:00+00'),  -- дубль
    (7, 'ETH-USDT', 'BUY',  1900,  1,   2,   'FILLED',           '2026-09-27 13:00+00');  -- filled > quantity: баг данных
