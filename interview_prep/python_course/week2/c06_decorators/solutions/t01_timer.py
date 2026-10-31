import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_duration = time.perf_counter() - start
            print(f"{func.__name__} took {wrapper.last_duration:.3f}s")

    wrapper.last_duration = None
    return wrapper
