from collections import Counter


def intersect_counts(a: list[int], b: list[int]) -> list[int]:
    left = Counter(b)
    result = []
    for x in a:
        if left[x] > 0:
            result.append(x)
            left[x] -= 1
    return result
