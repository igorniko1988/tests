from .t06_freeze import freeze


def dedupe(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        key = freeze(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
