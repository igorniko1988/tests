from collections import Counter


def first_unique_char(s: str) -> int:
    # Два прохода: сначала посчитать, потом найти первую с count == 1. O(n).
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
