from collections import Counter


def find_anagrams(text: str, pattern: str) -> list[int]:
    k = len(pattern)
    if k == 0 or k > len(text):
        return []
    need = Counter(pattern)
    window = Counter(text[:k])
    result = [0] if window == need else []
    for right in range(k, len(text)):
        window[text[right]] += 1
        left_ch = text[right - k]
        window[left_ch] -= 1
        if window[left_ch] == 0:
            del window[left_ch]
        if window == need:
            result.append(right - k + 1)
    return result
