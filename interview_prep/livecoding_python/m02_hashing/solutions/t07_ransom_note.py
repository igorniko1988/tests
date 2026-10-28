from collections import Counter


def can_construct(note: str, magazine: str) -> bool:
    # Каждой буквы в журнале должно быть не меньше, чем в записке. O(n + m).
    have = Counter(magazine)
    for ch, cnt in Counter(note).items():
        if have[ch] < cnt:
            return False
    return True
