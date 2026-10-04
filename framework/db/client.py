import psycopg
from psycopg.rows import dict_row


class Database:
    """Прямой доступ к базе стенда — только для проверок в тестах."""

    def __init__(self, url: str):
        self.url = url

    def fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        with psycopg.connect(self.url, row_factory=dict_row) as conn:
            return conn.execute(sql, params).fetchone()

    def get_order(self, order_id) -> dict | None:
        return self.fetch_one("SELECT * FROM orders WHERE id = %s", (order_id,))

    def get_balance(self, email: str, asset: str) -> dict | None:
        return self.fetch_one(
            """
            SELECT b.* FROM balances b
            JOIN users u ON u.id = b.user_id
            WHERE u.email = %s AND b.asset = %s
            """,
            (email, asset),
        )
