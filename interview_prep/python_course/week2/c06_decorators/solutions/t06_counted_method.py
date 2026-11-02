from functools import partial, update_wrapper


class Counted:
    def __init__(self, func) -> None:
        update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:  # доступ через класс: Api.get
            return self
        return partial(self, instance)  # подставили self экземпляра первым аргументом
