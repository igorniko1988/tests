from collections import defaultdict


def character_replacement(s: str, k: int) -> int:
    counts = defaultdict(int)
    left = max_freq = best = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        max_freq = max(max_freq, counts[ch])
        while right - left + 1 - max_freq > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
