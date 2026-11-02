class lazy_property:
    def __init__(self, func) -> None:
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        instance.__dict__[self.name] = value  # дальше Python найдёт значение в объекте
        return value
