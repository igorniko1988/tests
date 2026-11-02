def send_in_batches(items, n: int, send) -> dict:
    if n < 1:
        raise ValueError("n must be >= 1")
    result = {"sent": 0, "failed": []}
    number = 0

    def flush(batch):
        nonlocal number
        try:
            send(batch)
            result["sent"] += len(batch)
        except Exception:
            result["failed"].append(number)
        number += 1

    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == n:
            flush(batch)
            batch = []
    if batch:
        flush(batch)
    return result
