from functools import wraps


def log_calls(log: list[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
            call = f"{func.__name__}({', '.join(parts)})"
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                log.append(f"{call} raised {type(error).__name__}")
                raise
            log.append(f"{call} -> {result!r}")
            return result

        return wrapper

    return decorator
