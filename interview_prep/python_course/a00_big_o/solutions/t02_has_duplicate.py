def has_duplicate(items: list) -> bool:
    seen = set()
    for x in items:
        if x in seen:  # O(1) вместо прохода по списку
            return True
        seen.add(x)
    return False


# Короче, но всегда строит множество целиком (нет раннего выхода):
#     return len(set(items)) != len(items)
# Время O(n), память O(n) в обоих вариантах.
