def int_sqrt(x: int) -> int:
    lo, hi = 0, x
    while lo < hi:  # ищем наибольшее k с k * k <= x
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo
