def freeze(obj):
    if isinstance(obj, dict):
        return frozenset((key, freeze(value)) for key, value in obj.items())
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(item) for item in obj)
    if isinstance(obj, set):
        return frozenset(freeze(item) for item in obj)
    return obj
