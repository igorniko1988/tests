def batched(iterable, n):
    if n < 1:
        raise ValueError("n must be >= 1")

    def generate():
        batch = []
        for item in iterable:
            batch.append(item)
            if len(batch) == n:
                yield batch
                batch = []
        if batch:
            yield batch

    return generate()
