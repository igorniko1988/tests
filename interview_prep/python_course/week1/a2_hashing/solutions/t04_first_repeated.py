def first_repeated(s: str) -> str | None:
    seen = set()
    for ch in s:
        if ch in seen:
            return ch
        seen.add(ch)
    return None
