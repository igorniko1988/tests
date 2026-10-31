from functools import update_wrapper


class CountCalls:
    def __init__(self, func) -> None:
        update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

    def reset(self) -> None:
        self.count = 0
