def common_ids(a: list, b: list) -> list:
    in_b = set(b)  # O(m) — для проверки «есть ли в b»
    added = set()  # для проверки «уже в результате»
    result = []
    for x in a:  # O(n)
        if x in in_b and x not in added:
            added.add(x)
            result.append(x)
    return result


# list(set(a) & set(b)) — тоже O(n + m), но теряет порядок a: у set нет порядка.
# Время O(n + m), память O(n + m).
