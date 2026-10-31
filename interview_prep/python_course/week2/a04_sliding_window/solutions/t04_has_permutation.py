from collections import Counter


def has_permutation(pattern: str, text: str) -> bool:
    k = len(pattern)
    if k > len(text):
        return False
    need = Counter(pattern)
    window = Counter(text[:k])
    if window == need:
        return True
    for right in range(k, len(text)):
        window[text[right]] += 1
        left_ch = text[right - k]
        window[left_ch] -= 1
        if window[left_ch] == 0:
            del window[left_ch]
        if window == need:
            return True
    return False
