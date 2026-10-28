from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    # Counter: O(n). Вариант sorted(s) == sorted(t): O(n log n).
    return Counter(s) == Counter(t)
