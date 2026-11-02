def make_counter(start: int = 0, step: int = 1):
    current = start - step

    def counter() -> int:
        nonlocal current
        current += step
        return current

    return counter
