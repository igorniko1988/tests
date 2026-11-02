def validate(data: dict, schema: dict[str, type]) -> list[str]:
    errors = []
    for field, expected in schema.items():
        if field not in data:
            errors.append(f"missing: {field}")
        elif type(data[field]) is not expected:
            got = type(data[field]).__name__
            errors.append(f"type: {field} expected {expected.__name__}, got {got}")
    return errors
