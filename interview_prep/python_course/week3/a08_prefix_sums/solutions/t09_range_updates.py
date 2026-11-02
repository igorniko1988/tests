def range_updates(n: int, updates: list[tuple[int, int, int]]) -> list[int]:
    diff = [0] * (n + 1)
    for l, r, delta in updates:
        diff[l] += delta
        diff[r + 1] -= delta
    result, running = [], 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result
