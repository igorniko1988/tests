def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    return sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])[:k]
