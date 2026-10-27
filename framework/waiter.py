import time

def wait(condition, timeout, repeat):
    deadline = time.monotonic() + timeout
    while time.monotonic() <= deadline:
        if condition:
            return
        else:
            time.sleep(repeat)
    raise TimeoutError('Time is out')