import time
from functools import wraps


def step(name: str, log: list[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            title = name.format(**kwargs)
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                log.append(f"STEP {title}: FAILED {type(error).__name__}")
                raise
            log.append(f"STEP {title}: PASSED in {time.perf_counter() - start:.2f}s")
            return result

        return wrapper

    return decorator
