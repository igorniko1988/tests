from collections import Counter


def is_anagram(a: str, b: str) -> bool:
    return len(a) == len(b) and Counter(a) == Counter(b)
