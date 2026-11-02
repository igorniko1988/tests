import time
from collections.abc import Callable


def wait_until(
        condition: Callable[[], bool],
        timeout: float = 10,
        interval: float = 0.5,
        message: str = 'condition not met',
        ignore: tuple[type[Exception], ...] = (),
):
    deadline = time.monotonic() + timeout

    while True:
        try:
            if condition():
                return
        except ignore:
            pass
        if time.monotonic() >= deadline:
            raise AssertionError(f'{message} in {timeout} s')
        time.sleep(interval)
