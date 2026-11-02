from decimal import Decimal


def sort_records(records: list[dict]) -> list[dict]:
    def key(r: dict):
        if r["amount"] is None:
            # True > False: все записи без суммы уходят в конец
            return (True, Decimal(0), r["name"].lower())
        return (False, -Decimal(r["amount"]), r["name"].lower())

    return sorted(records, key=key)
