def my_deepcopy(obj):
    if isinstance(obj, dict):
        return {key: my_deepcopy(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [my_deepcopy(item) for item in obj]
    if isinstance(obj, tuple):
        return tuple(my_deepcopy(item) for item in obj)
    if isinstance(obj, set):
        return {my_deepcopy(item) for item in obj}
    return obj
