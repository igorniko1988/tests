from collections import Counter


def min_window(s: str, t: str) -> str:
    if not t:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (0, len(s) + 1)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left < best[1] - best[0]:
                best = (left, right)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best[1] > len(s) else s[best[0]:best[1] + 1]
