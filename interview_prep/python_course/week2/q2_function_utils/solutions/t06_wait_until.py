import time


def wait_until(condition, timeout=5.0, interval=0.1, *, message="condition", clock=time.monotonic, sleep=time.sleep):
    start = clock()
    while True:
        result = condition()
        if result:
            return result
        if clock() - start >= timeout:
            raise TimeoutError(f"{message} not met in {timeout}s, last value: {result!r}")
        sleep(interval)
