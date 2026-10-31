def sort_by(records: list[dict], *fields: str) -> list[dict]:
    result = list(records)
    for field in reversed(fields):  # от младшего ключа к старшему: сортировка стабильна
        name = field.lstrip("-")
        result.sort(key=lambda r: r[name], reverse=field.startswith("-"))
    return result
