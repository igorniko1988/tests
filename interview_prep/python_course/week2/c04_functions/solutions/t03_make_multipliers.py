def make_multipliers(n: int) -> list:
    return [lambda x, i=i: x * i for i in range(n)]
