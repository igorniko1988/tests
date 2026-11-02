def coalesce(*values, default=None):
    for value in values:
        if value is not None:  # именно is None, а не truthy-проверка
            return value
    return default


# Однострочник: next((v for v in values if v is not None), default)
