def memoize(func):
    cache = {}

    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            wrapper.calls += 1
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.calls = 0
    return wrapper
