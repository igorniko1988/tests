import time
from functools import wraps


def retry(times=3, delay=0.5, backoff=2.0, exceptions=(ConnectionError, TimeoutError), sleep=time.sleep):
    if times < 1:
        raise ValueError("times must be >= 1")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pause = delay
            for attempt in range(1, times + 1):
                wrapper.attempts = attempt
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    sleep(pause)
                    pause *= backoff

        wrapper.attempts = 0
        return wrapper

    return decorator
