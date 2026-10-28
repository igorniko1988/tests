def make_grid(rows: int, cols: int, fill=0) -> list[list]:
    return [[fill] * cols for _ in range(rows)]
