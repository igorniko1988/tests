def first_bad_build(n: int, is_bad) -> int:
    lo, hi = 1, n + 1  # n + 1 — «сломанных нет»
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo if lo <= n else -1
