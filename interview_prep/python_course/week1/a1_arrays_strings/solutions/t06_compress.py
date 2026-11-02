def compress(s: str) -> str:
    if not s:
        return ""
    parts = []
    current, count = s[0], 0
    for ch in s:
        if ch == current:
            count += 1
        else:
            parts.append(f"{current}{count}")
            current, count = ch, 1
    parts.append(f"{current}{count}")
    return "".join(parts)
