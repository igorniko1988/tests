import time
from functools import wraps


def retry(times: int = 3, exceptions: tuple = (Exception,), delay: float = 0.0):
    if times < 1:
        raise ValueError("times must be >= 1")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator
