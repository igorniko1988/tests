def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    # Префикс не длиннее самой короткой строки. O(S), S — сумма длин.
    shortest = min(strs, key=len)
    for i, ch in enumerate(shortest):
        for s in strs:
            if s[i] != ch:
                return shortest[:i]
    return shortest
