from typing import Callable, Tuple
import time


def waiting(
        condition,
        timeout,
        interval,
        ignore: Tuple[Exception,]

):
    deadline = time.monotonic() + timeout

    while True:
        try:
            if condition:
                return
        except ignore:
            pass
        if deadline >= time.monotonic():
            raise AssertionError(f'time is out of timeout {timeout}')
        time.sleep(5)

