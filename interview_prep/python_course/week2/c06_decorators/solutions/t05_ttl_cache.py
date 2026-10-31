import time
from functools import wraps


def ttl_cache(seconds: float, clock=time.monotonic):
    def decorator(func):
        cache = {}  # ключ аргументов -> (время сохранения, результат)

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = clock()
            if key in cache and now - cache[key][0] < seconds:
                return cache[key][1]
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result

        return wrapper

    return decorator
