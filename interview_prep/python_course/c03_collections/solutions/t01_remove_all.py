def remove_all(items: list, value) -> int:
    before = len(items)
    # Срез слева от = заменяет содержимое того же списка: вызывающий код видит изменения.
    items[:] = [x for x in items if x != value]
    return before - len(items)
