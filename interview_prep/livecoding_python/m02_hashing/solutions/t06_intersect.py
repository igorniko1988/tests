from collections import Counter


def intersect(a: list[int], b: list[int]) -> list[int]:
    # Counter & Counter берёт минимум количеств. O(n + m).
    return list((Counter(a) & Counter(b)).elements())
