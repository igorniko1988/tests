def call_logger(func, log: list[str]):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        log.append(f"{func.__name__}({', '.join(parts)}) -> {result!r}")
        return result

    return wrapper
